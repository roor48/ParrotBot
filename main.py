import discord
from discord.ext import commands
 
cur_prefix = '$'

bot = commands.Bot(command_prefix=cur_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
 
@bot.event
async def on_message(message):
    if message.content[0] == cur_prefix and message.author != bot.user:
        await message.channel.send(message.content[1:])
 
bot.run('MTA1NjQ0NDA0MDgwMDg5NDk5Ng.GW_KpF.wZu6i4iqXLjXnZ4N7GaYQBneqEzyF97q_TMiLM')