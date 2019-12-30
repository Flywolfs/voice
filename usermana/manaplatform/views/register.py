# -*- encoding: utf-8 -*-
'''
@File    :   register.py    
@Author :   Chi Zhang
'''
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from ..models import User
import datetime
# Create your views here.

def index(request):
    if request.method == "POST" and len(request.POST) == 2 and 'username' and 'password' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("received register!")
        try:
            old_user = User.objects.get(username=username)
            print("user existed!")
            # user existed , return 201 code
            ctx = {"info":"201"}
            return JsonResponse(ctx)
        except:
            # user not exist, go to register
            print("user not existed!")
            current_time = datetime.datetime.now()
            appid = str(current_time)[-6:]+username
            User.objects.create(username=username,password=password,timestamp=current_time,appid=appid)
            ctx = {"info":"200"}
            return JsonResponse(ctx)
    elif request.method == "GET":
        print("get register page!")
        ctx = {"info":"200"}
        return render(request, 'register.html',ctx)
    else:
        print("register error params")
        ctx = {"info":"402"}
        return JsonResponse(ctx)

