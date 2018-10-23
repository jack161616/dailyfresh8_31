#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from . import user_decorator
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator,Page

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

    print '==================验证--login-handle-======================-'
    #此处只是作为学习,分清get与filter所得到的对象不一样.filter返回的是列表,get则返回一个对象
    users2 = UserInfo.objects.get(uname=uname)
    print 'user:',users,',len_user:',len(users)
    print 'user2:',users2
    print users[0].upwd
    print users2.upwd
    print uname
    # users2.delete()  #delete 在对于 users和users2的使用结果不同.
    # print 'delete_users2_pwd:',users2.upwd
    print '==========================================================='

    #判断:如果未查到用户名则用户名错,如果查到则判断密码是否正确,正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')  # 承接登录验证的 转向 url地址.
            # print 'url:',url
            red=HttpResponseRedirect(url)
            #成功后删除转向地址,防止以后直接登录造成转向,,设置cookie由response设置.
            red.set_cookie('url','',max_age=-1)
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname

            print '=============验证====session============='
            print 'session["user_id"]:',request.session['user_id']
            print 'session["user_name"]:', request.session['user_name']
            print '=============验证====完毕============='
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
    # return HttpResponseRedirect('/')
    return redirect('/')

@user_decorator.login
def info(request):
    user=UserInfo.objects.get(id=request.session['user_id'])

    print '==========验证===user==================='
    #只是为了验证filter与get得到的user对象取值一样.
    user_uname = user.uname
    user2=UserInfo.objects.filter(uname=user_uname)
    print 'user:',user.uname
    print 'user2:',user2[0].uname,user2[0].uaddress

    goods22=GoodsInfo.objects.get(id=2)
    type11=goods22.gtype.goodsinfo_set.get(id=2)
    print 'goods22:',goods22
    print 'type11:',type11
    print '==========验证===完毕==================='

    # user_name=UserInfo.objects.get(id=request.session['user_id']).uname
    # user_address=
    #最近浏览
    goods_list=[]
    goods_ids=request.COOKIES.get('goods_ids','')
    if goods_ids != '':
        goods_ids1=goods_ids.split(',') #分成列表[,]
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id))) #这边就返回了商品对象

    print 'goods_list:',goods_list

    content={'title':'用户中心','user':user,
             'page_name':1,'goods_list':goods_list,
             }
    return render(request,'df_user/user_center_info.html',content)

@user_decorator.login
def order(request,pindex):
    order_list = OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    paginator = Paginator(order_list, 2)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))

    context = {'title': '用户中心',
               'page_name': 1,
               'paginator': paginator,
               'page': page, }
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    print 'session',request.session['user_id']
    user = UserInfo.objects.get(id=request.session['user_id'])
    print type(user)
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context={'title':'用户中心','user':user,'page_name':1}
    return render(request,'df_user/user_center_site.html',context)
    # return redirect(request.get_full_path())
    # return HttpResponseRedirect(request.COOKIES.get('url','/'))














