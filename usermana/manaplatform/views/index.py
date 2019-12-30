# -*- encoding: utf-8 -*-
'''
@File    :   index.py    
@Author :   Chi Zhang
'''
from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request, 'index.html')

