import apiToken
import discord
import findUser
import cube
from discord.ext.commands import Bot


############# discord bot start ################
intents = discord.Intents.all()
# !<asdf>
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game("!도움 을 입력하세요"))

################## !help #####################
@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title="큐브 얼마나 쳐먹었냐 ㅋㅋ",color=0x00ff00)
    embed.add_field(name="!큐브 <닉네임>", value="22/11/25 이후 큐브 내역을 보여줍니다.", inline=False)
    embed.add_field(name="!도움", value="도움말 출력", inline=False)
    embed.add_field(name="!정보넣기 <닉네임> <토큰>", value="토큰은 메이플 api센터에서 알아서 가져와라 띠벌", inline=False)
    embed.add_field(name="!업데이트 <닉네임>", value="정보 넣고 기다리셈 오래걸림..띠벌 ㅠ", inline=False)
    embed.add_field(name="!찾기 <닉네임>", value="찾고 싶은 사람의 무릉 층수, 레벨을 표시합니다.", inline=False)
    embed.add_field(name="추가 예정", value="", inline=False)
    await ctx.channel.send(embed=embed)
  

################## 큐브 사용 내역 #####################
@bot.command()
async def 큐브(ctx,name):
    await ctx.reply('❗️❗️❗️얼마나 썼냐 ㅋㅋ❗️❗️❗️')
    result = cube.cube_count(name)
    used_meso = 12500000*result[2] + 22600000*result[3]
    embed = discord.Embed(title="큐브 사용 내역",color=0xFF0000)
    embed.add_field(name="장인의 큐브", value=result[0], inline=False)
    embed.add_field(name="명장의 큐브", value=result[1], inline=False)
    embed.add_field(name="레드 큐브", value=result[2], inline=False)
    embed.add_field(name="블랙 큐브", value=result[3], inline=False)
    embed.set_footer(text = "꼴은 돈(리부트 기준, 장큡 명큡은 계산 안함) = %s 메소"%format(used_meso,','))
    await ctx.channel.send(embed=embed)

@bot.command()
async def 정보넣기(ctx,name,token):
    flag = cube.create_table(name,token)
    print(flag)
    if flag==None:
        await ctx.reply('정보를 입력하였습니다.\n!업데이트 <닉네임> 명령어를 입력하여 정보를 업데이트하세요.')
    else: await ctx.reply('❗️❗️❗️이미 등록되어있는 닉네임입니다.❗️❗️❗️')
    

@bot.command()
async def 업데이트(ctx,name):
    await ctx.reply('❗️❗️❗️오래걸립니다... 기다려!❗️❗️❗️')
    cube.maple_API(name)
    await ctx.reply('최신 버전입니다.')
    
################## 찾기 #####################
@bot.command()
async def 찾기(ctx,name):
    result = findUser.userInfo(name)
    embed = discord.Embed(title="✓서치 결과✓",color=0xFFFF00)
    embed.add_field(name='검색한 사람',value=name,inline=False)
    embed.add_field(name='레벨',value=result[1],inline=False)
    embed.add_field(name='무릉 층수',value=result[0],inline=False)
    await ctx.channel.send(embed=embed)
    
########################################
bot.run(apiToken.token)
########################################
