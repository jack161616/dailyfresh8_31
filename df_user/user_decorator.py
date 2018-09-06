#*-*coding:utf-8*-*

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
        #目的在于多了下面这一层,即返回登录页面,并且记住原先url地址.
            red=HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun