# -*- encoding: utf-8 -*-
'''
@File    :   search_groups.py    
@Author :   Chi Zhang
'''

from django.shortcuts import render,HttpResponse,redirect
from ..models import User,Group,TblTokenSessionid
import json

REQUESTLEN = 2
cached_user_login = dict()
def index(request):
    if request.method == "GET":
        if "username" in request.GET and "login_token" in request.GET and len(request.GET) == REQUESTLEN:
            username = request.GET.get("username")
            login_token = request.GET.get("login_token")
            # 一般登录用户都会在缓存中存一份，万一出现系统down的情况，缓存才会消失。缓存是一人一条
            if username in cached_user_login:
                if login_token == cached_user_login[username]:
                    #TODO 执行搜索全部会议结果列表
                    result = _search_all_groups()
                    if result == []:
                        ctx = {"code":200}
                        return HttpResponse(json.dumps(ctx))
                    result["code"] = 200
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
                    result = _search_all_groups()
                    if result == []:
                        ctx = {"code": 200}
                        return HttpResponse(json.dumps(ctx))
                    result["code"] = 200
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

def _search_all_groups():
    group_list = []
    groups = Group.objects.all()
    for i in groups:
        group = dict()
        group["id"] = i.id
        token = i.token
        group_infos = TblTokenSessionid.objects.filter(token=token)
        group["meeting_number"] = len(group_infos)
        aggr_time = 0
        group_member = 0
        for j in group_infos:
            aggr_time += j.timespan
            group_member += len(j.reg_names.split(","))
        group["token"] = token
        group["aggr_time"] = aggr_time
        group["group_member"] = group_member
        group["create_date"] = str(i.create_time)
        group_list.append(group)
    return {"group_list":group_list}
