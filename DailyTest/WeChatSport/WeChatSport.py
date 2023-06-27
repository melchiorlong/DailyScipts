# -*- coding: utf8 -*-
import requests
import json
user = input("请输入账号:")
passwd = input("请输入密码:")
end = input("请输入要刷取的步数:")
url = "https://api.kit9.cn/api/xiaomi_sports/api.php?mobile="+user+"&password="+passwd+"&step="+end
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent': ua.random}
req = requests.get(url=url,headers=headers).json()
code = req["code"]
if code == 200:
    print("提交成功",)
    print("提交步数为:",end)
elif code == 207:
    print("提交失败")
    print("登录失败，可能是账号或密码错误")
elif code == -1:
    print("60秒内只允许提交1次")