# -*- encoding: utf-8 -*-
'''
@File    :   urls.py    
@Author :   Chi Zhang
'''

from django.urls import path

from .views import add_group,add_member,delete_group,delete_meeting,delete_member,group_manage,index,login,\
    modify_group,modify_member,register,search_groups,search_single_meeting,search_meetings,search_single_meeting_history

urlpatterns = [
    path(r'index/',index.index,name="index"),
    path(r'login/',login.index,name="login"),
    path(r'register/',register.index,name="register"),
    path(r'meetinglist/',search_meetings.index,name="search_meetings"),
    path(r'meetingdetail/',search_single_meeting.index,name="search_single_meeting"),
    path(r'meetinghistory/',search_single_meeting_history.index,name="search_single_meeting_history"),
    path(r'groupmanage/',group_manage.index,name="group_manage"),
    path(r'grouplist/',search_groups.index,name="search_group"),
    path(r'addgroup/',add_group.index,name="add_group"),
    path(r'addmember/',add_member.index,name="add_member"),
    path(r'modifygroup/',modify_group.index,name="modify_group")
]