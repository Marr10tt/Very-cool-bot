import discord
from discord.ext import tasks, commands
import youtube_dl
import os
import random
from dotenv import load_dotenv
import musicCommands
from musicCommands import *
import botTokens
from botTokens import channelToken

#Version 0.1.2

#controls the bots prefix
client = commands.Bot(command_prefix="!")
#removes the native help command
client.remove_command('help')

#Sends out a message to the terminal when the bot goes online
@client.event
async def on_ready():
    print(f'{client.user} has connected')

#sends out a message every 60 minutes to drink water in the hydration channel
@tasks.loop(minutes=60)
async def water():
    global channelToken
    await client.wait_until_ready()
    channel = client.get_channel(botTokens.channelToken)
    await channel.send("Have some water")

#generic commands 

#help command, displays list of all important commands
@client.command()
async def help(ctx):
    await ctx.send("""```help - displays a list of key commands 
play - plays a given youtube link 
leave - makes the bot leave the vc```""")

#music commands
@client.command()
async def play(ctx, url : str):
    global client
    await musicCommands.play(ctx, url, client)

@client.command()
async def leave(ctx):
    global client
    #Links to the music commands file allowing for cleaner file space
    await musicCommands.leave(ctx, client)

#pauses the current track 
@client.command()
async def pause(ctx):
    global client
    await musicCommands.pause(ctx, client)

#resumes the current track after being paused
@client.command()
async def resume(ctx):
    global client
    await musicCommands.resume(ctx, client)

#stops the music (unable to resume afterwards)
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

#other commands

#coin flip command (picks heads or tails)
@client.command()
async def coinflip(ctx):
    coinfliprandom = ["Heads", "Tails"]
    rancoin = random.choice(coinfliprandom)
    await ctx.send(rancoin)

#dice roll command (picks a calue between 1 and 6 (being changed to incorporate any size dice))
@client.command()
async def dice(ctx):
    #current list of choices for the dice
    dicerandom = ["You rolled a 1","You rolled a 2","You rolled a 3","You rolled 4","You rolled a 5","You rolled a 6"]
    randice = random.choice(dicerandom)
    await ctx.send(randice)

#starts the hydration reminder timer segment 
water.start()
#loads discord token from given .env file 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
