import discord
import random
import os
import datetime
import subprocess
import tempfile
import shutil

import time

from pystyle import *
from pystyle import Colors, Colorate
from discord.ext import commands
import asyncio


intents = discord.Intents.all()

config = {
   'token': "",  # Bot Token
   'authid': ['',],  # Owner(s) ID(s)
   'name': "AntiBlank",  
   'embedcolor': "2F2963", 
   'prefix': "!",
   'footer': "Antiblank | Be safe"
 }

# 0xFFFF00 <- yellow
# 0x702963 <- purple

os.system('cls')
os.system('title AntiBlank Bot')
banner = f"""

         [Developers = Nyxoy & Clyde ]
                          
                Prefix = [{config['prefix']}]

 █████╗ ███╗   ██╗████████╗██╗██████╗ ██╗      █████╗ ███╗   ██╗██╗  ██╗
██╔══██╗████╗  ██║╚══██╔══╝██║██╔══██╗██║     ██╔══██╗████╗  ██║██║ ██╔╝
███████║██╔██╗ ██║   ██║   ██║██████╔╝██║     ███████║██╔██╗ ██║█████╔╝ 
██╔══██║██║╚██╗██║   ██║   ██║██╔══██╗██║     ██╔══██║██║╚██╗██║██╔═██╗ 
██║  ██║██║ ╚████║   ██║   ██║██████╔╝███████╗██║  ██║██║ ╚████║██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝
                                                                        
                                                                                                                                                     

"""

print(Colorate.Horizontal(Colors.red_to_purple, (banner)))
bot = commands.Bot(command_prefix=f"{config['prefix']}", intents=intents, help_command=None)

def black():
    try:
        with open("blacklist.txt", "r") as f:
            lines = filter(None, f.read().splitlines())
            return set(map(int, lines))
    except FileNotFoundError:
        return set()

blacklist = black()
file_counts = {}

@bot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title=f"{config['name']} Moderation", description="Sorry this is not a command.", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)






@bot.command(name='bl')
async def ban_user(ctx, user_id: int):
    authed = config['authid']
    if str(ctx.message.author.id) not in authed:
        embed = discord.Embed(title=f"{config['name']} Moderation", description="You do not have the necessary permissions.", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
        return

    if user_id in blacklist:
        embed = discord.Embed(title=f"{config['name']} Moderation", description="This user is already in the bot blacklist.", color=discord.Color.green())
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
        return
    
    user = bot.get_user(user_id)
    if user:
        user_name = user.name
    else:
        user_name = "Unknown User"
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(Colorate.Horizontal(Colors.red_to_purple, f"{user_name} is bl by {ctx.message.author.name} at {current_time}"))

    with open("blacklist.txt", "a") as f:
        f.write(str(user_id) + "\n")
        
    blacklist.add(user_id)
    embed = discord.Embed(title=f"{config['name']} Moderation", description=f"{user_name} is now in the bot blacklist.", color=discord.Color.green())
    embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)


with open("blacklist.txt", "r") as f:
    blacklist = set(int(line.strip()) for line in f.readlines())


@bot.command(name='unbl')
async def unban_user(ctx, user_id: int):
    authed = config['authid']
    if str(ctx.message.author.id) not in authed:
        embed = discord.Embed(title=f"{config['name']} Moderation", description="You do not have the necessary permissions.", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
        return

    if user_id not in blacklist:
        embed = discord.Embed(title=f"{config['name']} Moderation", description="This person isn't in the bot blacklist.", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
        return
    
    
    user = bot.get_user(user_id)
    if user:
        user_name = user.name
    else:
        user_name = "Unknown User"
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(Colorate.Horizontal(Colors.red_to_purple,f"{user_name} is unbl by {ctx.message.author.name} at {current_time}"))

    with open("blacklist.txt", "r") as f:
        lines = f.readlines()
    with open("blacklist.txt", "w") as f:
        for line in lines:
            if str(user_id) not in line.strip():
                f.write(line)

    blacklist.remove(user_id)
    embed = discord.Embed(title=f"{config['name']} Moderation", description=f"{user_name} is now no longer in the bot blacklist.", color=discord.Color.green())
    embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)

@bot.command(name='help')
async def lolhelpdude(ctx):
    if ctx.message.author.id in blacklist:
        embed=discord.Embed(title=f"{config['name']} Moderation", description="""
You are in the bot blacklist.
Try to contact the staff to revok this decision.""", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
 
    else:
        embed = discord.Embed(title=f"{config['name']} Commands", description=f"""
- !help → `Show bot's commands`
- !getkey → `Find out how to get a key`
- !info → `Some informations about the bot`
- !extract <your_key> → `Extract the webhook from a blank .exe file`""", color=int(config['embedcolor'], 16))
    embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)


@bot.command(name='info')
async def abu(ctx):
    if ctx.message.author.id in blacklist:
        embed=discord.Embed(title=f"{config['name']} Moderation", description="""
You are in the bot blacklist.
Try to contact the staff to revok this decision.""", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
    else:
        embed=discord.Embed(title=f"{config['name']} Informations", description="""
- Since : `August 2023`
- Bot Developers : `nyxoy & clyde`

- What is this bot : `Get the webhook of an .exe file made with blank`""", color=int(config['embedcolor'], 16))
        embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)


@bot.command(name='getkey')
async def ss(ctx):
    if ctx.message.author.id in blacklist:
        embed=discord.Embed(title=f"{config['name']} Moderation", description="""
You are in the bot blacklist.
Try to contact the staff to revok this decision.""", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
    else:
    # Create an embed message
        embed=discord.Embed(title=f"{config['name']} Key Manager", description="""
**How to get a key ?**
1. Create a ticket in admin's server. ||not maintained||
2. Wait for a staff member.
3. Open your dms, you will receive your key in private message.
                            - One key per person !""", color=int(config['embedcolor'], 16))
        embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)

def generatek():
    return "".join(
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        for _ in range(10)
    )

@bot.command(name='genkey')
async def genkeyy(ctx, user_id: int):
    authed = config['authid']
    if str(ctx.message.author.id) not in authed:
        embed = discord.Embed(
            title=f"{config['name']} Moderation",
            description="You do not have the necessary permissions.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
        return
    
    user = bot.get_user(user_id)
    if user:
        user_name = user.name
    else:
        user_name = "Unknown User"
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(Colorate.Horizontal(Colors.red_to_purple,f"{ctx.message.author.name} created a key for {user_name} at {current_time}"))

    key = generatek()
    with open("KEYS.txt", "a") as file:
        file.write(f"{user_id}:KEY-{key}\n")  

    embed = discord.Embed(
        title=f"{config['name']} Key Manager",
        description=f"- This is your key : ```KEY-{key}```",
        color=int(config['embedcolor'], 16)
    )
    embed.set_footer(text=f"{config['footer']}")
    user = await bot.fetch_user(int(user_id))  
    await user.send(embed=embed)

    embed = discord.Embed(
        title=f"{config['name']} Key Manager",
        description=" The User Key has been successfully generated! Check your DMs",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)

@bot.command(name='revok')
async def blacklistk(ctx, userid: int):
    authed = config['authid']
    if str(ctx.message.author.id) not in authed:
        embed = discord.Embed(title=f"{config['name']} Moderation", description="You do not have the necessary permissions.", color=discord.Color.red())
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
        return
    
    user = bot.get_user(userid)
    if user:
        user_name = user.name
    else:
        user_name = "Unknown User"
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(Colorate.Horizontal(Colors.red_to_purple,f"{ctx.message.author.name} revoked a key for {user_name} at {current_time}"))
  

    with open("KEYS.txt", "r") as f:
        lines = f.readlines()

    with open("KEYS.txt", "w") as f:
        for line in lines:
            if not line.startswith(f"{userid}:"):
                f.write(line)

    embed = discord.Embed(title=f"{config['name']} Key Manager", description=f"{userid}'s key has been succefuly revoked", color=discord.Color.green())
    embed.set_footer(text=f"{config['footer']}")
    await ctx.send(embed=embed)




@bot.command(name='extract')
async def unblank(ctx, key: str = "default"):
    if ctx.message.author.id in blacklist:
        embed = discord.Embed(
            title=f"{config['name']} Moderation",
            description="You are in the bot blacklist. Try to contact the staff to revoke this decision.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"{config['footer']}")
        await ctx.send(embed=embed)
    else:
        with open("KEYS.txt", "r") as f:
            keys = [line.strip().split(":") for line in f.readlines()]

        valid_key = False
        for k in keys:
            if k[0] == str(ctx.author.id) and k[1] == key:
                valid_key = True
                break

        if not valid_key:
            embed = discord.Embed(
                title=f"{config['name']} Key Manager",
                description="This is not your key.\n`!getkey` to get a key.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"{config['footer']}")
            await ctx.send(embed=embed)
        else:
              
            webhook_file = os.path.join("webhook.txt")

            embed = discord.Embed(
                title=f"{config['name']} Extractor",
                description="`[+] Please attach the .exe file ...`",
                color=int(config['embedcolor'], 16))
            embed.set_footer(text=f"{config['footer']}")
            await ctx.send(embed=embed)

            def check(message):
                return message.author == ctx.author and message.attachments

            try:
                msg = await bot.wait_for('message', check=check, timeout=60)
                attachment = msg.attachments[0]
                file_name = attachment.filename

                if file_name.endswith('.exe'):
                    await attachment.save('file.exe')
                    embed = discord.Embed(
                        title=f"{config['name']} Extractor",
                        description="`[+] File downloaded, extracting webhook ...`",
                        color=int(config['embedcolor'], 16))
                    embed.set_footer(text=f"{config['footer']}")
                    await ctx.send(embed=embed)

                    try:
                        subprocess.run('C:\\Users\\erict\\AppData\\Local\\Programs\\Python\\Python311\\python.exe main.py file.exe')  
                        await asyncio.sleep(5)

                        try:
                                        shutil.rmtree('file.exe_extracted')
                        except Exception as e:
                                pass                          


                        try:
                            with open(webhook_file, 'r') as f:
                                webhook_content = f.read()



                            embed = discord.Embed(
                                title=f"{config['name']} Extractor",
                                description=f"`[+] Webhook extracted :`\n```md\n{webhook_content}\n```\n [Webhook Tool](https://github.com/Nyxoy201/Webhook-Tool)",
                                color=int(config['embedcolor'], 16))
                            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1199393377905557616/1199723411606352073/Screenshot_2023-12-22_002059.png?ex=65c3947f&is=65b11f7f&hm=96704884efdbc269a9e9312d16bdfa3122c9cce6af583f634721d3781f407d78&")

                            embed.set_footer(text=f"{config['footer']}")

                            await ctx.author.send(embed=embed)

                            with open(webhook_file, 'w') as f:
                                f.write('')

                            embed = discord.Embed(
                                title=f"{config['name']} Extractor",
                                description="`[+] Webhook content sent via DM.`",
                                color=int(config['embedcolor'], 16))
                            embed.set_footer(text=f"{config['footer']}")
                            await ctx.send(embed=embed)

                        except FileNotFoundError:
                            embed = discord.Embed(
                                title=f"{config['name']} Extractor",
                                description="`[+] Webhook not found`",
                                color=discord.Color.red())
                            embed.set_footer(text=f"{config['footer']}")
                            await ctx.send(embed=embed)
                    except Exception as e:
                        embed = discord.Embed(
                            title=f"{config['name']} Extractor",
                            description=f"`[+] Error during extraction: {e}`",
                            color=discord.Color.red())
                        embed.set_footer(text=f"{config['footer']}")
                        await ctx.send(embed=embed)

                    if os.path.exists('file.exe'):
                        os.remove('file.exe')

                else:
                    embed = discord.Embed(
                        title=f"{config['name']} Extractor",
                        description="[+] Error downloading file ...`",
                        color=discord.Color.red())
                    embed.set_footer(text=f"{config['footer']}")
                    await ctx.send(embed=embed)
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title=f"{config['name']} Extractor",
                    description="`[+] Retry with a Blank file`",
                    color=discord.Color.red())
                embed.set_footer(text=f"{config['footer']}")
                await ctx.send(embed=embed)


            




bot.run(config['token'])
