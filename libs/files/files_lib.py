# _*_ coding: utf-8 _*_
# @Time     : 2018/8/18 17:07
# @Author   : Ole211
# @Site     : 
# @File     : files_lib.py    
# @Software : PyCharm
from datetime import datetime
from string import printable
from uuid import uuid4
import json
from random import randint, choice
from tornado.concurrent import run_on_executor
from models.files.upload_file_model import Files
from libs.pagination.pagination_libs import  Pagination




def files_list_lib(self, page):
    """01文件列表"""
    page = int(page)
    items = self.db.query(Files).limit(MAX_PAGE).offset((page - 1) * MAX_PAGE).all()
    if page == 1 and len(items) < MAX_PAGE:
        total = len(items)
    else:
        total = self.db.query(Files).order_by(None).count()
    return Pagination(page, MAX_PAGE, total, items)

def upload_files_lib(self, upload_files):
    # [{'body': '2133333aaaa', 'content_type': u'text/plain', 'filename': u'a.txt'},
    # {'body': 'aaaaaaa11111', 'content_type': u'text/plain', 'filename': u'b.txt'}]
    """02文件上传到服务器文件夹"""
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None


def  save_file(self, upload_file):
    """保存单个文件"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'jpeg', 'bmp', 'mp4', 'ogg', 'mp3', 'txt', 'png']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确'}
    uuidname = str(uuid4()) + '.%s' % files_ext
    # 'asdsdsd.txt'  'sdsadafa.jpg'
    # 文件大小tornado已经自动进行判断了， 所以不进行判断了,tornado 是单进程的
    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://www.shuaibin.wang:8888/images/' + old_file.uuid
        return {'status': True, 'msg': '文件保存成功(文件已经在硬盘上)', 'data': file_path}

    url = 'files/' + uuidname
    # 保存到服务器硬盘
    with open(url, 'wb') as f:
        f.write(file_content)
    # 保存数据库
    file_name = upload_file['filename']
    files = Files()
    files.filename = file_name
    files.uuid = uuidname
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.upload_time = datetime.now()
    files.file_hash = upload_file['body']
    # files.user_id = self.current_user.id
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    file_path = 'http://www.shuaibin.wang:8888/images/' + files.uuid
    return {'status': True, 'msg': '文件保存成功', 'data': file_path}

def files_list_del_file_lib(self, uuid):
    """从硬盘上彻底删除文件"""
    files = Files.by_uuid(uuid)
    self.db.delete(files)
    self.db.commit()

def files_message_lib(self, uuid):
    """03文件详情页"""
    return Files.by_uuid(uuid)


MAX_PAGE = 2

def file_page_lib(self, page):
    """04文件分页列表"""
    # 文件列表
    files = self.current_user.users_files
    print(files)# lazy='dynamic' 惰性查询，打印的是查询语句
    files_page = get_page_list(int(page), files, MAX_PAGE)
    # 回收站文件列表
    files_del = self.current_user.users_files_del
    return files_page, files_del

def get_page_list(current_page, content, MAX_PAGE):
    """04分页算法"""
    start = (current_page - 1) * MAX_PAGE
    end = start + MAX_PAGE

    split_content = content[start:end]
    total = content.count()
    count = total/MAX_PAGE
    if total % MAX_PAGE != 0:
        count += 1

    pre_page = current_page - 1
    next_page = current_page + 1

    if pre_page == 0:
        pre_page = 1
    if next_page > count:
        next_page = count

    if count < 5:
        pages = [p for p in xrange(1, count+1)]

    elif current_page <= 3:
        pages = [p for p in xrange(1, 6)]

    elif current_page >= count - 2:
        pages = [p for p in xrange(count-4, count+1)]

    else:
        pages = [p for p in xrange(current_page -2, current_page + 3)]

    return {
        'split_content': split_content,
        'count': count,
        'pre_page': pre_page,
        'next_page': next_page,
        'current_page': current_page,
        'pages': pages
    }



#-----------------------------分享链接处理器--(可以用另一个用户登录后分享文件)-----------------------------
def create_sharing_links_lib(self, file_uuid):
    """001创建分享链接"""
    # 生成redis键
    uu = str(uuid4())
    # 生成4位提取密码
    password = ''.join([choice(printable[:62]) for i in xrange(4)])
    # 创建字典
    redis_dict = {
        'user': self.current_user.name,
        'file_uuid': file_uuid,
        'password': password,
    }
    # 序列化字典
    redis_json = json.dumps(redis_dict)
    # 保存到redis中
    self.conn.setex('sharing_links:%s' % uu, redis_json, 500)
    return 'http://www.shuaibin.wang:8888/files/files_auth_sharing_links?uuid=%s' %uu, password

def get_username_lib(self, uu):
    """001获取分享者姓名"""
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回过期
    if redis_json is None:
        return {'status': False, 'msg': '分享已经过期', 'username': ''}
    # 如果有反序列化， 返回用户名
    redis_dict = json.loads(redis_json)
    return {'status': True, 'msg': '', 'username': redis_dict['user']}

def get_sharing_files_lib(self, uu, password):
    """002使用密码验证分享里链接"""
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期
    if redis_json is None:
        return {'status': False, 'msg': '分享已经过期', 'username': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户提交的密码与redis保存的密码
    if password == redis_dict['password']:
        # 对比成功， 密码保存当前用户的session
        self.session.set('sharing_links_password', password)
        # 返回分享链接
        links = '/files/files_sharing_list?uuid=%s' % uu
        return {'status': True, 'msg': '分享1111成功！', 'links': links, 'username': ''}
    return {'status': False, 'msg': '分享密码输入错误', 'username': redis_dict['user']}

def files_sharing_list_lib(self, uu):
    """003查看分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid 不存在', 'data': ''}
    # 获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        # 如果没有密码重新获取链接
        return {'status': False, 'msg': '请重新获取链接', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期， 并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有, 反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': Fasle, 'msg': '您没有获得这个文件的链接','data': ''}
    # 返回文件
    files = Files.by_uuid(redis_dict['file_uuid'])
    return {'status': True, 'msg': '分享成功', 'data': [files], 'uuid': uu}

def save_sharing_files_lib(self, uu):
    """004保存分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    # 获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        # 如果没有密码重新获取链接
        return {'status': False, 'msg': '没有权限', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期， 并删除session
    if redis_json is None:
        del self.session['sharing_links_passwrod']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等， 提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 把文件保存到当前用户
    files = Files.by_uuid(redis_dict['file_uuid'])
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    return {'status': True, 'msg': '保存成功', 'data': ''}
#-----------------------------分享链接处理器-----------------------------

#-------------------------------回收站接口----------------------------
def del_files_lib(self, uuid):
    """001删除到回收站"""
    files = Files.by_uuid(uuid)
    files.files_users.remove(self.current_user)
    files.files_users_del.append(self.current_user)
    self.db.add(files)
    self.db.commit()

def del_final_files_lib(self, uuid):
    """002彻底删除"""
    files = Files.by_uuid(uuid)
    files.files_users_del.remove(self.current_user)
    self.db.add(files)
    self.db.commit()

def recovery_files_lib(self, uuid):
    """003从回收站恢复"""
    files = Files.by_uuid(uuid)
    files.files_users_del.remove(self.current_user)
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
# -----------------------------回收站接口结束-----------------------------

import time
@run_on_executor
def files_download_lib(self, uuid):
    filepath = 'files/%s' % uuid
    self.set_header('Content-Type', 'application/octet-stream')
    self.set_header('Content-Disposition', 'attachment; filename=%s' % uuid )
    with open(filepath, 'rb') as f:
        while 1:
            data = f.read(1024 * 5)
            print(len(data))
            if  not data:
                break
            self.write(data)
            self.flush()
            time.sleep(1)
    self.finish()
