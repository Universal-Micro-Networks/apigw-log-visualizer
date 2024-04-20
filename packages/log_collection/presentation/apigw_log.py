import argparse
from datetime import datetime
from enum import Enum

from packages.log_collection.usecase.apigw_log.apigw_log import ApigwLog


class BatchType(Enum):
    FETCH_LOG = "fetch_log"
    LOAD_LOG = "load_log"


def execute(batch_type: BatchType):
    """execute batch process designated by batch_type"""
    apigw_log = ApigwLog()
    if batch_type == BatchType.FETCH_LOG:
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 4, 17)
        marker = ""

        apigw_log.fatch_from_s3("prod", start_date, end_date, marker)
    elif batch_type == BatchType.LOAD_LOG:
        apigw_log.load_to_db()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", required=True)
    args = parser.parse_args()

    execute(BatchType(args.type))
