# Slack Admin CLI

[![](https://badge.fury.io/py/slack-admin.png)](http://badge.fury.io/py/slack-admin)

[![](https://travis-ci.org/littlepea/slack-admin.png?branch=master)](https://travis-ci.org/littlepea/slack-admin)


## Features

* Clean-up old attachment files in your Slack account to free up space.

## Usage

Install from pypi:

```
$ pip install slack-admin
```

Configure the access credentials:

```
$ ...
```

Read the help:

```
$ slack-admin --help
Usage: slack-admin [OPTIONS] COMMAND [ARGS]...

  Slack admin CLI

Options:
  --help  Show this message and exit.

Commands:
  cleanup  Cleans up old file attachments from Slack
```

Example - delete all files older than 5 months old and bigger than 500Kb:
  
```
$ slack-admin cleanup --older "5 month ago" --bigger 500K

Going to delete all files older than 5 month ago and bigger than 500K
4 will be deleted
Do you agree? [y/n]y
deleted file 1 of 4: "Screenshot_20161005-092952.png"
deleted file 2 of 4: "Pasted image at 2016_09_30 11_33 AM.png"
deleted file 3 of 4: "targetprocess-screen-capture (4).png"
deleted file 4 of 4: "Testing site.png"
Deleted 4 files, saved 2.82802Mb
```