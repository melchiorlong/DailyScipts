# 导入模块
import itchat
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot()



zjy = bot.search('zjy')[0]

bot.messages.search(Nickname='小泥巴儿')

# 打印共同好友
for mf in mutual_friends(bot, bot2):
    print(mf)