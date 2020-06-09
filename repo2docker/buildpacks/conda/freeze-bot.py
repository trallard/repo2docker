import json
import os

if __name__ == "__main__":

    bot_phrase = os.getenv("BOT_PHRASE")
    assert bot_phrase, "Error: you have not provided a BOT_PHRASE"

    owner, repository = os.getenv("GITHUB_REPOSITORY").split("/")

    # load the event payload to check details

    event_payload = json.load("GITHUB_EVENT_PATH")

    comment_text = event_payload["comment"]
    issue_data = event_payload["issue"]

    trigger_action = False

    if bot_phrase in comment_text["body"] and "pull_request" in issue_data:
        trigger_action = True

        print("Trigger phrase detected -- triggering refreeze")

    print(f"::set-output name=PULL_REQUEST_NUMBER::{issue_data['number']}")
    print(f"::set-output name=TRIGGER_ACTION::{trigger_action}")
