import discord
import apiToken
import requests
import json
import cubeCount
from discord.ext.commands import Bot


############# 디코 봇 코드 ################
intents = discord.Intents.all()
# /명령어
bot = Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
  print("시스템 가동")

############# 명령어 #####################
@bot.command()
async def test(ctx):
    print("test")
    await ctx.reply('test good')

@bot.command()
async def 토큰(ctx,name,*,token):
    apiToken.key[name] = token
    print(apiToken.key)
    await ctx.reply('추가 됐나? 한번해보셈')
    
@bot.command()
async def 큐브(ctx,name,*,target_item):
    await ctx.reply('시간이 다소 걸립니다\n결과가 나오기 전 까지 기다려 주세요.')
    result = cubeCount.maple_API(name,target_item)
    embed = discord.Embed(title="큐브 사용 내역",color=0xFF0000)
    embed.add_field(name="장인의 큐브", value=result[0], inline=False)
    embed.add_field(name="명장의 큐브", value=result[1], inline=False)
    embed.add_field(name="레드 큐브", value=result[2], inline=False)
    embed.add_field(name="블랙 큐브", value=result[3], inline=False)
    await ctx.channel.send(embed=embed)
    
########################################
bot.run(apiToken.token)
########################################