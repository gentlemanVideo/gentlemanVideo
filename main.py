import os
import urllib.request
import urllib.error
import urllib.parse
import re
import json
import base64
import requests
import datetime
import time
import random

def get_ua():
    import random
    user_agents = [
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
		"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
		"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
		"Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
		"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
		"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14"
    ]
    user_agent = random.choice(user_agents)
    return user_agent

def getsttings(num):
    setting_str=[]
    with open("./settings.txt",'r',encoding='UTF-8') as filecont:
        contents=filecont.readlines()
    filecont.close()
    for i in range(len(contents)):
        setting_str.append(contents[i].split("@bf=")[1].replace("\n",""))
    return setting_str[num]  

  
ua = get_ua()
headers = {'User-Agent': ua}
vtitles=[]
vurls=[]
vimgs=[]

owner=getsttings(0)
repo=getsttings(1)
branch=getsttings(2)
#dlurl=getsttings(3)
token = os.environ['BFtoken']




def Vurldata(dlurl):
	_url = urllib.request.Request(dlurl,headers=headers)
	response = urllib.request.urlopen(_url, None, 10)
	data=response.read().decode('utf-8')
	response.close()
	# print(data)
	rule = r'data-id="(.*?)" data-is'
	vidList = re.findall(rule, data)
	#print(vidList)
	#https://www.xvideos.com/video{vidList}/_
	for vli in vidList:
		vitmeurl="https://www.xvideos.com/video"+ vli + "/_"
		#print(vitmeurl)
		_url2 = urllib.request.Request(vitmeurl,headers=headers)
		response2 = urllib.request.urlopen(_url2, None, 10)
		data2 = response2.read().decode('utf-8')
		vm3u8rule = r'html5player.setVideoHLS\(\'(.*?)\'\);'
		vm3u8 = re.findall(vm3u8rule, data2)
		vurls.append(vm3u8[0])
		vimgrule = r'html5player.setThumbUrl\(\'(.*?)\'\);'
		vimage = re.findall(vimgrule, data2)
		vimgs.append(vimage[0])
		vtitlerule = r'html5player.setVideoTitle\(\'(.*?)\'\);'
		vtitle_ = re.findall(vtitlerule, data2)
		vtitles.append(vtitle_[0])
		response2.close()
		RT = random.randint(1,2)
		time.sleep(RT)

#print(vtitles,vurls,vimgs)

with open("./data.txt",'r',encoding='UTF-8') as filecont:    
	datalists = filecont.readlines()
	filecont.close()
for i in range(len(datalists)):
	rt2 = random.randint(5,10)
	time.sleep(rt2)
	Vurldata(datalists[i])

with open("gentleman.txt","a", encoding='utf-8') as file:
	file.write("\n")
	for line in range(len(vtitles)):
		file.write("#image,"+vimgs[line]+"\n")
		file.write(vtitles[line]+","+vurls[line]+"\n\n")
	file.close()
	
	
def tobase64(filename):
    filepath = './'+filename
    with open(filepath, 'rb') as base64_:
        base64_str = base64.b64encode(base64_.read())
        str0 = base64_str.decode('utf-8')
        return str0

def upload_file(filename):
    global owner
    global repo
    global token
    global branch
    content=tobase64(filename)
    date_time = datetime.datetime.now().strftime('%Y-%m-%d')
    url="https://api.github.com/repos/"+owner+"/"+repo+"/contents/"+date_time+"/"+filename
    ua = get_ua()
    headers = {'User-Agent': ua,'Accept': 'application/vnd.github.v3+json','Authorization': 'token '+token}
    data = {"message":"actions update","content": content,"branch":branch}
    req = requests.put(url=url, data=json.dumps(data), headers=headers)
    print(req.text)
    return str(req).find("200")


	

up_live_list = upload_file("gentleman.txt")

if up_live_list != -1:
    print("gentleman.txt 已经更新")

else:
    print("gentleman.txt 更新失败")

	

