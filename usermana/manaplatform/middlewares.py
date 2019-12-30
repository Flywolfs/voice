# -*- encoding: utf-8 -*-
'''
@File    :   middlewares.py.py    
@Author :   Chi Zhang
'''
from django.utils.deprecation import MiddlewareMixin
class manaMiddle(MiddlewareMixin):

    def process_response(self, request, response):

        response['Access-Control-Allow-Origin']= "*"

        return response