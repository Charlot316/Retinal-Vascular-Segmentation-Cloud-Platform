# Generated by Django 3.1.7 on 2021-09-23 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_pho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pho',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='test'),
        ),
    ]
