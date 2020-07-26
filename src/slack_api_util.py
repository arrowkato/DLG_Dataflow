import requests
import json
from slack import WebClient
from slack.errors import SlackApiError

class SlackAPIUtil:
    def __init__(self, token_path="./slack_token.txt"):
        # 特に指定がない場合は、defaultのtokenを使う:
        with open(token_path) as f:
            token = f.read()

        self.token = token

        self.urls = {"conversations_list": "https://slack.com/api/conversations.list",
                     "users_list": "https://slack.com/api/users.list"}
        # slackのライブラリ用
        self.slack_client = WebClient(token=token)

    def list_channel_id(self):
        """
        tokenで設定しているチャンネルの一覧表示
        :return: なし
        """

        payload = {
            "token": self.token,
        }
        response = requests.get(self.urls["conversations_list"], params=payload)
        output = response.json()
        channels = output["channels"]
        for channel_info in channels:
            print(channel_info["id"] + " : " + channel_info["name"])

    def list_users(self):
        """
        ユーザ一覧を表示する
        :return: ユーザの一覧
        """
        payload = {
            "token": self.token,
        }
        response = requests.get(self.urls["users_list"], params=payload)
        json_response = response.json()
        # 整形
        output = json.dumps(json_response, indent=4)
        print(output)

    def list_message(self, channel_id):
        '''
        channel_idで指定したチャンネルのメッセージを表示
        :param token: DLGのSlackのAPI Token
        :param channel_id: channelのid get_DLG_slack_token()で取得可能
        :return: None
        '''
        messages = self.receive_message(channel_id)

        for message in messages:
            print(message)

    def receive_message(self, channel_id):
        '''
        channel_idで指定したチャンネルのメッセージを表示
        :param token: DLGのSlackのAPI Token
        :param channel_id: channelのid get_DLG_slack_token()で取得可能
        :return: None
        '''
        payload = {
            "token": self.token,
            "channel": channel_id
        }
        url = "https://slack.com/api/channels.history"
        response = requests.get(url, params=payload)

        json_data = response.json()

        messages = json_data["messages"]
        list = []
        for message in messages:
            list.append(message["text"])

        return list

    def send_message(self, channel_name, message_body):

        try:
            response = self.slack_client.chat_postMessage(
                channel=channel_name,
                text=message_body)
            assert response["message"]["text"] == message_body
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")






if __name__ == '__main__':
    spu = SlackAPIUtil()
    # とあるチャンネルのメッセージを取得
    # spu.list_message("C0134918QAE")

    # とあるチャンネルにメッセージを送る
    #spu.list_message("C0134918QAE")
    #spu.list_channel_id()
    #slack_token = os.getenv("")

    spu.send_message("#07-01-データパイプライン講座執筆", "でぃすいいずてすとめっせーじ :fire:")



