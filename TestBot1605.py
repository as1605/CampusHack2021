import discord
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse
import re
import random
from youtube_search import YoutubeSearch
import sys
import os

#lang_number[0],lang_name[1],lang_compiler[2],compiler_arguement[3]
language_array = [
    ["1","csharp","csc","source_file.cs -out:main.exe"],
    ["4","java","javac","Rextester.java"],
    ["5","python","python",""],
    ["6","c","gcc","source_file.c -o a.out"],
    ["7","c++","g++","source_file.cpp -o a.out"]
]

client = discord.Client()

def help(filename):
    with open(filename) as f:
        contents=f.read()
        return contents

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

def findid_cc(handle,contest_name,problem_id):
    url = 'https://www.codechef.com/'+contest_name+'/status/'+problem_id+'?sort_by=All&sorting_order=asc&language=All&status=All&handle='+handle+'&Submit=GO'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    elements=soup.find_all('table',class_='dataTable')
    sub_id=elements[0].tbody.find('td',{'width':'60'}).text
    return sub_id

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

def demo(s):
    if s=='c':
        with open('bot_c.txt') as f:
            lines=f.read()
            return lines
    elif s=='c++':
        with open('bot_c++.txt') as f:
            lines=f.read()
            return lines
    elif s=='python':
        with open('bot_python.txt') as f:
            lines=f.read()
            return lines
    elif s=='c#':
        with open('bot_c#.txt') as f:
            lines=f.read()
            return lines
    elif s=='java':
        with open('bot_java.txt') as f:
            lines=f.read()
            return lines
        
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

def clean(s):
    line=""
    for i in range(len(s)):
        line+=chr(s[i])
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

def meme_me(num):
    link = "https://xkcd.com/"+str(num)+"/info.0.json"
    response=requests.get(link)
    memes=response.json()        
    return memes

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

def youtube(search_query):
    results = YoutubeSearch(search_query,max_results=3).to_dict()
    links = []
    for result in results:
        url_suffix = result['url_suffix']
        link = "https://www.youtube.com" + url_suffix
        links.append(link)
    return links

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.lower().startswith("$demo"):
        string =message.content.split('$demo ')[1]
        lines =demo(string)
        await message.channel.send(lines)

    if message.content.lower().startswith("$comic"):
        num=random.randrange(1,1000,1)    
        memes=meme_me(num)
        num=memes['num']
        await message.channel.send('**#'+str(num)+' '+memes['title']+'**')
        await message.channel.send(memes['img'])
        await message.channel.send(memes['alt'])

    if message.content.lower().startswith("$help"):
        with open('help.txt') as f:
            lines=f.read()
            await message.channel.send(lines)

    if message.content.lower().find('$nice')>=0:
        await message.channel.send('nice to meet you')
    
    if message.content.lower().startswith("$stack"):
        s = message.content.split("$stack")[1]
        ques=stack(s)
        for q in ques:
            await message.channel.send(q[:2000])

    if message.content.lower().startswith("$duck"):
        s = message.content.split("$duck")[1]
        ques=duck(s)
        for q in ques:
            await message.channel.send(q[:2000])

    if message.content.lower().startswith("$github"):
        s = message.content.split(" ")
        user = s[1]
        repo = s[2]
        branch=s[3]
        path=s[4]
        beg=int(s[5])
        end=int(s[6])
        lines=github(user,repo,branch,path,beg,end)
        ext=path.split('.')[-1]
        out="```"+ext
        for line in lines:
            newline = '\n'
            out+=f'{newline}{line}'
        out+="```"
        await message.channel.send(out[:2000])
    
    if message.content.lower().startswith("$codechef"):
        s = message.content.split(" ")
        id = findid_cc(s[1],s[2],s[3])
        beg = int(s[4])
        end = int(s[5])
        lines=codechef(id,beg,end)
        out="```"
        if (len(s)>4):
            out+=s[4]
        for line in lines:
            newline = '\n'
            out+=f'{newline}{line}'
        out+="```"
        await message.channel.send(out[:2000])

    if message.content.lower().startswith("$youtube"):
        search_query = message.content.split("$youtube ")[1]
        links = youtube(search_query)
        for link in links:
            await message.channel.send(link)

    if any(message.content.startswith(language_array[index][2]) for index in range(len(language_array))):
        compiler_name = message.content.split('\n')[0]
        index = find_index(compiler_name)

        language_name = language_array[index][1]
        compiler = language_array[index][2]
        compiler_argument = language_array[index][3]
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

client.run(sys.argv[1])