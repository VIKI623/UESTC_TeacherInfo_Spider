#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json


dic = {
    'Labelxydm':'SchoolCode',  #学院代码
    'Labelxymc':'School',  #学院名称
    'Labeldsdm': 'IdentifyCode',  #导师代码
    'Labeldsxm': 'Name',  #导师姓名
    'Labelxb': 'Gender',  #性别
    'Labelcsny': 'Birth',  #出生年月
    'Labeltc': 'Special',  #特称
    'Labelzc': 'Title',  #职称
    'Labellb': 'Kind',  #类别
    'Labelxw': 'Degree',  #学位
    'Labelsx': 'Property',  #属性
    'Labelemail': 'Email',  #电子邮件
    'Labelxsjl': 'Experience',  #学术经历
    'Labelgrjj': 'Introduction',  #个人简介
    'lblKyxm': 'Project',  #科研项目
    'lblFbwz': 'Paper',  #发表文章
    'Labelbszydm1':'PhdMajor1Code',  #博士招生代码1
    'Labelbszymc1':'PhdMajor1Name',  #博士招生名称1
    'Labelsszydm1':'MasterMajor1Code',  #硕士招生代码1
    'Labelsszymc1':'MasterMajor1Name',  #硕士招生名称1
    'Labelbszydm2':'PhdMajor2Code',  #博士招生代码2
    'Labelbszymc2':'PhdMajor2Name',  #博士招生名称2
    'Labelsszydm2':'MasterMajor2Code',  #硕士招生代码2
    'Labelsszymc2':'MasterMajor2Name',  #硕士招生名称2
    'Labelbszydm3':'PhdMajor3Code',  #博士招生代码3
    'Labelbszymc3':'PhdMajor3Name',  #博士招生名称3
    'Labelsszydm3':'MasterMajor3Code',  #硕士招生代码3
    'Labelsszymc3':'MasterMajor3Name',  #硕士招生名称3
    'Labelbszydm4':'PhdMajor4Code',  #博士招生代码4
    'Labelbszymc4':'PhdMajor4Name',  #博士招生名称4
    'Labelsszydm4':'MasterMajor4Code',  #硕士招生代码4
    'Labelsszymc4':'MasterMajor4Name',  #硕士招生名称4
    'Labelbszydm5':'PhdMajor5Code',  #博士招生名称5
    'Labelbszymc5':'PhdMajor5Name',  #博士招生名称5
    'Labelsszydm5':'MasterMajor5Code',  #硕士招生代码5
    'Labelsszymc5':'MasterMajor5Name',  #硕士招生名称5
}

def getHtml(url):
    try:
        res= requests.get(url)
        res.raise_for_status()  #若发生错误请求，则抛出异常
        res.encoding = res.apparent_encoding  #从内容中分析出的响应内容编码方式
        return res.text
    except:
        return None

if __name__ == "__main__":
    JZY_id = 666;
    html = getHtml("http://222.197.183.99/TutorDetails.aspx?id=" + str(JZY_id))
    if(html != None):
        soup = BeautifulSoup(html,'html.parser')
        content = soup.find(id ="main")
        items = content.find_all('span')
        prereadydata = {}

        ##提取学院代码、学院名称、导师代码、导师姓名等信息
        for i in range(0,len(items)):
            if(items[i].string != None and 'id' in items[i].attrs):
                code = items[i].attrs['id']
                prereadydata[dic[code]] = items[i].string
        prereadydata['University'] = "电子科技大学"
        prereadydata['UniversityCode'] = "10614"

        ##若招生代码存在，则提取招生方向信息
        if 'PhdMajor1Code' or 'MasterMajor1Code' in prereadydata:
            itemMajor = content.select("table .l-wrap")
            detail = {}
            for i in range(0, len(itemMajor)):
                Code = itemMajor[i].select(".width4em")
                Name = itemMajor[i].select(".alignleft")
                if (i % 2 == 1):
                    degree = "Master"
                else:
                    degree = "Phd"
                for j in range(0,len(Code)):
                    ##招生方向序号  EX:detail[MasterMajor1Filed1Code] = “01方向：”
                    detail[degree + 'Major'+ str(int(i/2)+1) + 'Field'+str(j+1)+'Code'] = Code[j].string.strip()
                    ##招生方向名称  EX:detail[PhdMajor1Field1Name] = “软件理论与技术”
                    detail[degree + 'Major'+ str(int(i/2)+1) + 'Field'+str(j+1)+'Name'] = Name[j].string.strip()
        if detail != {}:
            prereadydata['MajorFeildDetail']=detail
        try:
            with open('D:/data/ZhanJinYu_Info.json','w') as f:
                json.dump(prereadydata, f, ensure_ascii = False)
            print("Success Finish")
        except:
            print("File Write Error")
    else:
        print("Get Html Error")