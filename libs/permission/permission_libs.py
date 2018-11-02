# _*_ coding: utf-8 _*_
# @Time     : 2018/7/23 23:57
# @Author   : Ole211
# @Site     : 
# @File     : permission_libs.py    
# @Software : PyCharm

from models.permission.permission_model import Role, Permission, Menu, Handler
from models.account.account_user_model import User
from libs.flash.flash_libs import flash
def permission_manage_list_lib(self):
    """01权限管理页面函数"""
    roles = Role.all()
    permissions = Permission.all()
    menus = Menu.all()
    handlers = Handler.all()
    users = User.all()

    #研发员工
    dev_role = Role.by_name('研发员工')
    dev_users = dev_role.users if dev_role else []
    return roles, permissions, menus, handlers, users, dev_users

def add_role_lib(self, name):
    """02添加角色"""
    role = Role.by_name(name)
    if role is not None:
        flash(self, "角色添加失败", 'error')
        return
    role = Role()
    role.name = name
    self.db.add(role)
    self.db.commit()
    flash(self, "角色添加成功", 'success')

def del_role_lib(self, roleid):
    """03删除角色"""
    role = Role.by_id(roleid)
    if role is None:
        flash(self, "角色删除失败", 'error')
        return
    self.db.delete(role)
    self.db.commit()
    flash(self, "角色删除成功", 'success')
    # flash(self, "角色删除失败", 'error')

def add_permission_lib(self, name, strcode):
    """04添加权限"""
    permission = Permission.by_name(name)
    if permission is not None:
        flash(self, "权限添加失败", 'error')
        return
    permission = Permission()
    permission.name = name
    permission.strcode = strcode
    self.db.add(permission)
    self.db.commit()
    flash(self, "权限添加成功", 'success')

def del_permission_lib(self, permissionid):
    """05删除权限"""
    permission = Permission.by_id(permissionid)
    if permission is None:
        flash(self, "权限删除失败", 'error')
        return
    self.db.delete(permission)
    self.db.commit()
    flash(self, "权限删除成功", 'success')

def add_menu_lib(self, name, permissionid):
    """06为菜单添加权限"""
    permission = Permission.by_id(permissionid)
    menu = Menu.by_name(name)
    if permission is None:
        return
    if menu is None:
        menu = Menu()
    menu.name = name
    menu.permission = permission
    self.db.add(menu)
    self.db.commit()

def del_menu_lib(self, menuid):
    """07删除菜单权限"""
    menu = Menu.by_id(menuid)
    if menu is None:
        return
    self.db.delete(menu)
    self.db.commit()

def add_handler_lib(self, name, permissionid):
    """08为处理器添加权限"""
    permission = Permission.by_id(permissionid)
    handler = Handler.by_name(name)
    if permission is None:
        return
    if handler is None:
        handler = Handler()
    handler.name = name
    handler.permission = permission
    self.db.add(handler)
    self.db.commit()

def del_handler_lib(self, handlerid):
    """09删除处理器权限"""
    handler = Handler.by_id(handlerid)
    if handler is None:
        return
    self.db.delete(handler)
    self.db.commit()

def add_user_role_lib(self, userid, roleid):
    """10为用户添加角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        return
    user.roles.append(role)
    self.db.add(user)
    self.db.commit()

def add_permission_role_lib(self, permissionid, roleid):
    """11为角色添加权限"""
    role = Role.by_id(roleid)
    permission = Permission.by_id(permissionid)
    if permission is None or role is None:
        return
    role.permissions.append(permission)
    self.db.add(role)
    self.db.commit()

def del_user_role_lib(self, userid):
    """12删除用户角色"""
    user = User.by_id(userid)
    if user is None:
        return
    # user.roles 是个列表 []列表清空
    # user.roles.remove(obj) 删除某一个对象
    # user.roles.pop() 弹出最后一个
    user.roles = []
    self.db.add(user)
    self.db.commit()

def add_user_dev_role_lib(self, userid, roleid):
    """13为用户添加角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        return
    user.roles.append(role)
    self.db.add(user)
    self.db.commit()

def del_user_dev_role_lib(self, userid, roleid):
    """14为用户删除角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        return
    user.roles.remove(role)
    self.db.add(user)
    self.db.commit()
