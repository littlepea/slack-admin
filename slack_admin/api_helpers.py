from urllib.parse import urlencode


BASE_URI = 'https://slack.com/api/'


def build_url(token, method, **kwargs):
    """Returns an API call URL for a given method

    :param token: Slack API token
    :param method: API method name
    :param kwargs: QueryString parameters
    :return: URL
    """
    query_string = urlencode(dict(kwargs, token=token))
    return f'{BASE_URI}{method}?{query_string}'


def build_files_list_url(token, to_timestamp=None, page=None):
    """Returns a URL for the files list API call

    :param token: Slack API token
    :param to_timestamp: Files older than this timestamp
    :return: URL
    """
    params = {}
    if to_timestamp:
        params['ts_to'] = to_timestamp
    if page:
        params['page'] = page
    return build_url(token, 'files.list', **params)


def build_file_delete_url(token, file_id):
    """Returns a URL for the delete file API call

    :param token: Slack API token
    :param file_id: ID of the file to be deleted
    :return: URL
    """
    return build_url(token, 'files.delete', file=file_id)


def get_files_from_response(response):
    """Returns a list of files from Slack API response

    :param response: Slack API JSON response
    :return: List of files
    """
    return response.get('files', [])


def get_page_range_from_response(response, start_from=1):
    """Returns a range of pages from Slack API response

    :param response: Slack API JSON response
    :return: Range of pages
    """
    return range(start_from, response['paging']['pages'] + 1)


def filter_files_by_size(files, bigger_than):
    """Returns files filtered by size

    :param files: List of files to be filtered
    :param bigger_than: Only return files bigger that this amount of bytes
    :return: Filtered list of files
    """
    return [file for file in files if file['size'] > bigger_than]
