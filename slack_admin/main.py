import asyncio
import os
import time

import click
import parsedatetime
import humanfriendly

from slackclient import SlackClient


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
        click.echo('Can\'t parse the date: {}'.format(older))
        return

    try:
        num_bytes = humanfriendly.parse_size(bigger)
    except humanfriendly.InvalidSize:
        click.echo(f'Can\'t parse the file size: {bigger}')
        return
    except TypeError:
        num_bytes = None

    token = token or os.environ.get('SLACK_API_TOKEN')
    if not token:
        click.echo('Please, provide --token or set SLACK_API_TOKEN env variable')
        return

    prompt_message = f'Going to delete all files older than {older}' + \
                     (f' and bigger than {bigger}' if num_bytes else f'')

    click.echo(prompt_message)
    if prompt and input('Do you agree? [y/n]').lower() != 'y':
        click.echo('Canceled deleting files')
        return

    client = SlackClient(token)
    space_cleared = 0

    first_page = client.api_call('files.list', ts_to=older_than_timestamp)
    files = first_page['files']

    event_loop = asyncio.get_event_loop()
    try:
        files += event_loop.run_until_complete(
            collect_files(client, older_than_timestamp, start_page=2, total_pages=first_page['paging']['pages'])
        )

        for file in files:
            space_cleared += event_loop.run_until_complete(
                delete_file(client, file)
            )
    finally:
        event_loop.close()

    num_files = len(files)
    click.echo(f'Deleted {num_files} files, saved {space_cleared / 1000000}Mb')


async def collect_files(client, older_than_timestamp, start_page=2, total_pages=2):
    all_files = []
    for page in range(start_page, total_pages+1):
        files = client.api_call('files.list', ts_to=older_than_timestamp, page=page)
        all_files += files['files']
    return all_files


async def delete_file(client, file):
    result = client.api_call('files.delete', file=file['id'])
    if result['ok']:
        click.echo(f'deleted file "{file["name"]}"')
        return file['size']
    else:
        click.echo(f'failed to delete file "{file["name"]}" because of "{result["error"]}"')
        return 0


if __name__ == '__main__':
    cli()
