# -*- encoding: utf-8 -*-
'''
@File    :   search_single_meeting.py    
@Author :   Chi Zhang
'''
from django.shortcuts import render,HttpResponse,redirect
from ..models import User,TblTokenSessionid
import json
import datetime

REQUESTLEN = 3
cached_user_login = dict()
def index(request):
    if request.method == "GET":
        if "username" in request.GET and "login_token" and "id" in request.GET and len(request.GET) == REQUESTLEN:
            username = request.GET.get("username")
            login_token = request.GET.get("login_token")
            id = request.GET.get("id")
            # 一般登录用户都会在缓存中存一份，万一出现系统down的情况，缓存才会消失。缓存是一人一条
            if username in cached_user_login:
                if login_token == cached_user_login[username]:
                    #TODO 根据tag和token查询会议记录并返回
                    result = _search_meeting_by_tag_token(id=id)
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
                    result = _search_meeting_by_tag_token(id=id)
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

def _search_meeting_by_tag_token(id=None):
    try:
        the_exact_meeting = TblTokenSessionid.objects.get(id=id)
        meeting_info = dict()
        meeting_info["tag"] = the_exact_meeting.tag
        meeting_info["token"] = the_exact_meeting.token
        meeting_info["timespan"] = the_exact_meeting.timespan
        meeting_info["meeting_member"] = len(the_exact_meeting.reg_names.split(","))
        meeting_info["create_date"] = the_exact_meeting.time
        return meeting_info
    except:
        return[]