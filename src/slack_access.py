import requests



def show_message(token, channel_id):
    '''
    channel_idで指定したチャンネルのメッセージを表示
    :param token: DLGのSlackのAPI Token
    :param channel_id: channelのid get_DLG_slack_token()で取得可能
    :return: None
    '''
    payload = {
        "token": token,
        "channel": channel_id
    }
    url = "https://slack.com/api/channels.history"
    response = requests.get(url, params=payload)

    json_data = response.json()
    messages = json_data["messages"]
    for i in messages:
        print(i["text"])


def get_dlg_slack_token():
    '''
    DLGのAPIトークンを取得。Gitから直接見えるのはよろしくないので、./slack_token.txtに保存している
    :return: tokenを文字列で返す
    '''
    path = './slack_token.txt'
    with open(path) as f:
        token = f.read()

    return token


def show_dlg_channel_list():
    '''
    DLGのSlackのチャネル一覧を表示
    :return: None
    '''
    token = get_dlg_slack_token()

    fetch_all_channels_url = "https://slack.com/api/conversations.list"

    payload = {
        "token": token,
    }
    response = requests.get(fetch_all_channels_url, params=payload)
    output = response.json()
    channels = output["channels"]
    for channel_info in channels:
        print(channel_info["id"] + " : " + channel_info["name"])


if __name__ == '__main__':
    token = get_dlg_slack_token()
    #show_dlg_channel_list()

    # CNKV8CVN0 : 07-01-データパイプライン講座執筆
    show_message(token, "CNKV8CVN0")

