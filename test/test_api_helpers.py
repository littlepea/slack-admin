import pytest

from slack_admin import api_helpers


class TestRequestHelpers(object):
    def test_build_url(self):
        assert api_helpers.build_url('xxx', 'users.list', p1='a', p2='b') == \
               'https://slack.com/api/users.list?p1=a&p2=b&token=xxx'

    def test_build_files_list_url(self):
        assert api_helpers.build_files_list_url('xxx') == 'https://slack.com/api/files.list?token=xxx'

    def test_build_files_list_url_for_page_two(self):
        assert api_helpers.build_files_list_url('xxx', page=2) == \
               'https://slack.com/api/files.list?page=2&token=xxx'

    def test_build_files_list_url_until_a_certain_date(self):
        assert api_helpers.build_files_list_url('xxx', to_timestamp='111') == \
               'https://slack.com/api/files.list?ts_to=111&token=xxx'

    def test_build_file_delete_url(self):
        assert api_helpers.build_file_delete_url('xxx', file_id='111') == \
               'https://slack.com/api/files.delete?file=111&token=xxx'


class TestResponseHelpers(object):
    def test_get_files_from_response(self):
        assert api_helpers.get_files_from_response({
            'files': [1, 2, 3]
        }) == [1, 2, 3]

    def test_get_page_range_from_response(self):
        assert api_helpers.get_page_range_from_response({
            'paging': {
                'pages': 5
            }
        }) == range(1, 6)

    def test_get_page_range_from_response_starting_from_second_page(self):
        assert api_helpers.get_page_range_from_response({
            'paging': {
                'pages': 5
            }
        }, start_from=2) == range(2, 6)

    def test_filter_files_bigger_than_one_megabyte(self):
        assert api_helpers.filter_files_by_size(
            [
                {'size': 1},
                {'size': 2},
                {'size': 1000100},
            ],
            bigger_than=1000000
        ) == [{'size': 1000100}]
