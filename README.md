# HateDetector

Built By @jcarterbohan, @himshikha21 and @shraddha1803

## Requirements
Compatible with Python 3.4-3.6
Use `requirements.txt` to get the required libraries

## How to install

Copy the repo by using the git command:
```git clone https://github.com/jcarterbohan/HateDetector.git```


## How to use HateRater


```py
from haterater import HateRater

#Exapmle use of HateRater
rating = HateRater("Hello John!")

#Example of use if you want a graph as well
rating = HateRater("Hello John!", True)
```

## How to use the Discord Bot

First go to https://discord.com/developers/ and create a new application.
Then go to the bot section and get the token from the page.

In `config.json`, for the id object, replace it with the token that you obtained.

Finally run `bot.py` from the command line



