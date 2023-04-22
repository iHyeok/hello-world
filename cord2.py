import discord

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

font = ImageFont.truetype("NotoSansKR-Medium.otf", 14)
font2 = ImageFont.truetype("NotoSansKR-Bold.otf", 18)

participants = ["리다이린",
            "재키",
            "아야",
            "피오라",
            "매그너스",
            "자히르",
            "나딘",
            "현우",
            "하트",
            "아이솔",
            "리다이린"]

CharList = ["리다이린",
            "재키",
            "아야",
            "피오라",
            "매그너스",
            "자히르",
            "나딘",
            "현우",
            "하트",
            "아이솔",
            "리다이린",
            "유키",
            "혜진",
            "쇼우",
            "키아라",
            "알렉스",
            "아디나"
            ]





SelectedChars = []

def coin_toss():
    """Simulates a coin toss, returning 'Heads' or 'Tails'."""
    return random.choice(['Heads', 'Tails'])

#1 = Team1 Ban
#2 = Team2 Ban
#3 = Team1 Pick
#4 = Team2 Pick

PBTEXT = [""
,"Team1 Ban"
,"Team2 Ban"
,"Team1 Pick"
,"Team2 Pick"
]
PBTEXT = [""
,"```css\n.Blue Ban\n```"
,"```diff\n-Red Ban\n```"
,"```css\n.Blue Pick\n```"
,"```diff\n-Red Pick\n```"
,"```픽밴이 완료 되었습니다```"
]
PBList = [2,1,1,2, 3,4,4,3, 2,1, 4,3,3,4,5]
PBOrderList = [9,10,11,12, 1,5,6,2, 13,14, 7,3,4,8]


def baseImgSetting():
    im = Image.open("sample/pickscreen.png")
    return im

def baseImgSetting2():
    im = Image.new("RGB", (380, 380), (255, 255, 255))
    blue_image = Image.new("RGB", (190, 40), (40, 150, 250))
    red_image = Image.new("RGB", (190, 40), (215, 20, 100))
    line = Image.new("RGB", (380, 70), (230, 230, 230))
    blank = Image.new("RGB", (2, 380), (0, 0, 0))

    im.paste(blue_image, (0, 0))
    im.paste(red_image, (190, 0))

    for i in range(6):
        if i % 2 == 1:
            im.paste(line, (0, 30+(i-1) * 70))

    im.paste(blank, (189, 0))  # 구분선

    # 이미지에 텍스트 추가
    d = ImageDraw.Draw(im)
    d.text((20, 3), "블루 팀", font=font2, fill=(0, 0, 0))
    d.text((220, 3), "레드 팀", font=font2, fill=(0, 0, 0))

    # 10, 320 밴밴
    # 340, 320 밴
    d.text((10, 320), "밴", font=font2, fill=(0, 0, 0))
    d.text((200, 320), "밴", font=font2, fill=(0, 0, 0))

    return im



# 간단한 메소드 추가
def getChampionImage(name):
    path = "./back_/"+name+".png"
    im = Image.open(path)
    return im.resize((47, 61))

def drawChar(im):
    d = ImageDraw.Draw(im)
    for i, data in zip(range(1, 15), participants):
        if data == "":
            continue
        if i < 5:
            im.paste(getChampionImage(data), (210, (i - 1) * 70 + 35))
            d.text((280, (i - 1) * 70 + 55), data, font=font, fill=(0, 0, 0))
        elif i < 9:
            im.paste(getChampionImage(data), (10, (i - 5) * 70 + 35))
            d.text((80, (i - 5) * 70 + 55), data, font=font, fill=(0, 0, 0))

        else: # 밴
            #정해진 6개의 포지션 좌표에
            ban_img_position = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),
                                 (35,315),(225,315),(275,315),(85,315),(135,315),(325,315),] #2,1,1,2,2,1,
            im.paste(getChampionImage(data), ban_img_position[i])


char_index = list()
CharList = []
with open(r'text/korChar.txt', encoding='utf8') as data:
    for text in data:
        char_index.append([text.rstrip('\n')])
        CharList.append(text.rstrip('\n'))


CharList.append("리 다이린")
# with open('text/engChar.txt', encoding='utf8') as data:
#     for idx, text in enumerate(data):
#         char_index[idx].append(text.rstrip('\n'))

import asyncio
import random

botAutoProgress = True

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global PBCount, participants, char_index, SelectedChars, botAutoProgress
        # don't respond to ourselves
        try:
            #print(message)
            #print(message.author)
            #if message.author == self.user:
            #    return

            if not '!' in message.content:
                return

            if message.content == '!명령어':
                await message.channel.send('명령어: [!CoinToss, !send_image, !픽밴 시작, !타이머 시간(초단위), !멈춰, !자동, !랜덤')

            if message.content == 'ping':
                await message.channel.send('pong')

            if message.content == '!멈춰':
                botAutoProgress = False
                await message.channel.send('제한 시간이 초과될 경우에도 다음 순서로 진행되지 않습니다')

            if message.content == '!자동':
                botAutoProgress = True
                await message.channel.send('제한 시간이 초과될 경우, 바로 다음 순서로 진행됩니다')

            if message.content == '!랜덤':
                randomChar = random.choice(CharList)
                while randomChar in SelectedChars:  # 중복이면 다시 돌림
                    randomChar = random.choice(CharList)

                if botAutoProgress:
                    await message.channel.send(f'!{randomChar}')
                else:
                    await message.channel.send(f'{randomChar}')

            # Check for the command to start the timer
            if message.content.startswith('!타이머'):
                # Get the time in seconds from the user's message
                self.Maxtime = int(message.content.split(' ')[1])
                self.Curtime = int(message.content.split(' ')[1])
                await message.channel.send(f'타이머가 {self.Maxtime}초로 설정되었습니다.')

            if message.content == '!CoinToss':
                result = coin_toss()
                #['Heads', 'Tails']
                imgPath = "Heads.png"
                if result == "Heads":
                    await message.channel.send(f"Toss: {result}")
                else:
                    imgPath = "Tails.png"
                    await message.channel.send(f"Toss: {result}")

                with BytesIO() as image_binary:
                    im = Image.open(imgPath)

                    # 이미지를 BytesIO 스트림에 저장
                    im.save(image_binary, "png")
                    # BytesIO 스트림의 0바이트(처음)로 이동
                    image_binary.seek(0)
                    # discord.File 인스턴스 생성
                    out = discord.File(fp=image_binary, filename="image.png")
                    await message.channel.send(file=out)

            if message.content.startswith('!send_image'):
                with BytesIO() as image_binary:
                    #im = Image.open("MonsterIcon_Wickline_01.png")
                    im = baseImgSetting()
                    drawChar(im)

                    # 이미지를 BytesIO 스트림에 저장
                    im.save(image_binary, "png")
                    # BytesIO 스트림의 0바이트(처음)로 이동
                    image_binary.seek(0)
                    # discord.File 인스턴스 생성
                    out = discord.File(fp=image_binary, filename="image.png")
                    await message.channel.send(file=out)

            if message.content == '!픽밴 시작':
                try:
                    if self.Maxtime:
                        self.Curtime = self.Maxtime
                    else:
                        self.Curtime = 30
                        self.Maxtime = 30
                except:
                        self.Curtime = 30
                        self.Maxtime = 30

                PBCount = 0
                participants = ["","","","","","","","","","","","","",""] #14
                SelectedChars = []
                await message.channel.send(PBTEXT[PBList[PBCount]])

                PBCount = PBCount + 1

                self.PBSelectedList = [False, False, False, False,
                  False, False, False, False,
                  False, False, False, False,
                  False, False, ]




                with BytesIO() as image_binary:
                    im = Image.open(f"sample/turn/TURN{PBCount}.png")

                    # 이미지를 BytesIO 스트림에 저장
                    im.save(image_binary, "png")
                    # BytesIO 스트림의 0바이트(처음)로 이동
                    image_binary.seek(0)
                    # discord.File 인스턴스 생성
                    out = discord.File(fp=image_binary, filename="image.png")
                    self.ProgressIMG = await message.channel.send(file=out)

                with BytesIO() as image_binary:
                    im = baseImgSetting()
                    drawChar(im)

                    # 이미지를 BytesIO 스트림에 저장
                    im.save(image_binary, "png")
                    # BytesIO 스트림의 0바이트(처음)로 이동
                    image_binary.seek(0)
                    # discord.File 인스턴스 생성
                    out = discord.File(fp=image_binary, filename="image.png")
                    self.PickIMG = await message.channel.send(file=out)

                # 타임 출력
                timer_message = await message.channel.send(
                    f'제한 시간 {self.Maxtime} 초. 남은 시간: {self.Maxtime} 초.')


                # Update remaining time dynamically
                PBTemp = PBCount
                for t in range(self.Maxtime-1, -2, -1):
                    if self.PBSelectedList[PBTemp - 1]:
                        break
                    await asyncio.sleep(1)
                    await timer_message.edit(
                        content=f'제한 시간 {self.Maxtime}초. 남은 시간: {t} 초.')
                    self.Curtime = t
                if self.Curtime <= 0:
                    await message.channel.send('선택 시간이 초과되었습니다')
                    randomChar = random.choice(CharList)
                    while randomChar in SelectedChars:  # 중복이면 다시 돌림
                        randomChar = random.choice(CharList)

                    await message.channel.send(f'!{randomChar}')

            if message.content.replace('!','') in CharList:
                selected_char = message.content.replace('!','')
                if PBCount > 14:
                    await message.channel.send(f"픽밴이 완료 되었습니다")

                elif selected_char in SelectedChars:
                    await message.channel.send(f"{selected_char}: 이미 등록된 실험체 입니다")
                else:
                    self.PBSelectedList[PBCount -1] = True
                    self.Curtime = self.Maxtime
                    SelectedChars.append(selected_char)
                    participants[PBOrderList[PBCount-1]-1] = selected_char
                    await message.channel.send(PBTEXT[PBList[PBCount]])
                    PBCount = PBCount + 1

                    with BytesIO() as image_binary:
                        im = Image.open(f"sample/turn/TURN{PBCount}.png")

                        # 이미지를 BytesIO 스트림에 저장
                        im.save(image_binary, "png")
                        # BytesIO 스트림의 0바이트(처음)로 이동
                        image_binary.seek(0)
                        # discord.File 인스턴스 생성
                        out = discord.File(fp=image_binary, filename="image.png")
                        await self.ProgressIMG.delete()
                        self.ProgressIMG = await message.channel.send(file=out)

                    with BytesIO() as image_binary:
                        # im = Image.open("MonsterIcon_Wickline_01.png")
                        im = baseImgSetting()
                        drawChar(im)

                        # 이미지를 BytesIO 스트림에 저장
                        im.save(image_binary, "png")
                        # BytesIO 스트림의 0바이트(처음)로 이동
                        image_binary.seek(0)
                        # discord.File 인스턴스 생성
                        out = discord.File(fp=image_binary, filename="image.png")
                        await self.PickIMG.delete()
                        self.PickIMG = await message.channel.send(file=out)

                    if PBCount <= 14:
                        # 타임 출력
                        timer_message = await message.channel.send(
                            f'제한 시간 {self.Maxtime} 초. 남은 시간: {self.Maxtime} 초.')

                        # Update remaining time dynamically
                        PBTemp = PBCount
                        for t in range(self.Maxtime-1, -2, -1):
                            if self.PBSelectedList[PBTemp-1]:
                                break
                            await asyncio.sleep(1)
                            await timer_message.edit(
                                content=f'제한 시간 {self.Maxtime}초. 남은 시간: {t} 초.')
                            self.Curtime = t
                        if self.Curtime <= 0:
                            await message.channel.send('선택 시간이 초과되었습니다')
                            randomChar = random.choice(CharList)
                            while randomChar in SelectedChars: # 중복이면 다시 돌림
                                randomChar = random.choice(CharList)

                            if botAutoProgress:
                                await message.channel.send(f'!{randomChar}')
                            else:
                                await message.channel.send(f'{randomChar}')

        except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            print('예외가 발생했습니다.', e)



intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run('MTA5NjAyNTg1MTI4OTY2OTc2NA.GfgozS.TFL2WDL2CeLIQR3wBRw_eXvA-f3ktsPcQKN4PM')

# import discord
# from discord.ext import commands
#
# # Define intents
# intents = discord.Intents.default()
# intents.messages = True  # Enable the messages intent
#
# # Create a bot instance with intents
# bot = commands.Bot(command_prefix='!', intents=intents)
#
# # Event: Bot is ready
# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user.name}')
#
# # Command: !hello
# @bot.command()
# async def hello(ctx):
#     await ctx.send('Hello, I am your Discord bot!')
#
# # Command: !ping
# @bot.command()
# async def ping(ctx):
#     await ctx.send('Pong!')
#
# # Run the bot
# bot.run('MTA5NjAyNTg1MTI4OTY2OTc2NA.GfgozS.TFL2WDL2CeLIQR3wBRw_eXvA-f3ktsPcQKN4PM')  # Replace with your bot token

#client.run('MTA5NjAyNTg1MTI4OTY2OTc2NA.GfgozS.TFL2WDL2CeLIQR3wBRw_eXvA-f3ktsPcQKN4PM')