#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup

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
    fp = open("D:/data/sichuanU/sxy.txt",'r')
    done = 0
    while not done:
        line = fp.readline()
        if(line != ''):
            tid = re.sub("\D", "", line)
            html = getHtml(line.strip())
            if(html!='error'):
                prereadydata={}
                soup = BeautifulSoup(html,"html5lib")
                picUrl = soup.find("img")["src"]
                if(picUrl != "/public/uploads/"):
                    pic = requests.get(url_base + picUrl)
                    fo = open('D:/data/sichuanU/photo/10610502/'+tid+'.jpg','wb')
                    fo.write(pic.content)
                    fo.close()
        else:
            done = 1
    fp.close()
