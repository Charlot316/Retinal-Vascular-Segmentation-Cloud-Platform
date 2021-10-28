from django.db import models
import os
from eyes.storage import ImageStorage


class Patient(models.Model):
    pName = models.CharField(max_length=30)
    pID = models.AutoField(primary_key=True)
    pPwd = models.CharField(max_length=25)
    pPhone = models.CharField(max_length=11)
    pAddr = models.CharField(max_length=30)
    pEmail = models.CharField(max_length=20)
    pTall = models.DecimalField(max_digits=3, decimal_places=3)
    pWeight = models.DecimalField(max_digits=3, decimal_places=3)
    pAge = models.IntegerField()
    pSex = models.CharField(max_length=1)
    #F/M
    pAller = models.TextField(max_length=200)
    pCharacter = models.BooleanField(default=False)
    # 上面那句是改之前的模板里的，为了测试的时候不出错，目前还是加上
    # True是管理员，False是读者，默认是读者

# 医生
class Doctor(models.Model):
    dID = models.AutoField(primary_key=True)
    dName = models.CharField(max_length=20)
    dPwd = models.CharField(max_length=25)
    dInfo = models.TextField(max_length=200)

# 管理员
class Manager(models.Model):
    mID = models.AutoField(primary_key=True)
    mName = models.CharField(max_length=20)
    mPwd = models.CharField(max_length=25)




class Pho(models.Model):
    name = models.CharField(max_length=255)
    saveName = models.CharField(max_length=255)
    uId=models.IntegerField(null=True)
    origin = models.CharField(null=True,max_length=255)
    bytemap = models.CharField(null=True,max_length=255)
    promap = models.CharField(null=True,max_length=255)
    img = models.FileField(blank=True, null=True, upload_to='test',storage=ImageStorage())