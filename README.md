# Very-cool-bot
A very cool bot

libraries needed to run the bot:
discord.py
pynacl
youtube-dl
yt-dlg
dotENV

files required to support music playing: 
ffmpeg.exe

# dotenv
create file called .env in the same place you have the application.py and ffmpeg.exe saved, inside the file do DISCORD_TOKEN=*replace token here*, this will allow the application to pull the token for use in running the bot 

# hydration channel information
create a file called botTokens.py with a variable called channelToken which contains the value of the channel you want hydration reminders in

example (something like this in a botTokens.py file):

channelToken = 12345678
