import discord
from discord.ext import commands
 
cur_prefix = '$'

bot = commands.Bot(command_prefix=cur_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')

@bot.event
async def on_command_error(message, error):
    await message.send("명령어도 똑바로 입력 못하냐??")


@bot.command()
async def 앵무새(message, text):
    await message.channel.send(text)

# @bot.command()
# async def prefix(message, *, text):
#     global cur_prefix
#     global bot
#     cur_prefix = text
#     bot = commands.Bot(command_prefix=cur_prefix, intents=discord.Intents.all())
#     await message.channel.send(f"명령어 시작은 {text}로 해라")

bot.run('MTA1NjQ0NDA0MDgwMDg5NDk5Ng.GW_KpF.wZu6i4iqXLjXnZ4N7GaYQBneqEzyF97q_TMiLM')