# -*- encoding: utf-8 -*-
'''
@File    :   group_manage.py    
@Author :   Chi Zhang
'''
from django.shortcuts import render,HttpResponse,redirect
from ..models import User,Group
import json
import datetime

REQUESTLEN = 3
cached_user_login = dict()
def index(request):
    if request.method == "GET":
        if "username" in request.GET and "login_token" in request.GET and "id" in request.GET and len(request.GET) == REQUESTLEN:
            user_name = request.GET.get("user_name")
            login_token = request.GET.get("login_token")
            id = request.GET.get("id")
            # 一般登录用户都会在缓存中存一份，万一出现系统down的情况，缓存才会消失。缓存是一人一条
            if user_name in cached_user_login:
                if login_token == cached_user_login[user_name]:
                    #TODO 执行搜索全部会议结果列表
                    result = _search_all_members_by_token(id=id)
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
                    user = User.objects.get(username=user_name)
                    last_user_login = user.user_login.last()
                    if last_user_login is None:
                        ctx= {"code":404}
                        return HttpResponse(json.dumps(ctx))
                    elif last_user_login.login_token != login_token:
                        ctx = {"code": 404}
                        return HttpResponse(json.dumps(ctx))
                    #TODO 执行搜索全部会议结果列表,并将该人的记录存到缓存中
                    cached_user_login[user_name] = login_token
                    result = _search_all_members_by_token(id=id)
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

def _search_all_members_by_token(id=None):
    group = Group.objects.get(id=id)
    member_list = []
    members = Member.objects.filter(group_id=id)
    for i in members:
        member = dict()
        member["id"] = i.id
        member["member_name"] = i.member_name
        member["member_id"] = i.member_id
        member["role"] = i.role
        member["create_date"] = i.create_time
        member["aggr_time"] = 0
        member["meeting_times"] = 0
        member_list.append(member)
    return {"members":member_list,"token":group.token}