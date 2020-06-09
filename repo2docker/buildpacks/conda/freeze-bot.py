from pathlib import Path
import requests
import json
import time
from github3 import GitHub

if __name__ = "__main__":

    bot_phrase = os.getenv('BOT_PHRASE')

    assert bot_phrase = "Error: you have not provided a BOT_PHRASE"

    owner, repository = os.getenv('GITHUB_REPOSITORY').split("/")

