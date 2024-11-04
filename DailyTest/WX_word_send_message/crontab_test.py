import requests, json
import datetime

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=252978a3-7e82-4fce-93d8-e8be66035b9b"

last_monday = str(datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 7))[0:10]
last_friday = str(datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 3))[0:10]


def get_basic_message():
    message = """
    又到了一周一次的<font color=\"info\">更新资产域周报</font>的时间了
    >周报填写地址：智控平台，pageID = 10061410 中最新的页签
    >数据统计区间：{last_monday} 至 {last_friday}
    >填写截止时间：<font color=\"warning\">周一下班前</font>""".format(
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
    data = json.dumps({"msgtype": "markdown", "markdown": {"content": content, "mentioned_list": ["@all"]}})
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)


if __name__ == '__main__':
    message = get_basic_message()
    send_msg(message)
