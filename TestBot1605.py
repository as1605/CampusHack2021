import discord
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse

TOKEN="ODE3MzgwODcxNDU1Mzc1NDAw.YEIrQQ.dXNWOi9Dvv3ePnebssNsFl1Igow"
client = discord.Client()

def stack(q, n=3):
    link="https://api.stackexchange.com/2.2/search/advanced"
    args= {
        "order" : "desc",
        "sort" : "votes",
        "q" : q[:1000],
        "site" : "stackoverflow"
    }
    response=requests.get(url=link, params=args)
    response=response.json()
    a=[]
    for i in range(n):
        try:
            a.append(response["items"][i]["link"])
        except:
            continue
    return a

def duck(str, n=5):
    r = requests.get('https://duckduckgo.com/html/?q='+str, headers={'user-agent': 'my-app/0.0.1'}) 
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('a', attrs={'class':'result__a'}, href=True)
    a=[]
    for link in results:
        n=n-1
        url = link['href']
        o = urllib.parse.urlparse(url)
        d = urllib.parse.parse_qs(o.query)
        a.append(d['uddg'][0])
        if n<=0:
            break
    return a

def rex(code, inp, plat='g++'):
    link='https://rextester.com/rundotnet/api'
    args= {
        "LanguageChoice": 7,
        "Program": code,
        "Input": inp,
        "CompilerArgs": "source_file.cpp -o a.out"
    }
    response = requests.post(link, data=args).json()
    a={}
    try:
        a["Result"]=response.get("Result")
    except:
        a["Result"]=None
    try:
        a["Warnings"]=response.get("Warnings")
    except:
        a["Warnings"]=None
    try:
        a["Errors"]=response.get("Errors")
    except:
        a["Errors"]=None
    try:
        a["Stats"]=response.get("Stats")
    except:
        a["Stats"]=None
    try:
        a["Files"]=response.get("Files")
    except:
        a["Files"]=None
    return a

def github(user,repo,branch,path,beg,end):
    link="https://raw.githubusercontent.com"
    link=link+'/'+user+'/'+repo+'/'+branch+'/'+path
    response=requests.get(url=link)
    response=response.content.splitlines()
    a=[]
    i=beg
    while (i<len(response)-1 and i<=end):
        a.append(f"{i}|"+str(response[i]))
        i+=1
    return a

def codechef(id,beg,end):
    link="https://www.codechef.com/viewplaintext/"
    link+=str(id)
    response=requests.get(url=link)
    response=response.content.splitlines()
    a=[]
    i=beg
    while (i<len(response)-1 and i<=end):
        a.append(f"{i}|"+str(response[i]))
        i+=1
    return a

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.lower().find('nice')>=0:
        await message.channel.send('nice')
    
    if message.content.lower().startswith("stack"):
        str = message.content.split("stack")[1]
        ques=stack(str)
        for q in ques:
            await message.channel.send(q[:2000])

    if message.content.lower().startswith("duck"):
        str = message.content.split("duck")[1]
        ques=duck(str)
        for q in ques:
            await message.channel.send(q[:2000])

    if message.content.lower().startswith("github"):
        str = message.content.split(" ")
        user = str[1]
        repo = str[2]
        branch=str[3]
        path=str[4]
        beg=int(str[5])
        end=int(str[6])
        lines=github(user,repo,branch,path,beg,end)
        ext=path.split('.')[-1]
        out="```"+ext
        for line in lines:
            newline = '\n'
            out+=f'{newline}{line}'
        out+="```"
        await message.channel.send(out[:2000])
    
    if message.content.lower().startswith("codechef"):
        str = message.content.split(" ")
        id = str[1]
        beg = int(str[2])
        end = int(str[3])
        lines=codechef(id,beg,end)
        out="```"
        if (len(str)>4):
            out+=str[4]
        for line in lines:
            newline = '\n'
            out+=f'{newline}{line}'
        out+="```"
        await message.channel.send(out[:2000])

    if message.content.lower().startswith("g++"):
        judge= rex(message.content.split("```c++")[1],message.content.split("```txt")[1],"g++")
        if judge["Result"]!=None:
            await message.channel.send("```"+judge["Result"][:2000]+"```")
        if judge["Warnings"]!=None:
            await message.channel.send("```Warnings: "+judge["Warnings"][:2000]+"```")
        if judge["Stats"]!=None:
            await message.channel.send("```Stats: "+judge["Stats"][:2000]+"```")
        if judge["Errors"]!=None:
            await message.channel.send("```Errors: "+judge["Errors"][:2000]+"```")
        if judge["Files"]!=None:
            await message.channel.send("```Files: "+judge["Files"][:2000]+"```")

        if judge["Errors"]!=None:
            err=judge["Errors"].split(':')
            index=err.index(' error')
            err=err[index+1]
            ques=stack(err)
            for q in ques:
                await message.channel.send(q[:2000])
            links=duck(err)
            for link in links:
                await message.channel.send(link[:2000])

client.run(TOKEN)