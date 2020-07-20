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
        response = requests.get(self.urls["users_list"], params=payload)
        json_response = response.json()
        # 整形
        output = json.dumps(json_response, indent=4)
        print(output)


if __name__ == '__main__':
    extract = Extract()
    # extract.list_channel_id()
    extract.list_users()
