# pylint:disable=protected-access
# pylint:disable=missing-function-docstring
import glob
import gzip
import os
from datetime import datetime, timedelta
from typing import Any, Generator, TextIO

from faker import Faker

from packages.log_collection.usecase.apigw_log import apigw_log

MIN_HTTP_STATUS_CODE = 200
MAX_HTTP_STATUS_CODE = 500
MIN_APIGW_ACCEPTABLE_LATENCY = 1
MAX_APIGW_ACCEPTABLE_LATENCY = 30000


def test_fatch_from_s3() -> None:
    # nothing to test at the moment
    pass


def test_get_prefixes() -> None:
    apigw_log_obj = apigw_log.ApigwLog()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    prefixes = apigw_log_obj._get_prefixes(start_date, end_date)
    for prefix in prefixes:
        print(prefix)
        assert prefix == f"{start_date.year}/{start_date.month}/{start_date.day}/"
        start_date = start_date + timedelta(days=1)


def test_get_s3_objects() -> None:
    # prefixes = _prefix_generator()

    # apigw_log_obj = apigw_log.ApigwLog()
    # TODO: implement test after implementing minio in docker
    pass


def test_save_logfile_to_json(mocker) -> None:
    apigw_log_obj = apigw_log.ApigwLog()
    mock_open_json = mocker.patch(
        "packages.log_collection.usecase.apigw_log.apigw_log.open",
        new_callable=mocker.mock_open,
    )
    files = _log_obj_generator()
    apigw_log_obj._save_logfile_to_json(files)
    mock_open_json.assert_called_once()
    # TODO: implement something to chekck the written data


def test_load_log_data_to_db() -> None:
    # nothing to test at the moment
    pass


def test_get_log_data_from_files(mocker) -> None:
    files = glob.glob(f"{os.path.dirname(__file__)}/test_logs_to_load/*.json")
    mocker.patch("glob.glob", return_value=files)

    apigw_log_obj = apigw_log.ApigwLog()
    result = apigw_log_obj._get_log_data_from_files()

    for log_dict in result:
        print(log_dict)
        assert "str_key" in log_dict
        assert "int_key" in log_dict
        assert "bool_key" in log_dict


def test_insert_log_data_to_db() -> None:
    # TODO: implement
    pass


def test_correct_log_data() -> None:
    faker = Faker("jp-JP")
    random_datetime = faker.past_datetime()
    expected_request_time_epoch = int(
        random_datetime.timestamp() * 1000
    )  # convert to milliseconds

    expected = {
        "requestTime": random_datetime,
        "integrationStatus": faker.random_int(
            min=MIN_HTTP_STATUS_CODE, max=MAX_HTTP_STATUS_CODE
        ),
        "integrationLatency": faker.random_int(
            min=MIN_APIGW_ACCEPTABLE_LATENCY, max=MAX_APIGW_ACCEPTABLE_LATENCY
        ),
    }

    challenge = {
        "requestTimeEpoch": str(expected_request_time_epoch),
        "integrationStatus": str(expected["integrationStatus"]),
        "integrationLatency": str(expected["integrationLatency"]),
    }
    apigw_log_obj = apigw_log.ApigwLog()
    result = apigw_log_obj._correct_log_data(challenge)

    assert "requestTime" in result
    assert isinstance(result["requestTime"], datetime)
    # compare only seconds
    assert (
        int(result["requestTime"].timestamp()) / 1000
        == int(expected["requestTime"].timestamp()) / 1000
    )
    assert result["integrationStatus"] == expected["integrationStatus"]
    assert result["integrationLatency"] == expected["integrationLatency"]


def test_valid_gzip_format() -> None:
    with open(
        f"{os.path.dirname(__file__)}/test_files/gzip_challenge.txt.gz", mode="rb"
    ) as f:
        challenge = f.read()
        result = apigw_log._valid_gzip_format(challenge)
        assert result

    with open(
        f"{os.path.dirname(__file__)}/test_files/gzip_challenge.txt.zip", mode="rb"
    ) as f:
        challenge = f.read()
        result = apigw_log._valid_gzip_format(challenge)
        assert result == False

    with open(
        f"{os.path.dirname(__file__)}/test_files/gzip_challenge.txt", mode="rb"
    ) as f:
        challenge = f.read()
        result = apigw_log._valid_gzip_format(challenge)
        assert result == False


def test_try_conv_str_to_int() -> None:
    faker = Faker("jp-JP")
    # 銀行の番号であれば、文字列を数値に変換できる
    random_int = faker.random_int(min=1, max=9999)
    challenge = str(random_int)
    result = apigw_log._try_conv_str_to_int(challenge)
    assert result == random_int

    challenge = faker.word()
    print(f"failuer test string: {challenge}")
    result = apigw_log._try_conv_str_to_int(challenge)
    assert result == 0


def _prefix_generator() -> Generator[str, Any, None]:
    yield f"{2024}/{1}/{2}/"


def _log_obj_generator() -> Generator[gzip.GzipFile | TextIO, Any, None]:
    with gzip.open(
        f"{os.path.dirname(__file__)}/test_files/gzip_challenge.txt.gz",
        mode="rt",
    ) as f:
        yield f
