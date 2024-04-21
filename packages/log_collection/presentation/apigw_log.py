import argparse
import asyncio
from datetime import datetime
from enum import Enum

from packages.log_collection.usecase.apigw_log.apigw_log import ApigwLog


class BatchType(Enum):
    FETCH_LOG = "fetch_log"
    LOAD_LOG = "load_log"


async def execute(
    batch_type: BatchType,
    environment: str,
    str_start_date: str | None,
    str_end_date: str | None,
    marker: str = "",
) -> None:
    """execute batch process designated by batch_type"""
    apigw_log = ApigwLog()
    if batch_type == BatchType.FETCH_LOG:
        start_date = (
            datetime.strptime(str_start_date, "%Y-%m-%d")
            if str_start_date
            else datetime(2024, 1, 1)
        )
        end_date = (
            datetime.strptime(str_end_date, "%Y-%m-%d")
            if str_end_date
            else datetime(2024, 6, 30)
        )

        apigw_log.fatch_from_s3(environment, start_date, end_date, marker)
    elif batch_type == BatchType.LOAD_LOG:
        await apigw_log.load_log_data_to_db()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--type", required=True, help="batch type (fetch_log/load_log)"
    )
    parser.add_argument(
        "-e", "--environment", required=True, help="environment name (dev/stg/prod)"
    )
    parser.add_argument(
        "-S", "--start_date", help="start date from when log files stored, YYYY-MM-DD"
    )
    parser.add_argument(
        "-E", "--end_date", help="end date till when log files stored, YYYY-MM-DD"
    )
    parser.add_argument(
        "-m",
        "--marker",
        help="marker to specify the restart point of the batch process",
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        execute(
            BatchType(args.type),
            args.environment,
            str_start_date=args.start_date,
            str_end_date=args.end_date,
            marker=args.marker,
        )
    )
