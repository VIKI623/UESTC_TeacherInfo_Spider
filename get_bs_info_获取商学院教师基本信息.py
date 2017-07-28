#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import re

url_base = "http://bs.scu.edu.cn"

def getHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'

if __name__ == "__main__":
    fo = open("D:/data/sichuanU/sxy.txt",'r')
    done = 0
    while not done:
        line = fo.readline()
        if(line != ''):
            tid = re.sub("\D", "", line)
            html = getHtml(line.strip())
            if(html!='error'):
                prereadydata={}
                soup = BeautifulSoup(html,"html5lib")
                Content = soup.find("div", class_="entry")
                basicContent = Content.find_all("td")  #basicContent[0]为图片信息
                introContent = Content.find_all("p")

                ##处理基本信息
                prereadydata['id'] = str(tid);
                prereadydata['name'] = basicContent[1].get_text().replace(u"姓名：", "").strip()
                prereadydata['job'] = basicContent[2].get_text().replace(u"职务：","").strip()
                prereadydata['title'] = basicContent[3].get_text().replace(u"职称：","").strip()
                prereadydata['phone'] = basicContent[4].get_text().replace(u"电话：","").strip()
                prereadydata['department'] = basicContent[5].get_text().replace(u"所在院系：","").strip()
                prereadydata['email'] = basicContent[6].get_text().replace(u"邮箱：","").strip()
                prereadydata['address'] = basicContent[7].get_text().replace(u"办公地址：","").strip()
                prereadydata['direction'] = basicContent[8].get_text().replace(u"研究方向：","").strip()

                ##处理个人简介信息
                introInfo = ""
                for i in range(0, len(introContent)):
                    introInfo = introInfo + introContent[i].get_text().strip() + " "
                introInfo = re.sub(re.compile(r'\s+'), ' ', introInfo).strip()
                prereadydata['introduction'] = introInfo.replace(u"个人简介：","")

                fk = open('D:/data/sichuanU/photo/10610502/sxy.json','w',encoding='utf-8')
                readydata = json.dumps(prereadydata,ensure_ascii=False)
                fk.write(readydata+ ',')
                fk.close()
        else:
            done = 1
    fo.close()