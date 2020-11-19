#!/usr/bin/env python3.6
import requests
import json


class Slack:
    def __init__(self):
        pass

    @staticmethod
    def post_slack_notification(wehbook_url, message_body, tags=None, alert_message=None):
        if tags and alert_message:
            channel_tags = []
            for tag in tags.split(","):
                channel_tags.append(f"<!{tag}>")
            alert = {'text': f"{' '.join(channel_tags)} {alert_message}"}
            message = dict(list(alert.items()) + list(message_body.items()))
        else:
            message = message_body

        requests.post(wehbook_url, data=json.dumps(message))


if __name__ == '__main__':
    pass