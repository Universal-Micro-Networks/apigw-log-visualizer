import gzip
import io
import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Generator, TextIO

import boto3
from botocore.exceptions import RefreshWithMFAUnsupportedError


class ApigwLog:
    s3 = boto3.client("s3", region_name="ap-northeast-1")

    def fatch_from_s3(self, environment: str, start_date: datetime, end_date: datetime, marker: str):
        environment = "prod"
        bucket = f"{environment}-iapigw-access-logs"
        prefixes = self._get_prefixes(start_date, end_date)
        files = self._get_s3_objects(bucket, prefixes, marker)
        self._save_logfile_to_csv(files)

    def load(self):
        pass

    def _get_prefixes(
        self, start_date: datetime, end_date: datetime
    ) -> Generator[str, Any, None]:
        days = (end_date - start_date).days
        date_list = map(lambda x, y=start_date: y + timedelta(days=x), range(days))
        for d in date_list:
            yield f"{d.year}/{d.month}/{d.day}/"

    def _get_s3_objects(
        self, _bucket, _prefixes: Generator[str, Any, None], _marker: str = ""
    ) -> Generator[gzip.GzipFile | TextIO, Any, None]:
        for prefix in _prefixes:
            print(f"{_bucket}:{prefix}")
            while True:
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
                            )

                        # main
                        if _valid_gzip_format(obj):
                            with gzip.open(io.BytesIO(obj), "rt") as file:
                                yield file
                        else:
                            raise Exception(
                                "ファイル拡張子(.gz)に対して圧縮形式が正しくありません。"
                            )

                if is_truncated is False:
                    break

    def _save_logfile_to_csv(
        self, _files: Generator[gzip.GzipFile | TextIO, Any, None]
    ):
        for file in _files:
            randam_filename = uuid.uuid4()
            os.makedirs(f"logs", exist_ok=True)
            with open(f"logs/{randam_filename}.csv", mode="w") as f:
                rows = file.readlines()
                for row in rows:
                    f.write(str(row))

    def _save_to_csv(self, f, _rows):
        for row in _rows:
            f.write(row)


class ApigwLogError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


def _valid_gzip_format(file_obj: bytes):
    with gzip.open(io.BytesIO(file_obj), "rt") as testing_file:
        try:
            testing_file.read()
            return True
        except OSError:
            return False


def _try_conv_str_to_int(challenge: str) -> int:
    try:
        return int(challenge)
    except ValueError:
        return 0
