#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup

url_base = "http://cwrh.scu.edu.cn"

def getHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


if __name__ == "__main__":
     html = getHtml(url_base + "/home/teacher/index.html")
     fp = open('D:/data/sichuanU/slsd.txt','w')
     if(html!='error'):
            soup = BeautifulSoup(html,"html.parser")
            content = soup.find_all('div',class_="menu")
            TeacherList = content[1].find_all('a',href=re.compile(u"/home/teacher/details/id/"))
            for Teacher in TeacherList:
                fp.write(url_base + Teacher["href"] + "\n")
            fp.close