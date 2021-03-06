import discord
import requests
import json

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith("```Errors:"):
        err = message.content.split("Errors:")[1]
        err = err.split('```')[0]
        link="https://api.stackexchange.com/2.2/search/advanced"
        args= {
            "order" : "desc",
            "sort" : "votes",
            "q" : err,
            "site" : "stackoverflow"
        }
        stack=requests.get(url=link, params=args)
        ans=stack.json()
        await message.channel.send(ans["items"][0]["link"])
        await message.channel.send(ans["items"][1]["link"])
        await message.channel.send(ans["items"][2]["link"])
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
            await message.channel.send("```"+rep.get("Result")[:1000]+"```")
        if (type(rep.get("Warnings"))==str):
            await message.channel.send("```Warnings: "+rep.get("Warnings")[:1000]+"```")
        if (type(rep.get("Stats"))==str):      
            await message.channel.send("```Stats: "+rep.get("Stats")[:1000]+"```")
        if (type(rep.get("Errors"))==str):      
            await message.channel.send("```Errors: "+rep.get("Errors")[:1000]+"```")
        if (type(rep.get("Files"))==str):      
            await message.channel.send("```Files: "+rep.get("Files")[:1000]+"```")
client.run("ODE3MzgwODcxNDU1Mzc1NDAw.YEIrQQ.gxw6UTKW7hXMWBckARswyg-FKpE")