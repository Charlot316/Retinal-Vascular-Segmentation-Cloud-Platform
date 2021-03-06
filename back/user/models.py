# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    comment_id = models.AutoField(db_column='comment_ID', primary_key=True)  # Field name made lowercase.
    photo = models.ForeignKey('Photo', models.DO_NOTHING, db_column='photo_ID', blank=True, null=True)  # Field name made lowercase.
    doctor = models.ForeignKey('Doctor', models.DO_NOTHING, db_column='doctor_ID', blank=True, null=True)  # Field name made lowercase.
    reply_to = models.ForeignKey('self', models.DO_NOTHING, db_column='reply_to', blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class Doctor(models.Model):
    doctor_id = models.AutoField(db_column='doctor_ID', primary_key=True)  # Field name made lowercase.
    doctor_username = models.CharField(max_length=255)
    doctor_password = models.CharField(max_length=255)
    doctor_realname = models.CharField(max_length=255, blank=True, null=True)
    doctor_email = models.CharField(max_length=255, blank=True, null=True)
    doctor_icon = models.CharField(max_length=255, blank=True, null=True)
    doctor_phone = models.CharField(max_length=255, blank=True, null=True)
    doctor_sex = models.SmallIntegerField(blank=True, null=True)
    doctor_age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class Manager(models.Model):
    manager_id = models.AutoField(db_column='manager_ID', primary_key=True)  # Field name made lowercase.
    manager_name = models.CharField(max_length=20)
    manager_password = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'manager'


class Patient(models.Model):
    patient_id = models.AutoField(db_column='patient_ID', primary_key=True)  # Field name made lowercase.
    patient_name = models.CharField(max_length=30)
    patient_phone = models.CharField(max_length=11, blank=True, null=True)
    patient_address = models.CharField(max_length=30, blank=True, null=True)
    patient_email = models.CharField(max_length=255, blank=True, null=True)
    patient_height = models.IntegerField(blank=True, null=True)
    patient_weight = models.IntegerField(blank=True, null=True)
    patient_age = models.IntegerField(blank=True, null=True)
    patient_sex = models.IntegerField(blank=True, null=True)
    patient_icon = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class Photo(models.Model):
    photo_id = models.AutoField(db_column='photo_ID', primary_key=True)  # Field name made lowercase.
    photo_realname = models.CharField(max_length=255)
    photo_doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='photo_doctor_ID', blank=True, null=True)  # Field name made lowercase.
    photo_savename = models.CharField(max_length=255)
    photo_patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='photo_patient_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'photo'


class Upload(models.Model):
    upload_id = models.AutoField(db_column='upload_ID', primary_key=True)  # Field name made lowercase.
    photo = models.ForeignKey(Photo, models.DO_NOTHING, db_column='photo_ID', blank=True, null=True)  # Field name made lowercase.
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctor_ID', blank=True, null=True)  # Field name made lowercase.
    upload_savename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upload'
