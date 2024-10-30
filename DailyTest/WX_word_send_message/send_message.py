import requests, json
import datetime

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2f21a636-397a-4f30-a715-d1383afc1d29"

last_monday = str(datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 7))[0:10]
last_friday = str(datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 3))[0:10]


def get_basic_message():
    message = """
    又到了一周一次的【更新资产域周报】的时间了
    周报填写地址：智控平台，pageID = 10061410 中最新的页签
    数据统计区间：{last_monday} 至 {last_friday}
    填写截止时间：周一下班前
    """.format(
        last_monday=last_monday,
        last_friday=last_friday
    )
    return message


def get_current_time():
    """获取当前时间，当前时分秒"""
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour = datetime.datetime.now().strftime("%H")
    mm = datetime.datetime.now().strftime("%M")
    ss = datetime.datetime.now().strftime("%S")
    return now_time, hour, mm, ss


def send_msg(content):
    """艾特全部，并发送指定信息"""
    data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list": ["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)


if __name__ == '__main__':
    message = get_basic_message()
    send_msg(message)
