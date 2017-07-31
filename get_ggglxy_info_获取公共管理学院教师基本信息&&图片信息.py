#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import re

url_base = "http://ggglxy.scu.edu.cn"

def getHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'

if __name__ == "__main__":
    for page in range(1, 17):
        html = getHtml(url_base + "/index.php?c=article&a=type&tid=18&page_1_page=" + str(page))
        if (html != 'error'):
            soup = BeautifulSoup(html, "html.parser")
            TeacherList = soup.find_all("li", class_="fl")
            prereadydata = {}
            for Teacher in TeacherList:
                content = Teacher.find_all("div")
                subUrl = url_base + "/" + content[0].find("a")["href"]
                picUrl = url_base + content[0].find("img")["src"]
                prereadydata["name"] = content[1].find("h3").get_text()
                prereadydata["title"] = content[1].find("p").get_text()
                prereadydata["department"] = content[2].find("p").get_text()
                prereadydata["email"] = content[2].find_all("p")[1].get_text()

                ##获取教师图片
                tid = re.sub("\D", "", subUrl)
                pic = requests.get(picUrl)
                fo = open('D:/data/sichuanU/photo/10610501/' + tid + '.jpg', 'wb')
                fo.write(pic.content)
                fo.close()

                ##获取教师资料
                subHtml = getHtml(subUrl)
                if (html != 'error'):
                    subSoup = BeautifulSoup(subHtml, "html.parser")
                    prereadydata["introduction"] = subSoup.find("div",class_ = "desc").get_text().strip()

                    subContent = subSoup.find_all("div",class_ = "detailbox mt20")

                    paperInfo = subContent[0].get_text()
                    paperInfo = re.sub(re.compile(r'\s+'), ' ', paperInfo).strip()
                    prereadydata["paper"] = paperInfo

                    awardInfo = subContent[1].get_text()
                    awardInfo = re.sub(re.compile(r'\s+'), ' ', awardInfo).strip()
                    prereadydata["award"] = awardInfo

                    projectInfo = subContent[2].get_text()
                    projectInfo = re.sub(re.compile(r'\s+'), ' ', projectInfo).strip()
                    prereadydata["project"] = projectInfo

                    jobInfo = subContent[3].get_text()
                    jobInfo = re.sub(re.compile(r'\s+'), ' ', jobInfo).strip()
                    prereadydata["job"] = jobInfo

                fk = open('D:/data/sichuanU/photo/10610501/ggglxy.json','w',encoding='utf-8')
                readydata = json.dumps(prereadydata,ensure_ascii=False)
                fk.write(readydata+ ',')
                fk.close()