#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect


def register(request):
    context={'title':'用户注册'}
    return render(request,'df_user/register.html',context)

def register_handle(request):
    #接收用户输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    #判断两次密码
    if upwd!=upwd2:
        return redirect('/user/register/')
    #密码加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()
    #注册成功,转到登录页面
    return redirect('/user/login/')

def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname')
    context={'title':'用户登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'df_user/login.html',context)

def login_handle(request):
    #接收请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    #根据用户名查询对象
    users=UserInfo.objects.filter(uname=uname)

    print '-------验证-----------'
    users2 = UserInfo.objects.all()
    print users
    print 'user2:',users2
    print users2[0]
    print users[0].upwd
    print uname
    #判断:如果未查到用户名则用户名错,如果查到则判断密码是否正确,正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')
            red=HttpResponseRedirect(url)
            #成功后删除转向地址,防止以后直接登录造成转向
            red.set_cookie('url','',max_age=-1)
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red

        #用户名对,密码错的情况
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            #ajax 只作为前段的判断,显现,  而django才是作为后面的密码用户名验证.判断是否正确,
            #然后返回json格式给模版,进而又回到模版出进行判断显现出来
            return render(request,'df_user/login.html',context)

    else:
        context = {'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

def info(request):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    #最近浏览
    goods_list=[]
    goods_ids=request.COOKIES.get('goods_ids','')


    return render(request,'df_user/user_center_info.html')

def order(request):
    return render(request,'df_user/user_center_order.html')

def site(request):
    return render(request,'df_user/user_center_site.html')















