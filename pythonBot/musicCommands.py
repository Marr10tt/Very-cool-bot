import discord
import youtube_dl
import os
from discord.ext import commands

#downloads and plays the song based on YT link
#defines the file name of the song downloaded also deleting it after the song is changed allowing for file efficiency
async def play(ctx, url : str, client):
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
async def leave(ctx, client):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

async def resume(ctx, client):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        #throws error message
        await ctx.send("The audio is not paused.")

async def pause(ctx, client):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")
