from django.db import models
from eyes.storage import ImageStorage


class Doctor(models.Model):
    doctor_id = models.AutoField(db_column='doctor_ID', primary_key=True)  # Field name made lowercase.
    doctor_username = models.CharField(max_length=255)
    doctor_password = models.CharField(max_length=255)
    doctor_realname = models.CharField(max_length=255, null=True)
    doctor_email = models.CharField(max_length=255, blank=True, null=True)
    doctor_icon = models.CharField(max_length=255, blank=True, null=True)
    doctor_phone = models.CharField(max_length=255, blank=True, null=True)
    doctor_sex = models.SmallIntegerField(blank=True, null=True)
    doctor_age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_doctor'


class Manager(models.Model):
    manager_id = models.AutoField(db_column='manager_ID', primary_key=True)  # Field name made lowercase.
    manager_name = models.CharField(max_length=20)
    manager_password = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'user_manager'


class Patient(models.Model):
    patient_name = models.CharField(max_length=30)
    patient_id = models.AutoField(db_column='patient_ID', primary_key=True)  # Field name made lowercase.
    patient_phone = models.CharField(max_length=11, blank=True, null=True)
    patient_address = models.CharField(max_length=30, blank=True, null=True)
    patient_email = models.CharField(max_length=255, blank=True, null=True)
    patient_height = models.DecimalField(max_digits=3, decimal_places=3, blank=True, null=True)
    patient_weight = models.DecimalField(max_digits=3, decimal_places=3, blank=True, null=True)
    patient_age = models.IntegerField(blank=True, null=True)
    patient_sex = models.CharField(max_length=1, blank=True, null=True)
    patient_icon = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_patient'


class Photo(models.Model):
    photo_id = models.AutoField(db_column='photo_ID', primary_key=True)  # Field name made lowercase.
    photo_realname = models.CharField(max_length=255)
    photo_img = models.FileField(max_length=255, upload_to='test', storage=ImageStorage())
    photo_doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='photo_doctor_ID', blank=True,
                                     null=True)  # Field name made lowercase.
    photo_promap = models.CharField(max_length=255, blank=True, null=True)
    photo_origin = models.CharField(max_length=255, blank=True, null=True)
    photo_savename = models.CharField(max_length=255)
    photo_patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='photo_patient_ID', blank=True,
                                      null=True)  # Field name made lowercase.
    photo_upload = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_photo'
