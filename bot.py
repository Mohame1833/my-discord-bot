import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

# استبدل 'YOUR_BOT_TOKEN' بتوكن البوت بتاعك
bot.run('MTM2MDQxODMzOTc4NDIzMjk2MA.GYpjU7.BaoloGut9fgUVAag-mpgL4IvX0wKR-jW0M0IAw')
