import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from pars import get_skin_info
from tokenbot import get_token


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Убедитесь, что токен правильно назван в .env файле

intents = discord.Intents.default()
intents.message_content = True  # Включение message_content intents

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def getskins(ctx, url: str):
    extension_path = r"C:\Users\valer\Downloads\JJICBEFPEMNPHINCCGIKPDAAGJEBBNHG_4_2_6_0.crx"
    await ctx.send('Starting to fetch skin data...')
    csv_filename = get_skin_info(url, extension_path)
    if csv_filename:
        await ctx.send(file=discord.File(csv_filename))
    else:
        await ctx.send('An error occurred while processing the skins.')

bot.run(get_token(1))

