# --*-- coding: utf-8 --*--
# @Time     : 2018/7/15 0:26
# @Author   : Ole211
# @Site     :
# @File     : taobao.py
# @Software : PyCharm
import requests
import sys
# 解析url 用的类库
#Python2
# import urllib
# from urlparse import urlparse
# python3
# from urllib.parse import urlparse
# import urllib.request
import re
import json
import codecs
import pandas as pd
import csv
from bs4 import BeautifulSoup as bs
import threading
import multiprocessing
from run_time import run_time as run



headers = {
'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'upgrade-insecure-requests':'1',
}

class TaobaoScrawl(object):
    """初始化"""
    def __init__(self):
        self.headers = headers
        self.path = './'
        self.pageurl = 'https://s.taobao.com/search?q='
        self.idurl = 'https://item.taobao.com/item.htm?id='
        self.urls = []
        self.nums = 0
    def parse_page(self,url):
        """网页解析"""
        res = requests.get(url, headers = self.headers)
        res.encoding = 'utf-8'
        if res.status_code == 200:
            return res
        return None

    """获取商品信息"""
    def page(self, url):
        item = {}
        res = self.parse_page(url)
        res.encoding = 'gbk'
        pattern = re.compile('<title>(.*?)</title>')
        title = re.findall(pattern, res.text)[0]
        if title[-3:] == u'淘宝网':
            pattern2 = re.compile('<em class="tb-rmb-num">(.*?)</em>')
            price = re.findall(pattern2, res.text)[0]
            item['title'] =title
            item['price'] = price
            item['url'] = url
        return item

    """获取单个页面商品链接"""
    def get_one_page_links(self, kw, pn):
        links = []
        key = kw
        url = self.pageurl + key + '&search_type=item&s=' + str(44*pn)
        res = self.parse_page(url)
        pattern = re.compile('"nid":"(.*?)"')
        allid = re.findall(pattern, res.text)
        for urlid in allid:
            thisurl = self.idurl + urlid
            links.append(thisurl)
        return links


    """获取所有链接"""
    def get_all_links(self, kw, n):
        for pn in range(n):
            self.urls.extend(self.get_one_page_links(kw, pn))
            self.nums = len(self.urls)

    """获取所有商品商品信息"""
    def get_all_shop(self, kw, n):
        data = []
        for pn in range(n):
            links = self.get_one_page_links(kw, pn)
            for url in links:
                print(url)
                item = self.page(url)
                if item:
                    data.append(item)
        return data

    """写入csv文件"""
    def writer_csv(self, kw, link):
        shop = self.page(link)
        if shop:
            items = []
            for k, v in shop.items():
                items.append(v)
            with open(self.path + kw+'.csv', 'a') as csvfile:
                f = csv.writer(csvfile)
                f.writerow(items)

    def save_json(self, kw, item):
        if item:
            with codecs.open(kw+'.json', 'a', encoding='utf-8') as f:
                content = json.dumps(item, ensure_ascii=False) + '\n'
                f.write(content)
                print('Save success')
        else:
            print('Empy data')




    """下载入口"""
    def download(self, kw, n):
        for pn in range(n):
            self.urls.extend(self.get_one_page_links(kw, pn))
        threads = [threading.Thread(target=self.writer_csv, args=(kw, link,)) for link in self.urls]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

############################################

    def taobao_main(self,kw,offset):
        print('正在解析第{}页'.format(offset))
        links = self.get_one_page_links(kw, offset)
        for link in links:
            print('正在下载：{}'.format(link))
            item = self.page(link)
            self.save_json(kw, item)

    @run
    def thread_enter(self, kw, n):
        '''
        淘宝商品多线程下载入口
        :param kw:
        :param n:
        :return:
        '''
        threads = [threading.Thread(target=self.taobao_main, args=(kw, offset )) for offset in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return True

######################################################################################
# 贴吧爬虫
url = 'http://tieba.baidu.com/f?kw='

class TiebaScrawl(object):
    def __init__(self):
        self.server = url
        self.nums = 0

    def parse_page(self, target):
        """网页解析"""
        res = requests.get(url=target, headers = headers)
        if res.status_code == 200:
            return res.text
        return None

    def get_one_page_data(self, target):
        """获取单个页面数据"""
        html = self.parse_page(target)
        pattern = re.compile('<div class="t_con cleafix">.*? title="回复">(.*?)</span>'+
                          '.*? href="/p/(.*?)" title="(.*?)" target='+
                          '.*?target="_blank">(.*?)</a></span>'+
                        '.*?title="创建时间">(.*?)</span>.*?</div>', re.S)
        allid = re.findall(pattern, html)
        pagedata = []
        print(allid)
        for i in allid:
            page = {}
            page['replynum'] = int(i[0])
            page['url'] = self.server + i[1]
            page['title'] = i[2]
            page['author'] = i[3]
            page['createtime'] = i[4]
            pagedata.append(page)
        # print(pagedata)
        return pagedata

    def get_data(self, name, begin_page, end_page):
        """获取全部数据"""
        data = []
        kw = name
        self.nums = int(end_page) - int(begin_page)
        for i in range(int(begin_page), int(end_page)):
            pn = (i-1) * 50
            target = self.server + kw + '&pn=' +str(pn)
            pagedata = self.get_one_page_data(target)
            data.extend(pagedata)
        return data

    def download(self, name, begin_page, end_page):
        """下载入口"""
        total_data = []
        kw = name
        self.nums = end_page - begin_page
        print('开始下载', name)
        for i in range(begin_page, end_page):
            pn = (i-1) * 50
            target = self.server + kw + '&pn=' + str(pn)
            pagedata = self.get_one_page_data(target)
            total_data.extend(pagedata)
            sys.stdout.write('  已经下载; %.3f%%' % float(i/self.nums*100) + '\r')
            sys.stdout.flush()
        df = pd.DataFrame(total_data)
        df.to_csv('./' + kw + '.csv')
        print('下载完成')
        return total_data

if __name__ == '__main__':
    kw = raw_input('输入贴吧名称：')
    begin = int(raw_input('起始页：'))
    end = int(raw_input('结束页：'))
    d = TiebaScrawl()
    data = d.get_data(kw, begin, end)
    for i in data:
        print(i)
    # d1.download(name, begin, end)
    # print(d1.parse_page('http://tieba.baidu.com/f?kw=c&ie=utf-8&pn=100'))
    # print(d1.get_one_page_data('http://tieba.baidu.com/f?kw=python&ie=utf-8&pn=100'))
    #
    # kw = input("input item: ")
    # n = int(input('input page counts: '))
    # t = TaobaoScrawl()
    # isOk = t.thread_enter(kw, n)
    # if isOk:
    #     print('ok')
