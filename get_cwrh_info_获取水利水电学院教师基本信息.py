#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import re

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
    fo = open("D:/data/sichuanU/slsd.txt",'r')
    done = 0
    while not done:
        line = fo.readline()
        if(line != ''):
            tid = re.sub("\D", "", line)
            html = getHtml(line.strip())
            if(html!='error'):
                prereadydata={}
                soup = BeautifulSoup(html,"html.parser")
                basicContent = soup.find("div", class_="js_1")
                reserchContent = soup.find("div", class_="js_2" )
                paperContent = soup.find("div", class_="js_3" )
                awardContent = soup.find("div", class_="js_4" )
                courseContent = soup.find("div", class_="js_5")
                ##js_6为联系方式，与js_1基本信息重复
                otherContent = soup.find("div", class_="js_7")

                ##处理js_1基本信息
                basic = basicContent.find_all("li")
                prereadydata['id'] = str(tid);
                prereadydata['name'] = basic[0].get_text().replace(u"姓名：","").strip()
                prereadydata['gender'] = basic[1].get_text().replace(u"性别：","").strip()
                prereadydata['birth'] = basic[2].get_text().replace(u"出生年月：","").strip()
                prereadydata['degree'] = basic[3].get_text().replace(u"学位：","").strip()
                prereadydata['title'] = basic[4].get_text().replace(u"职称：","").strip()
                prereadydata['address'] = basic[5].get_text().replace(u"联系地址：","").strip()
                prereadydata['postcode'] = basic[6].get_text().replace(u"邮编：","").strip()
                prereadydata['email'] = basic[7].get_text().replace(u"电子邮箱：","").strip()
                prereadydata['phone'] = basic[8].get_text().replace(u"电话号码：","").strip()
                prereadydata['fax'] = basic[9].get_text().replace(u"传真：","").strip()

                ##处理js_2科研信息
                reserch = "".join(reserchContent.get_text().splitlines())
                prereadydata['reserch'] = reserch.strip()

                ##处理js_3论文信息
                paper = "".join(paperContent.get_text().splitlines())
                prereadydata['paper'] = paper.strip()

                ##处理js_4荣誉信息
                award = "".join(awardContent.get_text().splitlines())
                prereadydata['award'] = award.strip()

                ##处理js_5课程信息
                course = "".join(courseContent.get_text().splitlines())
                prereadydata['course'] = course.strip()

                ##处理js_7其他信息
                other = "".join(otherContent.get_text().splitlines())
                prereadydata['other'] = other.strip()

                fk = open('D:/data/sichuanU/photo/10610102/slsd.json','w',encoding='utf-8')
                readydata = json.dumps(prereadydata,ensure_ascii=False)
                fk.write(readydata+ ',')
                fk.close()
        else:
            done = 1
    fo.close()