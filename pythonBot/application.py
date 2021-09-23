import discord
from discord.ext import commands
import youtube_dl
import os
import random
from dotenv import load_dotenv
#Version 0.1.2

#controls the bots prefix
client = commands.Bot(command_prefix="!")
#removes the native help command
client.remove_command('help')

#generic commands 

#help command, displays list of all important commands
@client.command()
async def help(ctx):
    await ctx.send("help - displays a list of key commands")
    await ctx.send("play - plays a given youtube link")
    await ctx.send("leave - makes the bot leave the vc")

#music commands

#downloads and plays the song based on YT link
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.webm")
    try:
        if song_there:
            os.remove("song.webm")
    #throws a user error message if 2 songs are tried to be played at once
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    #connects the bot to the general vc
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='general')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #249/250/251 sets it to download a webm. 
    #discord.FFMpegOpusAudio allows it to play immediately after downloading without any conversion
    ydl_opts = {
        'format': '249/250/251',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
    voice.play(discord.FFmpegOpusAudio("song.webm"))

#makes the bot leave the vc it is in
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

#pauses the current track 
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

#resumes the current track after being paused
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        #throws error message
        await ctx.send("The audio is not paused.")

#stops the music (unable to resume afterwards)
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


#other commands

#coin flip command (picks heads or tails)
@client.command()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

#dice roll command (picks a calue between 1 and 6 (being changed to incorporate any size dice))
@client.command()
async def dice(ctx):
    #current list of choices for the dice
    choices1 = ["You rolled a 1","You rolled a 2","You rolled a 3","You rolled 4","You rolled a 5","You rolled a 6"]
    randice = random.choice(choices1)
    await ctx.send(randice)

#loads discord token from given .env file 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
