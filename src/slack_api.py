from slack_sdk import WebClient

class slack_api:
    def __init__(self, token):
        self.client = WebClient(token)
        
    def get_channel_id(self, channel_name):
        result = self.client.conversations_list()
        channels = result.data['channels']
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        channel_id = channel["id"]
        return channel_id

    def post_thread(self, channel_id, text):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text = text,
        )
        return result
