from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(default='',max_length=255)
    password = models.CharField(default='',max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

class User_login(models.Model):
    username = models.CharField(default='', max_length=255)
    last_login_time = models.DateTimeField(auto_now_add=True)
    login_token = models.CharField(default='',max_length=255)
    user = models.ForeignKey(User,related_name="user_login",on_delete=models.CASCADE,null=True)

class Group(models.Model):
    token = models.CharField(default='',max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    member_name = models.CharField(default='',max_length=255)
    member_id = models.CharField(default='',max_length=255)
    role = models.CharField(default='',max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group,related_name="_group_member",on_delete=models.CASCADE,null=True)

class TblSpeakerRegister(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=50)
    speaker_name = models.CharField(max_length=50)
    feature_vector = models.TextField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_speaker_register'


class TblTokenSessionid(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    session_id = models.CharField(max_length=50)
    reg_names = models.CharField(max_length=255)
    status = models.IntegerField()
    timespan = models.BigIntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_token_sessionid'


class TblVoiceResultInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    reg_names = models.CharField(max_length=255)
    session_id = models.CharField(max_length=50)
    duration = models.CharField(max_length=20, blank=True, null=True)
    section_timestamp = models.CharField(max_length=20, blank=True, null=True)
    section_index = models.BigIntegerField(blank=True, null=True)
    file_tag = models.CharField(max_length=50, blank=True, null=True)
    item_index = models.BigIntegerField()
    start_index = models.BigIntegerField()
    length = models.BigIntegerField()
    item_timestamp = models.CharField(max_length=20)
    speaking_name = models.CharField(max_length=255, blank=True, null=True)
    emotion = models.CharField(max_length=255, blank=True, null=True)
    asr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_voice_result_info'