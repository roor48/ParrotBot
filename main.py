import discord
from discord.ext import commands
 
cur_prefix = '#'

bot = commands.Bot(command_prefix=cur_prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')
 
@bot.command()
async def hello(message):
    await message.channel.send('Hi!')
 
bot.run('MTA1NjQ0NDA0MDgwMDg5NDk5Ng.GW_KpF.wZu6i4iqXLjXnZ4N7GaYQBneqEzyF97q_TMiLM')