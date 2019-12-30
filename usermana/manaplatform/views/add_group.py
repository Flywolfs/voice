# -*- encoding: utf-8 -*-
'''
@File    :   add_group.py    
@Author :   Chi Zhang
'''
from django.shortcuts import render,HttpResponse,redirect
from ..models import User,Group
import json
import datetime

REQUESTLEN = 3
cached_user_login = dict()
def index(request):
    if request.method == "POST":
        if "username" in request.POST and "login_token" in request.POST and "token" in request.POST and len(request.POST) == REQUESTLEN:
            username = request.POST.get("username")
            login_token = request.POST.get("login_token")
            token = request.POST.get("token")
            # 一般登录用户都会在缓存中存一份，万一出现系统down的情况，缓存才会消失。缓存是一人一条
            if username in cached_user_login:
                if login_token == cached_user_login[username]:
                    #TODO 执行将新增团队
                    result = _add_new_group(token=token)
                    return HttpResponse(json.dumps(result))
                else:
                    ctx = {"code":404}
                    return HttpResponse(json.dumps(ctx))
            else:
                try:
                    #找出最新的登录记录
                    user = User.objects.get(username=username)
                    last_user_login = user.user_login.last()
                    if last_user_login is None:
                        ctx= {"code":404}
                        return HttpResponse(json.dumps(ctx))
                    elif last_user_login.login_token != login_token:
                        ctx = {"code": 404}
                        return HttpResponse(json.dumps(ctx))
                    #TODO 执行搜索全部会议结果列表,并将该人的记录存到缓存中
                    cached_user_login[username] = login_token
                    result = _add_new_group(token=token)
                    return HttpResponse(json.dumps(result))
                #此人不存在
                except:
                    ctx = {"code":404}
                    return HttpResponse(json.dumps(ctx))
        else:
            ctx = {"code": 400}
            return HttpResponse(json.dumps(ctx))
    else:
        ctx = {"code":400}
        return HttpResponse(json.dumps(ctx))

# TODO 完善方法
def _add_new_group(token=None):
    try:
        existed_group = Group.objects.get(token=token)
        return {"code":201}
    except:
        new_group = Group(token=token)
        new_group.save()
        return {"code":200}