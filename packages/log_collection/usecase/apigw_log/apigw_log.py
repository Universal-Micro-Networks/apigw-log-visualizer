import glob
import gzip
import io
import json
import os
import shutil
import uuid
from datetime import datetime, timedelta
from typing import Any, Generator, TextIO

import boto3
from botocore.exceptions import RefreshWithMFAUnsupportedError

from packages.log_collection.domain.apigw_log.apigw_log_schema import ApigwLogSchema
from packages.log_collection.infra.apigw_analysis_db import get_db_connection
from packages.log_collection.infra.model.access_log import AccessLog as AccessLogModel


class ApigwLog:
    s3 = boto3.client("s3", region_name="ap-northeast-1")

    def fatch_from_s3(
        self, environment: str, start_date: datetime, end_date: datetime, marker: str
    ) -> None:
        """fetch log files from S3

        Args:
            environment (str): environment name i.e. prod, stg, dev
            start_date (datetime): date after when log files are collected
            end_date (datetime): date before when log files are collected
            marker (str, optional): S3 marker to restart this function where ended last time. Defaults to "".
        """
        bucket_name_suffix = os.getenv("BUCKET_NAME_SUFFIX", "iapigw-access-logs")
        bucket = f"{environment}-{bucket_name_suffix}"
        prefixes = self._get_prefixes(start_date, end_date)
        files = self._get_s3_objects(bucket, prefixes, marker)
        self._save_logfile_to_json(files)

    def _get_prefixes(
        self, start_date: datetime, end_date: datetime
    ) -> Generator[str, Any, None]:
        """Get S3 prefixes

        Args:
            start_date (datetime): date after when log files are collected
            end_date (datetime): date before when log files are collected

        Yields:
            Generator[str, Any, None]: S3 prefix generator
        """
        days = (end_date - start_date).days
        date_list = map(lambda x, y=start_date: y + timedelta(days=x), range(days))
        for d in date_list:
            yield f"{d.year}/{d.month}/{d.day}/"

    def _get_s3_objects(
        self, _bucket, _prefixes: Generator[str, Any, None], _marker: str = ""
    ) -> Generator[gzip.GzipFile | TextIO, Any, None]:
        """Get log files from S3

        Args:
            _bucket (_type_): S3 Backet Name
            _prefixes (Generator[str, Any, None]): S3 prefix list
            _marker (str, optional): S3 marker to restart this function where ended last time. Defaults to "".

        Raises:
            ApigwLogError: Raise when MFA token is expired or gzip file is invalid.
        Yields:
            Generator[gzip.GzipFile | TextIO, Any, None]: uncompressed log file generator
        """
        for prefix in _prefixes:
            print(f"{_bucket}:{prefix}")
            while True:
                print(f"list objects with marker:{_marker}")
                response = self.s3.list_objects(
                    Bucket=_bucket, Prefix=prefix, Marker=_marker
                )
                is_truncated = response["IsTruncated"]
                if "Contents" not in response:
                    break

                for content in response["Contents"]:
                    _marker = content["Key"]

                    if content["Key"].endswith(".gz"):
                        try:
                            obj = self.s3.get_object(
                                Bucket=_bucket, Key=content["Key"]
                            )["Body"].read()
                        except RefreshWithMFAUnsupportedError as e:
                            raise ApigwLogError(
                                f"MFAの有効期限切れの可能性があります。再開するには以下の設定をしてください。\n\n開始日:{prefix} marker:{_marker}"
                            ) from e

                        # main
                        if _valid_gzip_format(obj):
                            with gzip.open(io.BytesIO(obj), "rt") as file:
                                yield file
                        else:
                            raise ApigwLogError(
                                "ファイル拡張子(.gz)に対して圧縮形式が正しくありません。"
                            )

                if is_truncated is False:
                    break

    def _save_logfile_to_json(
        self, _files: Generator[gzip.GzipFile | TextIO, Any, None]
    ) -> None:
        """save log file to csv

        Args:
            _files (Generator[gzip.GzipFile  |  TextIO, Any, None]): log file
        """
        for file in _files:
            random_filename = uuid.uuid4()
            os.makedirs("logs", exist_ok=True)
            with open(f"logs/{random_filename}.json", mode="w", encoding="UTF-8") as f:
                rows = file.readlines()
                is_first = True
                f.write("[")
                for row in rows:
                    if " " in str(row):
                        if is_first:
                            is_first = False
                        else:
                            f.write(",")
                        json_obj = str(row).split(" ", 1)[1]
                        f.write(json_obj)
                f.write("]")

    async def load_log_data_to_db(self) -> None:
        """load log data to DB"""
        async_session = get_db_connection()
        os.makedirs("logs/loaded", exist_ok=True)
        log_dict_list = self._get_log_data_from_files()

        await self._insert_log_data_to_db(async_session, log_dict_list)

    def _get_log_data_from_files(self) -> Generator[dict[str, Any], Any, None]:
        """Get log files

        Yields:
            Generator[str, Any, None]: log file generator
        """
        files = glob.glob("logs/*.json")
        file_num = len(files)
        loaded_file_num = 1
        for file in files:
            with open(file, mode="r", encoding="UTF-8") as f:
                log_dict_list = json.load(f)
                yield from log_dict_list
            shutil.move(file, "logs/loaded/")
            print(f"{loaded_file_num:,}/{file_num:,} are loaded")
            loaded_file_num = loaded_file_num + 1

    async def _insert_log_data_to_db(
        self, async_session, log_dict_list: Generator[dict[str, Any], Any, None]
    ) -> None:
        """load log data to DB

        Args:
            log_dict (dict): log data
        """
        for log_dict in log_dict_list:
            log_dict = self._correct_log_data(log_dict)
            access_log_data = ApigwLogSchema(**log_dict)
            async with async_session() as session:
                async with session.begin():
                    access_log_model = AccessLogModel(**access_log_data.model_dump())
                    session.add(access_log_model)
                await session.commit()

    def _correct_log_data(self, log_dict: dict) -> dict:
        """Correct log data

        Args:
            log_dict (dict): source log data

        Returns:
            dict: corrected log data if needed
        """
        # it's alomost impossible to convert requestTime string to datetime object, so I get requestTime from requestTimeEpoch
        log_dict["requestTime"] = datetime.fromtimestamp(
            float(log_dict["requestTimeEpoch"]) / 1000
        )
        log_dict["integrationStatus"] = _try_conv_str_to_int(
            log_dict["integrationStatus"]
        )
        log_dict["integrationLatency"] = _try_conv_str_to_int(
            log_dict["integrationLatency"]
        )
        return log_dict


class ApigwLogError(Exception):
    """API Gateway Log Error

    Args:
        Exception (_type_): Base Exception
    """

    def __init__(self, message: str) -> None:
        """_summary_

        Args:
            message (str): _description_
        """
        self.message = message

    def __str__(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.message


def _valid_gzip_format(file_obj: bytes) -> bool:
    """Check if gzip file format is valid

    Args:
        file_obj (bytes): gzip file object

    Returns:
        _type_: True if valid, False if invalid
    """
    with gzip.open(io.BytesIO(file_obj), "rt") as testing_file:
        try:
            testing_file.read()
            return True
        except OSError:
            return False


def _try_conv_str_to_int(challenge: str) -> int:
    """Try to convert a string to an integer

    Args:
        challenge (str): string to convert to integer

    Returns:
        int: converted integer
    """
    try:
        return int(challenge)
    except ValueError:
        return 0
