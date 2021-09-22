import discord
from discord.ext import commands
import youtube_dl
import os
import random

client = commands.Bot(command_prefix="!")
#music bot
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.webm")
    try:
        if song_there:
            os.remove("song.webm")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='general')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': '249/250/251',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
    voice.play(discord.FFmpegOpusAudio("song.webm"))

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


#other commands
@client.command()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin)
    
@client.command()
async def dice(ctx):
    choices1 = ["You rolled a 1","You rolled a 2","You rolled a 3","You rolled 4","You rolled a 5","You rolled a 6"]
    randice = random.choice(choices1)
    await ctx.send(randice)

@client.command()
async def copy(ctx):
    await ctx.send("copy")

client.run('')
