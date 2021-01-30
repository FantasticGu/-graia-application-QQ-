from graia.broadcast import Broadcast
from graia.application.entry import (
    GraiaMiraiApplication, Group, Friend, Member, MessageChain, Plain, At, Session, Image)
from spider import (translate, getImgByPid, getImgBySearch)
import asyncio
import re
import random


loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080",  # httpapi 服务运行的地址
        authKey="initAuthKey",  # authKey
        account=12345678,  # 机器人的 qq 号
        websocket=True
    ))

lucky_num = {}


@bcc.receiver("GroupMessage")
async def group_message_translate(app: GraiaMiraiApplication, group: Group, msg: MessageChain, sender: Member):
    Text = msg.get(Plain)[0].text
    firstText = Text.split(' ')[0]
    if (firstText == "翻译" or firstText == "translate"):

        if Text.split(' ')[1][0] == '/':
            deslan = re.search(r'/[A-Za-z\_]*', Text).group(0)[1:]
            originText = re.split(r'/[A-Za-z\_]* ', Text)[1]
            sendMsg = translate(originText, 1, deslan)

        else:
            sendMsg = translate(Text[Text.find(' ') + 1:])

        await app.sendGroupMessage(group, MessageChain.create([Plain(sendMsg)]))

    elif (Text == "今日人品"):
        if lucky_num.get(sender.id) == None:
            lucky_num[sender.id] = random.randint(0, 100)
        await app.sendGroupMessage(group, MessageChain.create([At(sender.id), Plain("今天的人品是" + str(lucky_num[sender.id]) + '~')]))

    elif (firstText == "pid"):
        pid = Text.split(' ')[1]
        nums = getImgByPid(pid)

        if (nums > 0):
            for i in range(0, nums):
                await app.sendGroupMessage(group, MessageChain.create([Image.fromLocalFile('tmp_' + str(i) + '.jpg')]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([Plain('获取图片失败，请检查PID是否有误')]))

    elif (firstText == "搜索"):
        searchText = Text.split(' ')[1]
        pids = getImgBySearch(searchText)
        try:
            for i in range(0, len(pids)):
                await app.sendGroupMessage(group, MessageChain.create([Plain(pids[i]), Image.fromLocalFile('tmp_' + str(i) + '.jpg')]))
        except:
            await app.sendGroupMessage(group, MessageChain.create([Plain('搜索失败')]))

app.launch_blocking()
