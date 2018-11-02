# _*_ coding: utf-8 _*_
# @Time     : 2018/9/29 4:30
# @Author   : Ole211
# @Site     : 
# @File     : handler.py
# @Software : PyCharm
import tornado.web
import codecs
import json
import os
from utils.taobao import TaobaoScrawl, TiebaScrawl
from utils.baike_crawl  import go
import requests
from utils.RSA import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('ball.html')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('07index.html', error='True')
    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        if username and password == '123':
            self.render('clock.html', username=username,error='success')
        else:
            self.render('07index.html', error='Fail')

class KeyLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("07index.html", error="True")
    def post(self):
        username2 = self.get_argument("username2", "")
        key = self.request.files.get("private_key", "")
        print(key)
        key_data = key[0]["body"]
        msg = decode(key_data, private_key[0], N)
        print('密文', key_data)
        print('解密', msg)
        if username2 and msg=="poo..1475":
            self.render("clock.html", username=username2, error="sucess")
        else:
            self.render("07index.html", error="Fail")


class HomeHandler(tornado.web.RequestHandler):
    def get_news(self):
        #'''获取金山词霸每日一句'''
        import requests
        import json
        self.url = "http://open.iciba.com/dsapi/"
        r = requests.get(self.url)
        content = r.json()['content']
        note = r.json()['note']
        return content, note

    def get(self):
        username = self.get_argument('username', 'no')
        urllist = [
            ("/login", "登陆窗口"),
            ('http://www.baidu.com', '百度'),
            ('http://www.zhihu.com', '知乎'),
            ('http://www.sina.com', '新浪'),
            ("/hikvision", "海康威视"),
            ("/huawei", "华为"),
            ("/dahua", "大华"),
            ("/dahuanews", "大华新闻"),
            ("/taobao", "淘宝搜索"),
            ("/tieba", "贴吧搜索"),
            ("/uploadfile", "文件上传"),
        ]
        atag = "<a href='http://www.baidu.com' target='_blank'>__百度一下__</a>"
        msg = self.get_news()
        self.render('03escape.html',
                    username=username,
                    urllist = urllist,
                    atag = atag,
                    msg=msg)

class ExtendHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('name', 'no')
        self.render('05extend.html', username=username)

class TaobaoHandler(tornado.web.RequestHandler):
    import csv
    def get(self):
        self.render('taobao.html', data='')

    def post(self):
        kw = self.get_argument('kw', '')
        import os
        filePath =  kw + '.json'
        if os.path.exists(filePath):
            with codecs.open(filePath, 'r') as f:
                content = f.readlines()
            data = []
            for line in content:
                data.append(json.loads(line))
            self.render('taobao.html', data=data)
        else:
            t = TaobaoScrawl()
            # d = t.get_all_shop(kw, 3)
            isOk = t.thread_enter(kw, 3)
            if isOk:
                # 读取json文件
                with codecs.open(kw+'.json', 'r') as f:
                    content = f.readlines()
                data = []
                for line in content:
                    data.append(json.loads(line))
                self.render('taobao.html', data=data)



        # self.render('taobao.html', d=d)


class TiebaHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('tieba_search.html', d='')

    def post(self):
        kw = self.get_argument('kw','')
        begin = self.get_argument('begin', '')
        end = self.get_argument('end','')
        d1 = TiebaScrawl()
        data = d1.get_data(kw, begin, end)
        d = []
        n = 0
        for i in data:
            print(i)
            temp = [i['url'].strip(), i['title'].strip(), str(n)]
            d.append(temp)
            n += 1
        self.render("tieba_search.html", d=d, n=n)

class BaikeCrawlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('doc.html', article='')

    def post(self):
        kw =self.get_argument('kw', '')
        go(kw)
        self.redirect('/doc')



def get_note():
    '''获取金山词霸每日一句'''
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content, note


class DocHandler(tornado.web.RequestHandler):
    def get_txtlist(self):
        li = os.listdir("static/documents/")
        print(li)
        txtlist = []
        for file in li:
            filename = os.path.splitext(file)[-2]
            filepath = os.path.join("static/documents/", file)
            if os.path.splitext(file)[-1] in ['.txt']:
                txtlist.append((filepath, filename))
        return txtlist

    def get(self):
        txtlist = self.get_txtlist()
        article = []
        for i in txtlist:
            with open(i[0], 'r') as f:
                content = f.readlines()
                article.append((i[1], content))
        print(txtlist)
        self.render('doc.html', article=article)


class UploadAvatarHandler(tornado.web.RequestHandler):
    def get_imglist(self):
        li = os.listdir("static/images/")
        imglist = []
        for i in li:
          fullName = os.path.join("static/images/", i)
          if os.path.splitext(fullName)[-1] in [".jpeg", ".gif", ".png", '.jpg']:
              imglist.append(fullName)
        return imglist

    def get(self):
        '''
        页面显示图片函数
        :return:
        '''
        note = get_note()
        urllist=self.get_imglist()
        urllist = sorted(urllist)
        urllist = urllist[::-1]
        print(urllist)
        rows = len(urllist) // 4
        columns = len(urllist) % 4
        print(len(urllist))
        self.render("avatar.html",
            note = note,
            urllist=urllist,
            rows=rows,
            columns=columns)

    def post(self):
        '''
        上传文件函数
        目前支持图片， txt文档
        :return:
        '''
        import os
        import imghdr

        img_data = self.request.files.get("user_avatar", "")
        # print(img_data)
        print(img_data[0].keys())
        # print(img_data[0]["filename"])
        print(img_data[0]["content_type"])
        filename, txt_ext= os.path.splitext(os.path.split(img_data[0]["filename"])[-1])
        ext = imghdr.what('', h=img_data[0]['body']) # 获取图片的后缀名
        print(filename)
        print(ext)
        if ext in ['png', 'jpeg', 'jpg', 'gif', 'bmp']:
            filepath = "static/images/" + filename + '.' + ext
            with open(filepath, "wb") as f:
                f.write(img_data[0]["body"])
        elif txt_ext in ['.txt']:
            print(txt_ext)
            filepath = "static/documents/" + filename + txt_ext
            with open(filepath, 'w') as f:
                f.write(img_data[0]['body'])
        else:
            print('无法上传')
        self.redirect("/uploadfile")

# 大华新闻分析
class DahuaHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dahuaSpider.html")

# 大华新闻页面
class DahuaNewsHandler(tornado.web.RequestHandler):
    def get(self):
        import pandas as pd
        import json
        with open("dahua.json", "r") as f:
            content = f.read()
        # 转换为列表字典
        dict_list = [json.loads(i.strip()) for i in content.split('\n')[:-1]]
        df1 = dict_list
        """
        #转换为pandas DataFrame 格式
        df = pd.DataFrame(dict_list)
        # 字符串转时间格式
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
        # 按日期进行排序
        df1 = df.sort_values(by=["date"], ascending=False)
        """
        self.render("dahuanews.html",
                    df1=df1[:50])

class HwHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("huaweiNews.html")

class HkHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("hikvision&dahua.html")



#工资查询
# 计算工资
def wage(h):
    #加班时数
    #h = float(input('请输入加班时数: '))
    #基本工资
    base_wage = 4050
    #岗位补助
    worker_wage = 300
    #高温补助
    tem_wage = 190
    #每小时工资
    hour_wage = base_wage/26/8
    #加班工资
    overtime_wage = hour_wage*h

    #------以下为扣款部分--------
    #养老金
    old_age_pay = 245
    #医保
    medical_pay = 61
    #水电
    water_pay = 30
    #待业
    await_pay = 15
    #税前总工资
    total_wage = base_wage + \
                    overtime_wage + \
                    worker_wage + \
                    tem_wage - \
                    old_age_pay - \
                    medical_pay - \
                    water_pay - \
                    await_pay
    #计算个人所得税
    if total_wage > 5000:
        #高于5000，超出部分按3%计算所得税
        tax_pay = (total_wage-5000)*0.03
    else:
        tax_pay = 0
    #扣除税后实际工资
    realiy_wage = total_wage-tax_pay
    return h, total_wage, realiy_wage, tax_pay


class WageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("wage.html",h="", w="", r="", t="")

    def post(self):
        hour = self.get_argument("hour", "")
        h, w, r, t = wage(float(hour))
        kw={
        "h":h,
        "w":w,
        "r":r,
        "t":t,
        }
        self.render("wage.html", **kw)

