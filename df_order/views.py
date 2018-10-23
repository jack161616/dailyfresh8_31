#*-*coding=utf-8*-*

from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from models import *
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from django.db import transaction
from datetime import datetime
from decimal import Decimal

@user_decorator.login
def order(request):
    #查询用户对象
    user=UserInfo.objects.get(id=request.session['user_id'])
    #根据提交查询购物车信息
    get=request.GET
    cart_ids=get.getlist('cart_id')
    cart_ids1=[int(item) for item in cart_ids]
    carts=CartInfo.objects.filter(id__in=cart_ids1)
    # print '===========order====呀演的======'
    # cart2=CartInfo()
    # cart2.user_id=1
    # cart2.count=3
    # cart2.goods_id=4
    # cart2.save()
    # order3=OrderInfo()
    # order3.user_id=3
    # order3.oaddress='dddd'
    # order3.oid=3333333
    # order3.otatal=456.34
    # order3.odata=datetime.now()
    # order3.oIsPay=True
    # order3.save()
    #
    # print '=================================='
    #构造传递到模板中的数据
    context={'title':'提交订单',
             'page_name':1,
             'carts':carts,
             'user':user,
             'cart_ids':','.join(cart_ids),
             }
    return render(request,'df_order/place_order.html',context)

'''
事务:一旦操作失败则全部退回
1.创建订单对象
2.判断商品的库存
3.创建详单对象
4.修改商品库存
5.删除购物车
'''
# @transaction.atomic()
# @user_decorator.login
# def order_handle(request):
#     tran_id=transaction.savepoint()
#     #接收购物车编号
#     cart_ids=request.POST.get('cart_ids')
#     try:
#         #创建订单对象
#         order=OrderInfo()
#         now=datetime.now()
#         uid=request.session['user_id']
#         order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
#         order.user_id=uid
#         order.odate=now
#         order.oaddress=request.POST.get('adress')
#         order.ototal=0
#         order.save()
#         #创建详单对象
#         cart_ids1=[int(item) for item in cart_ids.split(',')]
#         total=0
#         for id1 in cart_ids1:
#             detail=OrderDetailInfo()
#             detail.order=order
#             #查询购物车信息
#             cart=CartInfo.objects.get(id=id1)
#             # 判断商品库存
#             goods=cart.goods
#             if goods.gkucun>=cart.count: #如果库存大于购买数量
#                 # 减少商品库存
#                 goods.gkucun=cart.goods.gkucun-cart.count
#                 goods.save()
#                 # 完善详单信息
#                 detail.goods_id=goods.id
#                 price=goods.gprice
#                 detail.price=price
#                 count=cart.count
#                 detail.count=count
#                 detail.save()
#                 total=total+price*count
#                 #删除购物车数据
#                 cart.delete()
#             else:#如果库存小于购买数量
#                 transaction.savepoint_rollback(tran_id)
#                 return redirect('/cart/')
#                 # return HttpResponse('no')
#         #保存总价
#         order.ototal=total+10
#         order.save()
#         transaction.savepoint_commit(tran_id)
#     except Exception as e:
#         print '========================%s'%e
#         transaction.savepoint_rollback(tran_id)
#
#     return redirect('/user/order/')

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id=transaction.savepoint()
    #接收购物车编号
    cart_ids=request.POST.get('cart_ids')#5,6
    try:
        #创建订单对象
        order=OrderInfo()
        now=datetime.now()
        uid=request.session['user_id']
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        # print order.oid
        order.odata=now
        order.oaddress=request.POST.get('address')
        order.otatal=0
        print '=============order_handle=================='
        print 'user:',uid,'order:',order.oid,order.user,order.user_id,order.odata,order.oaddress
        order.save()
        user2=UserInfo()
        user2.uname='jack171717'
        # user2.save()
        print '=============order_handle===jiesu==============='
        order.save()
        #创建详单对象
        cart_ids1=[int(item) for item in cart_ids.split(',')]
        total=0
        for id1 in cart_ids1:
            detail=OrderDetailInfo()
            detail.order=order
            # 查询购物车信息
            cart=CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods=cart.goods
            if goods.gkucun>=cart.count:#如果库存大于购买数量
                # 减少商品库存
                goods.gkucun=cart.goods.gkucun-cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id=goods.id
                price=goods.gprice
                detail.price=price
                count=cart.count
                detail.count=count
                detail.save()
                total=total+price*count
                #删除购物车数据
                cart.delete()
            else:#如果库存小于购买数量
                # transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
                # return HttpResponse('no')
        # 保存总价
        order.ototal=total+10
        order.save()
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '================%s'%e
        transaction.savepoint_rollback(tran_id)

    # return HttpResponse('ok')
    return redirect('/user/order/')












