# To Do List
# 엑셀 파일로 저장된거 json으로 바꾸기


import json
import pandas as pd
import discord
from discord.ext import commands
 
# Never Using Prefix
cur_prefix = 'dsajfl;adsjfl;'

commendList = ["가입", "신고", "배워", "잊어", "따라해"]

bot = commands.Bot(command_prefix=cur_prefix, intents=discord.Intents.all())

commandData = pd.read_excel('C:/GitHub/Python/DiscordBot_RepeatBot/MyBotData.xlsx').values.tolist()
commandDict = {}
for i in commandData:
    commandDict[i[0]] = [i[1], i[2], i[3]]
print(commandDict)

with open("C:/GitHub/Python/DiscordBot_RepeatBot/Users.json", 'r') as json_file:
    users = json.load(json_file)
print(users)

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
    return

@bot.event
# 명령어 입력 에러
async def on_command_error(message, error):
    await message.send("명령어도 똑바로 입력 못하냐??")
    print(error)
    return

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if "무새야 데이터 저장" == message.content:
        if message.author.id == 468316922052608000:
            SaveDatas()
            await message.channel.send("데이터를 저장했어요!")
        elif message.author.id != 468316922052608000:
            await message.channel.send("넌 관리자가 아니잖아!")
        return

    if "무새야 " == message.content[:4]:
        await MuseYa(message, message.content[4:])
        return



    if str(message.author.id) in users["reports"]:
        if "잘자" in message.content:
            await message.channel.send(f"{message.author.mention}님! 잘자요~")
        elif "욕" == message.content:
            await message.channel.send(f"{message.author.mention}님! 욕은 하지말아요~♡")


async def Register(message):
    await message.channel.send("아직 가입을 안하셨네요!\n`무새야 가입`을 입력해주세요")
    return

async def MuseYa(message, text):
    if "가입" == text:
        if str(message.author.id) in users["reports"]:
            await message.channel.send("이미 가입 되어있어요!")
        else:
            users["reports"][str(message.author.id)] = 0
            await message.channel.send("가입 완료!")
        return
    
    if not str(message.author.id) in users["reports"]:
        await Register(message)
        return
    
    if text[:3] ==  "신고 ":
        await ReportWord(message, text[3:])
        return
    if text[:3] == "배워 ":
        await LearnWord(message, text[3:])
        return
    if text[:3] == "잊어 ":
        await ForgetWord(message, text[3:])
        return
    if text[:4] == "따라해 ":
        await message.channel.send(text[4:])
        return
    if text[:4] == "명령어":
        await message.channel.send("```무새야 ~~\n배워 {가르칠 말} {내용} ( {}안은 공백 없이 )\n잊어 {가르친 말}\n{가르친 말}```")

    await SayWord(message, text)


async def ReportWord(message, text):
    text = text.replace(" ", "")
    if not text in commandDict:
        await message.channel.send("어... 그 단어는 내 기억에 없는디")
        return
    
    users["reports"][str(commandDict[text][2])] += 1
    await message.channel.send("메세지 신고 완료!\n`허위 신고는 안돼`")


async def LearnWord(message, text):
    if text.count(' ') != 1:
        await message.channel.send("공백을 잘 확인해주길~")
        return

    text = text.split(' ')
    if len(text[0]) > 10:
        await message.channel.send("그렇게 큰 건 내 뇌에 다 안 들어온다고옷~♡\n`가르칠 말을 10글자 이내로 작성해주세요`")
        return
    if len(text[1]) > 100:
        await message.channel.send("그렇게 큰 건 내 뇌에 다 안 들어온다고옷~♡\n`내용을 100글자 이내로 작성해주세요`")
        return

    if text[0] in commandDict:
        await message.channel.send(f"{text[0]}은 이미 알고 있다구!")
        return

    commandDict[text[0]] = [text[1], message.author, str(message.author.id)]
    await message.channel.send(f"{text[0]}이라고 하면 {text[1]}이라고 하면 되는거구나!")


async def ForgetWord(message, text):
    text = text.replace(" ", "")
    if text in commandDict:
        del commandDict[text]
        await message.channel.send(f"어라? {text}가 뭐였는지 기억이 안나...")
    else:
        await message.channel.send(f"어라? 나는 {text}라는 말을 모르는데?")



async def SayWord(message, text):
    text = text.replace(" ", "")
    
    if text in commendList:
        await message.channel.send(f"{text}는 다른 명령어로 지정되었기 때문에 가르칠 수 없어~")
    elif text in commandDict:
        await message.channel.send(f"{commandDict[text][0]}\n`{commandDict[text][1]}님이 가르쳐 주셨어요!`")
    else:
        await message.channel.send(f"{text}라는 단어를 모르는거 같아..")


def SaveDatas():
    lastDatas = []
    print("명령어 저장 중...")
    for i in commandDict.keys():
        lastDatas.append([i, commandDict[i][0], str(commandDict[i][1]), commandDict[i][2]])

    lastDatas = pd.DataFrame.from_records(lastDatas)
    lastDatas.to_excel("C:/GitHub/Python/DiscordBot_RepeatBot/MyBotData.xlsx", index=False)
    print("명령어 저장 완료")

    print("유저 저장 중...")
    with open("C:/GitHub/Python/DiscordBot_RepeatBot/Users.json", 'w') as json_file:
        json.dump(users, json_file)

    print("유저 저장 완료")

bot.run('MTA1NjQ0NDA0MDgwMDg5NDk5Ng.GW_KpF.wZu6i4iqXLjXnZ4N7GaYQBneqEzyF97q_TMiLM')