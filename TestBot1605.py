import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message)
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run("ODE3MzgwODcxNDU1Mzc1NDAw.YEIrQQ.gxw6UTKW7hXMWBckARswyg-FKpE")