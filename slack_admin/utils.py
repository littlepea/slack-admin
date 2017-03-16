import time

import humanfriendly
import parsedatetime


def parse_date_string(date_string):
    """Returns datetime from a human-readable date string

    :param date_string: Human-readable date string (ex: "1 month ago", "1 Jan, 2017")
    :return: datetime object
    """
    cal = parsedatetime.Calendar()
    parsed_date, parse_status = cal.parseDT(datetimeString=date_string)
    if parse_status:
        return parsed_date


def get_timestamp_from_date_string(date_string):
    """Returns timestamp from a human-readable date string

    :param date_string: Human-readable date string (ex: "1 month ago", "1 Jan, 2017")
    :return: datetime object
    """
    parsed_date = parse_date_string(date_string)
    if parsed_date:
        timestamp = int(time.mktime(parsed_date.timetuple()))
        return timestamp


def get_bytes_size_from_string(size):
    """Returns a size in bytest from a human-readable string

    :param size: Human-readable size string (ex: 500Kb)
    :return: Size in bytes
    """
    try:
        bytes_size = humanfriendly.parse_size(size)
        return bytes_size
    except humanfriendly.InvalidSize:
        return None
    except TypeError:
        return None
