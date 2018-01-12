# -*- coding: <utf8> -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Ticket
import datetime, json


def check(sn,pwd):
    
    verified = False
    try:
        ticket = Ticket.objects.get(sn=sn)
    except :
        msg = "券号不存在"
    else:
        if ticket.pwd != pwd:
            msg = "密码错误"
        elif ticket.actived != True:
            msg = "此券尚未激活"
        elif ticket.date_effective > datetime.date.today():
            msg = "此券有效期尚未开始"
        elif ticket.date_expire < datetime.date.today():
            msg = "此券已经失效，有效期至" + ticket.date_expire.isoformat()
        elif ticket.date_use != None:
            msg = "此券已于 " + timezone.make_naive(ticket.date_use).isoformat(' ') + " 使用"
        else:
            verified = True
            msg = ticket.get_product_display()
    return verified,msg

def index(request):
    return render(request,'coupon/verify.html')
def indexsn(request,sn):
    return render(request,'coupon/verify.html',{'sn':sn})

def verify(request):
    
    verified = False
    sn = ''
    msg = "非法访问"
    if request.method == 'POST':
        try:
            sn = request.POST['sn']
            pwd = request.POST['pwd']
        except:
            msg = "网络错误"
        else:
            verified,msg = check(sn,pwd)
    if request.is_ajax():
        return HttpResponse(json.dumps({
            'verified':verified,
            'msg':msg
            }
                                       )
                            )
    else:                   
        if verified:        
            return render(request,'coupon/order.html',{
                'sn':sn,
                'pwd':pwd,
                'good':msg
                })
        else:
            return render(request,'coupon/verify.html',{
                'sn':sn,
                'error_message':msg
                })

def order(request):
    
        verified = False
        if request.method == 'POST':
            try:
                sn = request.POST['sn']
                pwd = request.POST['pwd']
                name = request.POST['name']
                phone = request.POST['phone']
                address = request.POST['address']
                comments = request.POST['comments']
            except:
                msg = "网络错误"
            else:
                verified,msg = check(sn,pwd)
        if verified:
            try:
                ticket = Ticket.objects.get(sn=sn)
                ticket.date_use = timezone.now()
                ticket.order_name = name
                ticket.order_phone = phone
                ticket.order_address = address
                ticket.order_comments = comments
                ticket.save()
                msg = sn + "成功提交订单"
            except:
                msg = "提交订单失败"
            if request.is_ajax():
                return HttpResponse(json.dumps({
                    'verified':verified,
                    'msg':msg
                    }
                                               )
                                    )
            else:
                return render(request,'coupon/verify.html',{
                    'error_message':msg
                    })
        elif request.is_ajax():
            return HttpResponse(json.dumps({
                'verified':verified,
                'msg':msg
                }
                                           )
                                )
        else:
            return render(request,'coupon/verify.html',{
                'sn':sn,
                'error_message':msg
                }
                          )
            
                
            
