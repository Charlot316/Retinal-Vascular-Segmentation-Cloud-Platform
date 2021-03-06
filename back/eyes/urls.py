"""eyes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import user.views
from eyes import settings
# from user.views import ChatConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addPatient/', user.views.add_patient),
    path('findPatient/', user.views.find_patient),
    path('login/', user.views.login),
    path('register/', user.views.register),
    path('receive/', user.views.receive_origin),
    path('upload/', user.views.receive_upload),
    path('getListForDoctor/', user.views.get_photo_list_for_doctor),
    path('getListForPatient/', user.views.get_photo_list_for_patient),
    path('deletePicture/', user.views.delete_picture),
    path('revisePictureName/', user.views.revise_picture_name),
    path('getPatientInfo/', user.views.get_patient_info),
    path('uploadPatientIcon/', user.views.receive_patient_icon),
    path('editPatientInfo/', user.views.edit_patient_info),
    path('getDoctorInfo/', user.views.get_doctor_info),
    path('uploadDoctorIcon/', user.views.receive_doctor_icon),
    path('editDoctorInfo/', user.views.edit_doctor_info),
    path('getPhotoInfo/', user.views.get_photo_info),
    path('sendComment/', user.views.send_comment),
    path('deleteComment/', user.views.delete_comment),
    # path('addPatient/', user.views.addPatient),
    # path('delePatient/', user.views.delePatient),
    # path('addDoctor/', user.views.addDoctor),
    # path('deleDoctor/', user.views.deleDoctor),
    # path('findPatient/', user.views.findPatient),
    # path('findDoctor/', user.views.findDoctor),
    # path('chanePatient/',user.views.changePatient),
    # path('changeDoctor/', user.views.changeDoctor),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^', TemplateView.as_view(template_name="index.html")),
]

# websocket_urlpatterns=[
#     # ????????????websocket??????
#     path('wx/', ChatConsumer.as_asgi()),
# ]