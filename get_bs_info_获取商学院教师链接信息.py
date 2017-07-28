#coding=utf-8
import requests
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
     html = getHtml(url_base + "/index.php?m=fcontent&a=index&catid=13")
     fp = open('D:/data/sichuanU/sxy.txt','w')
     if(html!='error'):
            soup = BeautifulSoup(html,"html.parser")
            content = soup.find_all('ul',class_="clearfix")
            TeacherList = content[1].find_all('a')
            for Teacher in TeacherList:
                fp.write(url_base + Teacher["href"] + "\n")
            fp.close