"""
Tests for `slack_admin.utils` module.
"""
import pytest
import datetime

from freezegun import freeze_time

from slack_admin import utils


@freeze_time('2017-01-30')
class TestDateParsing(object):
    def test_parse_date_string_from_one_year_ago(self):
        assert utils.parse_date_string('1 year ago') == datetime.datetime(2016, 1, 30, 8)
        assert utils.get_timestamp_from_date_string('1 year ago') == 1454112000

    def test_parse_date_string_from_specific_date(self):
        assert utils.parse_date_string('2016-11-01') == datetime.datetime(2016, 11, 1, 8)
        assert utils.get_timestamp_from_date_string('2016-11-01') == 1477958400

    def test_parse_invalid_date_string(self):
        assert utils.parse_date_string('lkj345') is None
        assert utils.get_timestamp_from_date_string('lkj345') is None


class TestSizeParsing(object):
    def test_parse_size_of_one_megabyte(self):
        assert utils.get_bytes_size_from_string('1M') == 1000000

    def test_parse_size_of_half_megabyte(self):
        assert utils.get_bytes_size_from_string('500Kb') == 500000

    def test_parse_invalid_size(self):
        assert utils.get_bytes_size_from_string('five bottles') is None
