from datetime import datetime
from dateutil import parser


def string_to_date(date_str: str) -> datetime:
    if date_str is None:
        return
    try:
        return parser.parse(date_str)
    except:
        raise Exception(f"Unable to convert date {date_str}")
