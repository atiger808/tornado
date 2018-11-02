# _*_ coding: utf-8 _*_
# @Time     : 2018/7/30 2:13
# @Author   : Ole211
# @Site     : 
# @File     : flash_libs.py    
# @Software : PyCharm

def flash(self, message, category='message'):
    """先调用flash"""
    flashes = self.session.get('_flashes', [])
    flashes.append((category, message))  #[('error', '保存失败'),('ok', '分类保存了')]
    self.session.set('_flashes', flashes)



def get_flashed_messages(self, with_categories=False, category_filter=[]):
    """后调用get_flashed_messages"""
    flashes = self.flashes
    if flashes is None:
        self.flashes = flashes = self.session.get('_flashes', [])
        del self.session['_flashes']
    if category_filter:
        flashes = list(filter(lambda f: f[0] in category_filter, flashes))
    if not with_categories:
        return [x[1] for x in flashes]
    return flashes



#   <!-- 消息闪现-->
# {% for category, message in get_flashed_messages(with_categories=True) %}
#         {% if category == 'error' %}
#         <p style="background-color:#ff003e"> {{ message }}</p>
#         {% elif category == 'success' %}
#         <p style="background-color: greenyellow">{{ message }}</p>
#         {% end %}
#
#  {% end %}

# <!-- 过滤闪现 -->
#         {% for message in get_flashed_messages(category_filter=['error']) %}
#             <p style="background-color: red">{{ message }}</p>
#         {% end %}
#         {% for message in get_flashed_messages(category_filter=['success']) %}
#             <p style="backgound-color: green">{{ message }}</p>
#         {% end %}
#
# <!-- ajax 弹窗 消息闪现-->
# {% for category, message in get_flashed_messages(with_categories=True) %}
#         {% if category == 'error' %}
#             <script type="text/javascript">
#                 swal({
#                     'title': '错误',
#                     'text': '{{ message }}',
#                     'type': 'error',
#                     'showCancelButton': false,
#                     'showConfirmButton': false,
#                     'timer': 2000
#                 })
#             </script>
#         {% elif category == 'success' %}
#             <script type="text/javascript">
#                 swal({
#                     'title': '正确',
#                     'text': '{{ message }}',
#                     'type': 'success',
#                     'showCancelButton': false,
#                     'showConfirmButton': false,
#                     'timer': 2000
#                 })
#             </script>
#         {% end %}
# {% end %}
