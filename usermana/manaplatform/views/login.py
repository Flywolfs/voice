# -*- encoding: utf-8 -*-
'''
@File    :   login.py    
@Author :   Chi Zhang
'''

from django.shortcuts import render,HttpResponse,redirect
from ..models import User
# Create your views here.

def index(request):
    if request.method == "POST" and len(request.POST) == 2 and 'username' and 'password' in request.POST:
        print("received login!")
        username = request.POST.get('username')
        password = request.POST.get('pass   word')
        try:
            old_user = User.objects.get(username=username,password=password)
            # user existed , return 200 code
            request.session["msg"] = username
            return redirect('/voice/dashboard')
        except:
            # user not exist, go to register
            ctx = {"info":"201"}
            return HttpResponse(str(ctx))
    elif request.method == "GET":
        print("get login page!")
        ctx = {"info":"200"}
        return render(request, 'login.html',ctx)
    else:
        print("login error params")
        ctx = {"info": "402"}
        return HttpResponse(str(ctx))

def dashboard(request):
    print("=================")
    return render(request,'dashboard.html')

