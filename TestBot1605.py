import discord
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re

#lang_number[0],lang_name[1],lang_compiler[2],compiler_arguement[3]
language_array = [
    ["1","c#","csc","source_file.cs -out:main.exe"],
    ["4","java","javac","Rextester.java"],
    ["5","python","python",""],
    ["6","c","gcc","source_file.c -o a.out"],
    ["7","c++","g++","source_file.cpp -o a.out"]
]

TOKEN="ODEwODY5MjEyNDA2NjEyMDU4.YCp6zQ.9FjMI0Vf4I3rs86iERSXJCvjTPI"

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
    index = find_index(plat)
    args= {
        "LanguageChoice": int(language_array[index][0]),
        "Program": code,
        "Input": inp,
        "CompilerArgs": language_array[index][3]
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

def clean(str):
    line=""
    for i in range(len(str)):
        line+=chr(str[i])
    line=line.replace("&amp;","&")
    line=line.replace("&lt;","<")
    line=line.replace("&gt;",">")
    line=line.replace("&quot;","\"")
    return line

def github(user,repo,branch,path,beg,end):
    link="https://raw.githubusercontent.com"
    link=link+'/'+user+'/'+repo+'/'+branch+'/'+path
    response=requests.get(url=link)
    response=response.content.splitlines()
    a=[]
    i=beg
    while (i<len(response)-1 and i<=end):
        a.append(f"{i}|"+clean(response[i]))
        i+=1
    return a

def find_index(compiler_name):
    compiler_array = []
    for i in range(len(language_array)):
        compiler_array.append(language_array[i][2])
    index = compiler_array.index(compiler_name)
    return index
# c# , java , python, c , c++
def find_error(full_error_string, index):
    if index == 0:
        error_messages = full_error_string.split('\n')
        for i in range(len(error_messages)):
            error_messages[i] = error_messages[i][error_messages[i].index(')')+1:]
            if(error_messages[i].endswith('\r')):
                error_messages[i] = error_messages[i][:-1]
        full_error_string = "c#" + error_messages[0]       
    elif index == 1:
        error_messages = re.split("error:|warning:",full_error_string)[1:]
        for i in range(len(error_messages)):
            error_messages[i] = error_messages[i].split('\n')[0]
        full_error_string = error_messages[0]
    elif index == 2:
        full_error_string = "Python "+full_error_string.split('\n')[-2]
    elif index == 3:
        error_messages = full_error_string.split("error:")[1:]
        for i in range(len(error_messages)):
            error_messages[i] = error_messages[i].split('\n')[0]
        full_error_string = error_messages[0]
    elif index == 4:
        error_messages = full_error_string.split("error:")[1:]
        for i in range(len(error_messages)):
            error_messages[i] = error_messages[i].split('\n')[0]
        full_error_string = error_messages[0]
    print(full_error_string)
    return full_error_string

def codechef(id,beg,end):
    link="https://www.codechef.com/viewplaintext/"
    link+=str(id)
    response=requests.get(url=link)
    response=response.content.splitlines()
    a=[]
    i=beg
    while (i<len(response)-1 and i<=end):
        a.append(f"{i}|"+clean(response[i]))
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

    if any(message.content.startswith(language_array[index][2]) for index in range(len(language_array))):
        compiler_name = message.content.split('\n')[0]
        index = find_index(compiler_name)

        language_name = language_array[index][1]
        compiler = language_array[index][2]
        compiler_arguement = language_array[index][3]
        if len(message.content.split("```"+language_name))>1:
            src=message.content.split("```"+language_name)[1].split("```")[0]
        else:
            src=message.content.split("```")[1]
        if len(message.content.split("```"))>3:
            inp=message.content.split("```")[3]
        else:
            inp=""
        judge= rex(src,inp,compiler)

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
            err = find_error(judge["Errors"],index)

            ques=stack(err)
            for q in ques:
                await message.channel.send(q[:2000])
            links=duck(err)
            for link in links:
                await message.channel.send(link[:2000])

client.run(TOKEN)