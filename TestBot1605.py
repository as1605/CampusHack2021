import discord
import requests
import json

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if (message.author.nick==None):
        name=message.author.name
    else:
        name=message.author.nick
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! '+ name)
    if message.content.lower().find('nice')>=0:
        await message.channel.send('nice')
    if message.content.startswith('g++'):
        url='https://rextester.com/rundotnet/api'
        req= {
            "LanguageChoice": 7,
            "Program": message.content.split("```c++")[1],
            "Input": message.content.split("```txt")[1],
            "CompilerArgs": "source_file.cpp -o a.out"
        }
        rep = requests.post(url, data=req).json()
        if (type(rep.get("Result"))==str):
            await message.channel.send("```"+rep.get("Result")+"```")
        if (type(rep.get("Warnings"))==str):
            await message.channel.send("```Warnings: "+rep.get("Warnings")+"```")
        if (type(rep.get("Stats"))==str):      
            await message.channel.send("```Stats: "+rep.get("Stats")+"```")
        if (type(rep.get("Errors"))==str):      
            await message.channel.send("```Errors: "+rep.get("Errors")+"```")
        if (type(rep.get("Files"))==str):      
            await message.channel.send("```Files: "+rep.get("Files")+"```")

client.run("ODE3MzgwODcxNDU1Mzc1NDAw.YEIrQQ.gxw6UTKW7hXMWBckARswyg-FKpE")