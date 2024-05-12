# To Do List
# 엑셀 파일로 저장된거 json으로 바꾸기

import json
import pandas as pd
import requests
import time
import discord
from discord.ext import commands

# Never Using Prefix
cur_prefix = 'dsajfl;adsjfl;'

commendList = ["가입", "신고", "배워", "잊어", "따라해", "핑", "급식", "조식", "중식", "석식", "프사"]
adminIdList = [468316922052608000, 451664773939986434]

bot = commands.Bot(command_prefix=cur_prefix, intents=discord.Intents.all())

discordApi = "https://discord.com/api/users/"
BOT_KEY = "MTA1NjQ0NDA0MDgwMDg5NDk5Ng.GW_KpF.wZu6i4iqXLjXnZ4N7GaYQBneqEzyF97q_TMiLM"
header = {"Authorization": "Bot " + BOT_KEY}

SC_CodeDict = {"서울": "B10", "부산": "C10", "대구": "D10", "인천": "E10", "광주": "F10",
               "대전": "G10", "울산": "H10", "세종": "I10",
               "경기도": "J10", "강원도": "K10", "충청북도": "M10", "충청남도": "N10",
               "전라북도": "P10", "전라남도": "Q10", "경상북도": "R10", "경상남도": "S10",
               "제주도": "T10"}
neisApi = 'https://open.neis.go.kr/hub/'
neisKey = '7add51844cc841ff8226457e938b6094'

commandData = pd.read_csv('./MyBotData.csv').values.tolist()
commandDict = {}
for i in commandData:
    commandDict[i[0]] = [i[1], i[2]]

with open("./Users.json", 'r') as json_file:
    users = json.load(json_file)
    if not "reports" in users:
        users["reports"] = {}


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
    if message.author.bot:
        return

    if "무새야 데이터 저장" == message.content:
        if message.author.id in adminIdList:
            SaveDatas()
            await message.channel.send("데이터를 저장했어요!")
        else:
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
        elif "안녕" in message.content:
            await message.channel.send("안녕")


async def MuseYa(message, text):
    global commandDict
    global users

    print(message.author.global_name, text)
    if "가입" == text:
        if str(message.author.id) in users["reports"]:
            await message.channel.send("이미 가입 되어있어요!")
        else:
            users["reports"][str(message.author.id)] = 0
            await message.channel.send("가입 완료!")
        return
    
    if text[:3] == "명령어":
        await message.channel.send("무새가 아는 명령어들:\n중괄호({}) 안은 선택입니다!\n"
                                   "\n__앵무새한테 가르치기__\n\n"
                                   "`무새야 배워 <가르칠 말> <내용>` - 가르칠 말과 내용은 공백없이 입력 해주세요!\n"
                                   "`무새야 잊어 <잊을 말>` - 사용자가 입력한 단어를 잊습니다!\n"
                                   "`무새야 <가르친 말>`\n"
                                   "`무새야 신고 <가르친 말>`\n"
                                   "`무새야 따라해 <따라할 말>`\n"
                                   "\n__무새가 찾아주는 급식표~__\n\n"
                                   "`무새야 <급식|조식|중식|석식> <지역> <학교> {날짜}`\n"
                                   "지역 형식 : [서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종, 경기도, 강원도, 충청북도, 충청남도, 전라북도, 전라남도, 경상북도, 경상남도, 제주도]}\n"
                                   "학교 형식 : 이름 첫 글자 딴 줄임말 금지(예 : 배정고등학교 -> 배정고 = O, 배정미래고등학교 -> 배미고 = X, 배정미래고등학교 -> 미래고 = O\n"
                                   "날짜 형식 : yyyymmdd (예 : 20061130)\n"
                                   "\n__기타__\n\n"
                                   "`무새야 핑` - 퐁!\n"
                                   "`무새야 프사 <맨션|사용자 id>` - 사용자의 프로필 사진을 불러옵니다.")
        return

    if not str(message.author.id) in users["reports"]:
        await message.channel.send("아직 가입을 안하셨네요!\n`무새야 가입`을 입력해주세요")
        return

    if text[:4] == "다 잊어":
        if message.author.id in adminIdList:
            commandDict = {}
            users = {"reports": {}}
            await message.channel.send("헤헤.. 다 까먹어버렸당")
        else:
            await message.channel.send("넌 관리자가 아니잖아!")
        return

    if text[:3] == "배워 ":
        await LearnWord(message, text[3:])
        return
    if text[:3] == "잊어 ":
        await ForgetWord(message, text[3:])
        return
    if text[:3] == "신고 ":
        await ReportWord(message, text[3:])
        return
    if text[:4] == "따라해 ":
        await message.channel.send(text[4:])
        return
    if text[:3] in ["급식 ", "조식 ", "중식 ", "석식 "]:
        if text[0] == '급':
            text = list(text)
            text[0] = '중'
            text = ''.join(text)
        await TodayMeal(message, text[3:], text[:2])
        return
    if text[:1] == "핑":
        await message.channel.send("퐁!")
        return
    if text[:3] == "프사 ":
        await ProfilePicture(message, text[3:])
        return

    await SayWord(message, text)


async def ReportWord(message, text):
    text = text.replace(" ", "")
    if not text in commandDict:
        await message.channel.send("어... 그 단어는 내 기억에 없는디")
        return

    users["reports"][str(commandDict[text][1])] += 1
    await message.channel.send("메세지 신고 완료!\n`허위 신고는 안돼잉`")


async def LearnWord(message, text):
    if text.count(' ') != 1:
        await message.channel.send("공백을 잘 확인해주길~")
        return

    text = text.split(' ')
    if (text[0] in commendList):
        await message.channel.send(f"{text[0]}는 다른 명령어로 지정되었기 때문에 가르칠 수 없어~")
        return
    
    if len(text[0]) > 10:
        await message.channel.send("그렇게 큰 건 내 뇌에 다 안 들어온다고옷~♡\n`가르칠 말을 10글자 이내로 작성해주세요`")
        return
    if len(text[1]) > 100:
        await message.channel.send("그렇게 큰 건 내 뇌에 다 안 들어온다고옷~♡\n`내용을 100글자 이내로 작성해주세요`")
        return

    if text[0] in commandDict:
        await message.channel.send(f"{text[0]}은 이미 알고 있다구!")
        return

    commandDict[text[0]] = [text[1], str(message.author.id)]
    await message.channel.send(f"`{text[0]}`이라고 하면 `{text[1]}`이라고 하면 되는거구나!")


async def ForgetWord(message, text):
    if not message.author.id in adminIdList:
        return
    text = text.replace(" ", "")
    if text in commandDict:
        del commandDict[text]
        await message.channel.send(f"어라? {text}가 뭐였는지 기억이 안나...")
    else:
        await message.channel.send(f"어라? 나는 {text}라는 말을 모르는데?")


async def SayWord(message, text):
    text = text.replace(" ", "")

    if text in commendList:
        await message.channel.send(f"명령어 형식을 확인해주세용~♥")
        return

    if text in commandDict:
        r = requests.get(
            discordApi + str(commandDict[text][1]), headers=header)
        while r.status_code == 429:
            time.sleep(r.json()['retry_after'])
            r = requests.get(
                discordApi + str(commandDict[text][1]), headers=header)
        r = r.json()['global_name']
        await message.channel.send(f"{commandDict[text][0]}\n`{r}님이 가르쳐 주셨어요!`")
        return

    await message.channel.send(f"{text}(이)라는 단어를 모르는거 같아..")


async def TodayMeal(message, text, foodType):
    text = text.split()
    if len(text) == 2:
        text.append(time.strftime('%Y%m%d'))
    elif len(text) == 3:
        try:
            int(text[2])
            if len(text[2]) != 8:
                raise Exception
        except:
            await message.channel.send("날짜 형식은 `yyyymmdd`입니다!")
            return
    else:
        await message.channel.send("공백을 확인해주세요!\n`무새야 급식 (지역명) (학교명) {날짜}`")
        return

    if not text[0] in SC_CodeDict:
        await message.channel.send("지역 이름을 확인해 줘!")
        return

    text[0] = SC_CodeDict[text[0]]
    school_Code = requests.get(neisApi+f"schoolInfo?KEY={neisKey}&Type=json&SCHUL_NM={text[1]}&ATPT_OFCDC_SC_CODE={text[0]}").json()
    if "RESULT" in school_Code:
        await message.channel.send("학교 이름을 확인해 줘! (풀네임으로)")
        return


    if (len(school_Code["schoolInfo"][1]["row"]) > 1):
        _schoolName = ""
        for i in school_Code["schoolInfo"][1]["row"]:
            _schoolName += i["SCHUL_NM"] + ", "
        await message.channel.send(f"겹치는 학교가 있는것 같아~ `{_schoolName[:-2]}`")
        return
    school_Code = school_Code["schoolInfo"][1]["row"][0]["SD_SCHUL_CODE"]

    mealData = requests.get(neisApi+f"mealServiceDietInfo?KEY={neisKey}&Type=json&ATPT_OFCDC_SC_CODE={text[0]}&SD_SCHUL_CODE={school_Code}&MLSV_YMD={text[2]}").json()
    if "RESULT" in mealData:
        await message.channel.send(f"{text[2][:4]}-{text[2][4:6]}-{text[2][6:8]}일은 밥 없는 날~")
        return

    hasLunch = False

    mealData = mealData["mealServiceDietInfo"][1]["row"]
    for i in range(len(mealData)):
        if mealData[i]["MMEAL_SC_NM"] == foodType:
            hasLunch = True
            mealData = mealData[i]["DDISH_NM"].replace('<br/>', '')
            break
    if not hasLunch:
        await message.channel.send(f"{text[2][:4]}-{text[2][4:6]}-{text[2][6:8]}일은 {foodType}이 없는데?")
        return

    # mealData = mealData["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"].replace('<br/>', '')

    todayMeal = ""
    isNotPlus = False
    for i in mealData:
        if i == "(":
            isNotPlus = True
        elif i == ")":
            isNotPlus = False
            continue
        if isNotPlus:
            continue
        todayMeal += i
    todayMeal = " ".join(todayMeal.split()).replace(' ', '\n')
    await message.channel.send(f"`{text[2][:4]}-{text[2][4:6]}-{text[2][6:8]}일 {foodType}`\n```{todayMeal}```")
    return

async def ProfilePicture(message, text):
    if (text[:2] != '<@' or text[-1] != '>') and not str.isdigit(text):
        await message.channel.send("사용자를 멘션해주세요!")
        return
    
    if not str.isdigit(text):
        text = text[2:-1]
    
    r = requests.get(
        discordApi + text, headers=header)
    if r.status_code == 404:
        await message.channel.send("알 수 없는 사용자입니다.")
        return
    while r.status_code == 429:
        time.sleep(r.json()['retry_after'])
        r = requests.get(
            discordApi + text, headers=header)
    r = r.json()['avatar']
    await message.channel.send(f'https://cdn.discordapp.com/avatars/{text}/{r}.png?size=4096')

def SaveDatas():
    lastDatas = []
    print("명령어 저장 중...")
    for i in commandDict.keys():
        lastDatas.append([i, commandDict[i][0], str(commandDict[i][1])])

    lastDatas = pd.DataFrame.from_records(lastDatas)
    lastDatas.to_csv(
        "./MyBotData.csv", index=False)
    print("명령어 저장 완료")

    print("유저 저장 중...")
    with open("./Users.json", 'w') as json_file:
        json.dump(users, json_file, ensure_ascii=False)

    print("유저 저장 완료")


bot.run(BOT_KEY)
