#*-*coding:utf-8*-*
from django.shortcuts import render,redirect
from models import *
from df_goods.models import *
from django.http import JsonResponse,HttpResponseRedirect
from df_user import user_decorator

@user_decorator.login
def cart(request):
    uid=request.session['user_id']
    carts=CartInfo.objects.filter(user_id=uid)
    print '=================验证==carts=========='
    print 'carts:',carts
    print '=================验证==over=========='
    context={'title':'购物车','page_name':1,
             'carts':carts
             }
    return render(request, 'df_cart/cart.html', context)

@user_decorator.login
def add(request,gid,count):
    #用户uid购买了gid商品,数量为count
    uid=request.session['user_id']
    gid=int(gid)
    count=int(count)
    #查询购物车是否已经有此商品,如果有则数量增加,如果没有则新增,
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    carts1 = CartInfo.objects.filter(user=int(uid), goods=int(uid))
    print '========add_cart=================='
    print 'carts:',carts[0]
    print 'carts_count:',carts[0].count
    print 'carts1:',carts1[0]
    print 'carts1_goods:',carts1[0].goods.gjianjie
    print '========add_cart=================='
    if len(carts)>=1:
        cart=carts[0]
        cart.count=cart.count+count
    else:
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
    cart.save()
    #如果是ajax请求则返回json,否则转向购物车
    if request.is_ajax():
        count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
        data={'cart_id':cart.id,'count':count}
        return JsonResponse(data)
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request,cart_id,count):
    count1=1
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count
        cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

@user_decorator.login
def delete(request,cart_id):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)
