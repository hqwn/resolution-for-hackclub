from logging import Logger
from slack_sdk import WebClient
import logging

logger = logging.getLogger(__name__)

def member_joined_channel_callback(event: dict, client: WebClient, logger: Logger):
    try:

        user_id = event["user"]
        user_info = client.users_info(user=user_id)
        name = user_info["user"]['real_name']

        blocks = [
           
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Welcome User: {name}!"
			}
		}
	]


        client.chat_postMessage(
            channel=event["channel"],
            blocks=blocks,
            text="Welcome!"  
        )

    except Exception as e:
        logger.error(e)