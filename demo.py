# _*_ coding: utf-8 _*_
# @Time     : 2018/7/12 21:11
# @Author   : Ole211
# @Site     : 
# @File     : demo.py    
# @Software : PyCharm

# scrapy 常用命令
scrapy startproject tutorial(项目名称 ) # 创建一个scrapy 项目
scrapy list #列出当前目录可用的spider
scrapy crawl <spider> #运行spider
scrapy genspider <name> <domain>

# turorial 项目的文件
# scrapy.cfg 项目的配置文件
# items.py 容器 配置需要采集的字段  相当于一个dict
# piplines  管道  保存数据
# middlewares 中间键  对爬取的前后做处理， 比如修改 headers


scrapy.Spider

name #爬虫的名字， 必须唯一
start_urls #爬虫初始的url 列表
parse response #默认的处理函数

Requests 和 Response对象
# 每一个请求都是一个Requestd对象
# 请求完成之后会把response 对象发送给spider处理，
# url status headers body

# start_requests

# xpath 常用符号
#
# / 从根节点查找数据， /head/div
# // 从所有的文档里面查找
# @ 选取属性
#  text() 获取内容
# * 所以 //div[@*]  选取所有带属性的div, id, class


# 方法
# contains  模糊匹配， 包含 contains(@id, 'image')  选取id 属性的值包含image的节点
# text()

# css 符号
# * 通用元素选择器
# E 标签选择器  匹配E标签的元素
# . class 选择器 例如： .info 匹配所有的class 属性里面包含info的元素
# E[att='val'] 属性att的值val的E标签


