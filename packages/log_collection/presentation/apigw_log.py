"""_summary_
"""

from datetime import datetime

from packages.log_collection.usecase.apigw_log.apigw_log import ApigwLog


def main():
    """_summary_"""
    start_date = datetime(2024, 2, 1)
    end_date = datetime(2024, 4, 17)
    marker = ""

    apigw_log = ApigwLog()
    apigw_log.fatch_from_s3("prod", start_date, end_date, marker)


if __name__ == "__main__":
    main()
