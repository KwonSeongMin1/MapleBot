import discord
import apiToken
import cubeCount
import findUser
from discord.ext.commands import Bot


############# 디코 봇 코드 ################
intents = discord.Intents.all()
# /명령어
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game("!도움 을 입력하세요"))

################## 도움말 #####################
@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title="큐브 사용 내역",color=0x00ff00)
    embed.add_field(name="!큐브 <닉네임> <아이템 이름>", value="아이템에 넣은 큐브 목록을 보여줍니다.\n 22/11/25 이후 큐브 내역을 보여줍니다.", inline=False)
    embed.add_field(name="!도움", value="도움말 출력", inline=False)
    embed.add_field(name="!찾기 <닉네임>", value="찾고 싶은 사람의 무릉 층수, 레벨을 표시합니다.", inline=False)
    embed.add_field(name="추가 예정", value="", inline=False)
    await ctx.channel.send(embed=embed)
  

################## 큐브 사용 내역 #####################
@bot.command()
async def 큐브(ctx,name,*,target_item):
    await ctx.reply('❗️❗️❗️시간이 다소 걸립니다.\n결과가 나오기 전 까지 기다려 주세요.')
    result = cubeCount.maple_API(name,target_item)
    used_meso = 12500000*result[2] + 22600000*result[3]
    embed = discord.Embed(title="큐브 사용 내역",color=0xFF0000)
    embed.add_field(name="장인의 큐브", value=result[0], inline=False)
    embed.add_field(name="명장의 큐브", value=result[1], inline=False)
    embed.add_field(name="레드 큐브", value=result[2], inline=False)
    embed.add_field(name="블랙 큐브", value=result[3], inline=False)
    embed.set_footer(text = "꼴은 돈(리부트 기준, 장큡 명큡은 계산 안함) = %s 메소"%format(used_meso,','))
    await ctx.channel.send(embed=embed)
    
    
################## 찾기 #####################
@bot.command()
async def 찾기(ctx,name):
    result = findUser.userInfo(name)
    embed = discord.Embed(title="✓서치 결과✓",color=0xFFFF00)
    embed.add_field(name='검색한 사람',value=name,inline=False)
    embed.add_field(name='레벨',value=result[1],inline=False)
    embed.add_field(name='무릉 층수',value=result[0],inline=False)
    await ctx.channel.send(embed=embed)
    
################## test용 #####################
@bot.command()
async def 테스트(ctx):
    await ctx.channel.send("이것은 TTS 테스트라고 합니다!",tts=True)
    
########################################
bot.run(apiToken.token)
########################################