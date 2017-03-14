import asyncio
import os
import time

import aiohttp
import click
import humanfriendly
import parsedatetime


@click.group()
def cli():
    """
    Slack admin CLI
    """
    pass


@cli.command()
@click.option('--older', '-o', default='1 year ago', help='Older than (ex: 2017-12-09, "1 month ago", etc..., '
                                                          'default: "1 year ago")')
@click.option('--bigger', '-b', help='Bigger than (ex: 1M, 2Gb, etc...)')
@click.option('--prompt/--no-prompt', default=True)
@click.option('--token', '-t', help='Slack API token (default: SLACK_API_TOKEN env variable value)')
def cleanup(older, bigger, prompt, token):
    """
    Cleans up old file attachments from Slack
    """
    cal = parsedatetime.Calendar()
    older_than, parse_status = cal.parseDT(datetimeString=older)
    older_than_timestamp = int(time.mktime(older_than.timetuple()))
    if not parse_status:
        print('Can\'t parse the date: {}'.format(older))
        return

    try:
        bigger_than = humanfriendly.parse_size(bigger)
    except humanfriendly.InvalidSize:
        print(f'Can\'t parse the file size: {bigger}')
        return
    except TypeError:
        bigger_than = None

    token = token or os.environ.get('SLACK_API_TOKEN')
    if not token:
        print('Please, provide --token or set SLACK_API_TOKEN env variable')
        return

    event_loop = asyncio.get_event_loop()
    try:
        files = event_loop.run_until_complete(
            get_files(token, older_than_timestamp, bigger_than)
        )

        print(f'Going to delete all files older than {older}' +
              (f' and bigger than {bigger}' if bigger_than else f''))
        print(f'{len(files)} will be deleted')
        if prompt and input('Do you agree? [y/n]').lower() != 'y':
            print('Canceled deleting files')
            return

        space_cleared = event_loop.run_until_complete(
            delete_files(token, files)
        )
    finally:
        event_loop.close()

    print(f'Deleted {len(files)} files, saved {space_cleared / 1000000}Mb')


async def get_files(token, older_than_timestamp, bigger_than=None):
    files = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://slack.com/api/files.list',
                               params={'token': token, 'ts_to': older_than_timestamp}) as resp:
            first_page = await resp.json()
            files += first_page['files']

        for page in range(2, first_page['paging']['pages'] + 1):
            async with session.get('https://slack.com/api/files.list',
                                   params={'token': token, 'ts_to': older_than_timestamp, 'page': page}) as resp:
                current_page = await resp.json()
                files += current_page['files']

    if bigger_than:
        return [file for file in files if file['size'] > bigger_than]

    return files


async def delete_files(token, files):
    space = 0
    count = 1
    num_files = len(files)
    async with aiohttp.ClientSession() as session:
        for file in files:
            async with session.get('https://slack.com/api/files.delete',
                                   params={'token': token, 'file': file['id']}) as resp:
                result = await resp.json()

                if result['ok']:
                    print(f'deleted file {count} of {num_files}: "{file["name"]}"')
                    space += file['size']
                    count += 1
                else:
                    print(f'failed to delete file "{file["name"]}" because of "{result["error"]}"')
    return space


if __name__ == '__main__':
    cli()
