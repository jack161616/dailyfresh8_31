#*-*coding:utf-8-*-
from django.shortcuts import render,redirect
from models import *
from django.core.paginator import Paginator,Page
from df_user import user_decorator
from django.http import HttpResponse
from df_cart.models import *


def index(request):
    typelist=TypeInfo.objects.all()
    type0=typelist[0].goodsinfo_set.order_by('-id')
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')
    type1 = typelist[1].goodsinfo_set.order_by('-id')
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')
    type2 = typelist[2].goodsinfo_set.order_by('-id')
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')
    type3 = typelist[3].goodsinfo_set.order_by('-id')
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')
    type4 = typelist[4].goodsinfo_set.order_by('-id')
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')
    type5 = typelist[5].goodsinfo_set.order_by('-id')
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')

    print '------------验证-------------'
    print type0[1]
    print 'cart_count:',type0[1].cartinfo_set.count()   #查的是该商品的购物车有这类几种,值始终为1
    print 'cart_count2:', cart_count(request)     #查的是该用户的购物车有几类商品.

    context={'title':'首页',
             'type0':type0, 'type01':type01,
             'type1': type1, 'type11': type11,
             'type2': type2, 'type21': type21,
             'type3': type3, 'type31': type31,
             'type4': type4, 'type41': type41,
             'type5': type5, 'type51': type51,
             'cart_count':cart_count(request)
             }

    return render(request,'df_goods/index.html',context)

def list(request,tid,pindex,sort):
    # tid---title的分类,即品种分类, pindex---页码的第几页,  sort--排序的分类.
    typeinfo=TypeInfo.objects.get(pk=int(tid))
    news=typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort=='1':#默认,最新
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        # goods_list=typeinfo.goodsinfo_set.order_by('-id')
    elif sort=='2':#价格
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
        # goods_list = typeinfo.goodsinfo_set.order_by('-gprice')
    elif sort=='3':#人气,点击量
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator=Paginator(goods_list,10)
    page=paginator.page(int(pindex))
    context={'title':typeinfo.ttitle,
             'page':page,'paginator':paginator,
             'typeinfo':typeinfo,'sort':sort,
             'news':news,
             'cart_count':cart_count(request)
             }
    return render(request,'df_goods/list.html',context)


def detail(request,gid):
    #商品的id
    #goods=GoodsInfo.objects.filter(pk=int(gid))
    goods=GoodsInfo.objects.get(pk=int(gid))
    goods.gclick=goods.gclick+1
    goods.save()

    print '=============验证====detail================='
    print 'goods.gtype.ttitle:',goods.gtype
    good_id=GoodsInfo.objects.filter(gtype=1)
    print 'goods.gtype_id:',goods.gtype.goodsinfo_set.get(id=3)
    # type_id = GoodsInfo.gtype.get(id=1)
    # print 'type:',type_id
    print type(goods)
    print goods.gtitle
    # 注意filter和get返回的对象是不一样的.get返回的是单个对象,而filter返回的是一个列表性对象.
    # 所有取属性上就要如:goods[0].gtitle
    print '====================================='

    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context={'title':goods.gtype.ttitle,'g':goods,
             'news':news,'gid':gid,
             'cart_count':cart_count(request)
            }
    response =  render(request, 'df_goods/detail.html', context)
    # 记录最近浏览记录,在用户中心使用
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_id='%d'%goods.id
    if goods_ids!='':   #判断是否有浏览记录,如有则继续判断
        goods_ids1=goods_ids.split(',') #拆分为列表
        if goods_ids1.count(goods_id)>=1:   #如果商品已经被记录,则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)  #删除后置于列表第一个是为了让他处于浏览最新记录状态
        if len(goods_ids1)>=6: # 只保留最新5个浏览记录
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1) #重新拼接为字符串,
    else:
        goods_ids=goods_id #如果没有浏览记录,则直接添加
    response.set_cookie('goods_ids',goods_ids)

    print '===========验证==COOKIE======================'
    print 'goods_ids:',goods_ids
    print 'goods_id:',goods_id
    # print 'goods_id1:',goods_ids1
    print '=================================================='

    return response

#购物数量
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView,self).extra_context()
        context['title']='搜索'
        context['guest_cart']=1
        context['cart_count']=cart_count(self.request)
        return context















