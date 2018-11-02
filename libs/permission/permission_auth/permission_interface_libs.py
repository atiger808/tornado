# _*_ coding: utf-8 _*_
# @Time     : 2018/7/27 0:32
# @Author   : Ole211
# @Site     : 
# @File     : permission_interface_libs.py    
# @Software : PyCharm

import functools
from models.permission.permission_model import Handler, Menu

obj_model = {
    "handler": Handler,
    "menu": Menu
}



class PermissionAuth(object):
    def __init__(self):
        self.user_permission = set()
        self.obj_permission = ''

    def permission_auth(self, user, name, types, model):
        # 获取当前用户的权限
        print'=====permission_auth======'
        roles = user.roles
        if roles is None:
            return
        for role in roles:
            for permission in role.permissions:
                self.user_permission.add(permission.strcode)

        # 获取handler 权限
        handler =model[types].by_name(name)
        if handler is None:
            return
        permission = handler.permission
        self.obj_permission = permission.strcode
        #如果hadnler 对应的权限存在用户的所有权限集合中， 返回True
        print('-'*50)
        print(self.user_permission)
        print(self.obj_permission)
        print('-' * 50)
        if self.obj_permission in  self.user_permission:
            return True
        return False


# 带参数的装饰器, 删除权限验证
def handler_permission(handlername, types):
    """

    :param handlername:
    :param types:
    :return:
    例：
        @handler_permission('DelPermissionHandler', 'handler')
    """
    def func(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if PermissionAuth().permission_auth(self.current_user, handlername, types, obj_model ):
                return method(self, *args, **kwargs)
            else:
                self.write("没有删除角色的权限")
        return wrapper
    return func

def menu_permission(self, menuname, types):
    if PermissionAuth().permission_auth(self.current_user, menuname, types, obj_model):
        return True
    return False

