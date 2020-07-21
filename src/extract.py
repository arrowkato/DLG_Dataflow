import requests
import json


class Extract:
    def __init__(self, token="default"):
        # 特に指定がない場合は、defaultのtokenを使う:
        if token == "default":
            path = './slack_token.txt'
            with open(path) as f:
                token = f.read()

        self.token = token
        # self.channel_id = channel_id

        self.urls = {}
        self.urls["conversations_list"] = "https://slack.com/api/conversations.list"
        self.urls["users_list"] = "https://slack.com/api/users.list"

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
            #print(message["text"])

        return list



if __name__ == '__main__':
    extract = Extract()
    #extract.list_channel_id()
    #extract.list_users()

    #extract.receive_message("C0134918QAE")
    extract.list_message("C0134918QAE")

