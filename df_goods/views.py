#*-*coding:utf-8-*-
from django.shortcuts import render,redirect
from models import *
from django.core.paginator import Paginator,Page


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

    context={'title':'首页',
             'type0':type0, 'type01':type01,
             'type1': type1, 'type11': type11,
             'type2': type2, 'type21': type21,
             'type3': type3, 'type31': type31,
             'type4': type4, 'type41': type41,
             'type5': type5, 'type51': type51,
             }

    return render(request,'df_goods/index.html',context)

def list(request,tid,pindex,sort):
    # tid---title的分类,即品种分类, pindex---页码的第几页,  sort--排序的分类.
    typeinfo=TypeInfo.objects.get(pk=int(tid))
    news=typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort=='1':#默认,最新
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort=='2':#价格
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort=='3':#人气,点击量
        goods_list=GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator=Paginator(goods_list,10)
    page=paginator.page(int(pindex))
    context={'title':typeinfo.ttitle,
             'page':page,'paginator':paginator,
             'typeinfo':typeinfo,'sort':sort,
             'news':news,
             }
    return render(request,'df_goods/list.html',context)

def detail(request,gid):
    #商品的id
    #goods=GoodsInfo.objects.filter(pk=int(gid))
    goods=GoodsInfo.objects.get(pk=int(gid))
    goods.gclick=goods.gclick+1
    goods.save()

    print '=============验证====================='
    print goods.gtype.ttitle
    print type(goods)
    print goods.gtitle
    # 注意filter和get返回的对象是不一样的.get返回的是单个对象,而filter返回的是一个列表性对象.
    # 所有取属性上就要如:goods[0].gtitle
    print '====================================='

    news=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context={'title':goods.gtype.ttitle,'g':goods,
             'news':news,'gid':gid,
            }

    return render(request,'df_goods/detail.html',context)




















