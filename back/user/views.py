import datetime
import operator
import os
import subprocess

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.encoding import escape_uri_path
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
import json
from user.models import Doctor, Patient, Photo
from django.views import View
from eyes.settings import MEDIA_ROOT
from django.contrib.auth.hashers import make_password, check_password


def login(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        uname = data_json.get('username')
        pwd = data_json.get('password')
        print(uname)
        print(pwd)
        user = Doctor.objects.filter(doctor_username=uname)
        print(user)
        if len(user) == 0:
            return JsonResponse({'success': False, 'message': '用户不存在'})
        if len(user) > 0:
            if check_password((user[0]).doctor_password, pwd):
                return JsonResponse({'success': True, 'message': '登录成功', 'userID': user[0].doctor_id,
                                     'role': 'Doctor'})
    else:
        return JsonResponse({})


def register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_name = data_json.get('username')
        temp_pwd = data_json.get('password')
        new_email = data_json.get('email')
        new_ph = data_json.get('phone')
        new_realname = data_json.get('realname')
        new_sex = data_json.get('sex')
        print(new_name)
        new_pwd = make_password(temp_pwd, None, 'pbkdf2_sha1')
        print(new_pwd)
        print(new_email)
        print(new_ph)
        print(new_realname)
        print(new_sex)
        if new_name is None:
            return JsonResponse({'success': False, 'message': '未输入'})
        else:
            space = Doctor.objects.filter(doctor_username=new_name)
            if len(space) > 0:
                return JsonResponse({'success': False, 'message': '用户名已存在'})
            else:
                new_d = Doctor()
                new_d.doctor_username = new_name
                new_d.doctor_password = new_pwd
                new_d.doctor_email = new_email
                new_d.doctor_phone = new_ph
                new_d.doctor_realname = new_realname
                new_d.doctor_sex = new_sex
                new_d.save()
                return JsonResponse({'success': True, 'message': '注册成功'})
    else:
        return JsonResponse({})


def get_photo_list_for_doctor(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        u_id = data_json.get('user_id')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数
        title = data_json.get('title')  # 每页显示条目数
        result = Photo.objects.filter(uId=u_id, name__contains=title)
        apply_list = list(
            result.values('photo_id', 'photo_realname', 'photo_savename', 'photo_origin', 'photo_upload',
                          'photo_promap', 'photo_patient__patient_id'))
        total = len(apply_list)
        paginator = Paginator(apply_list, pagesize)
        try:
            p_list = paginator.page(pagenum)
        except PageNotAnInteger as e:
            p_list = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                p_list = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                p_list = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'success': True, 'message': '返回list成功', 'imageList': list(p_list), 'total': total},
                            safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})


def receive_origin(request):
    BASEURL = "http://10.251.0.251:8000/media/test/"
    image = request.FILES.get('pic_img')
    u_id = request.POST.get('user_id')
    obj = Photo.objects.create(photo_img=image)
    obj.photo_doctor = Doctor.objects.get(doctor_id=u_id)

    obj.photo_realname = os.path.basename(os.path.splitext(image.name)[0])
    obj.photo_savename = os.path.basename(os.path.splitext(obj.img.path)[0])
    obj.photo_origin = BASEURL + os.path.basename(
        os.path.splitext(obj.img.path)[0]) + "_origin.png"
    obj.photo_promap = BASEURL + os.path.basename(
        os.path.splitext(obj.img.path)[0]) + "_promap.png"
    obj.save()
    subprocess.Popen("python ./test/test.py" + " " + os.path.basename(obj.img.path), shell=True)
    # os.remove('./media/test/test.tif')
    # data = jsonResult.json_managresult(message="添加成功", result="success", data=[], form_data={})

    return JsonResponse('message="上传成功', safe=False)


def delete_picture(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        photo_id = data_json.get('photoID')
        p = Photo.objects.filter(photoID=photo_id)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '图片'}, status=404)
        else:
            photo = Photo.objects.get(photoID=photo_id)
            save_name = photo.photo_savename
            try:
                if photo.photo_upload is not None:
                    os.remove('./media/test/' + save_name + '_upload.png')
                os.remove('./media/test/' + save_name + '_promap.png')
                os.remove('./media/test/' + save_name + '_origin.png')
            except FileNotFoundError as e:
                print("exception:" + e)
            photo.delete()
            return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    else:
        return JsonResponse({})


def revise_picture_name(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_name = data_json.get('newName')
        photo_id = data_json.get('photoID')

        picture = Photo.objects.filter(photo_id=photo_id)
        if len(picture) == 0:
            return JsonResponse({'success': False, 'message': '不存在该图片'}, status=404)
        else:
            obj = Photo.objects.get(photo_id=photo_id)
            obj.photo_realname = new_name
            obj.save()
            return JsonResponse({'success': True, 'message': '修改成功'}, status=200)
    else:
        return JsonResponse({})

# def addPatient(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         new_name = data_json.get('username')
#         new_pwd = data_json.get('password')
#         new_email = data_json.get('email')
#         new_sex = data_json.get('sex')
#         new_ph = data_json.get('phone')
#         print(new_name)
#         print(new_pwd)
#         print(new_email)
#         print(new_sex)
#         print(new_ph)
#         space = Patient.objects.filter(pName=new_name)
#         if len(space) > 0:
#             return JsonResponse({'success': False, 'message': '用户名已存在'})
#         else:
#             new_p = Patient()
#             new_p.pName = new_name
#             new_p.pPwd = new_pwd
#             new_p.pEmail = new_email
#             new_p.pSex = new_sex
#             new_p.pPhone = new_ph
#             new_p.save()
#             return JsonResponse({'success': True, 'message': '新增成功'})
#     else:
#         return JsonResponse({})
#
#
# def delePatient(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         name = data_json.get('pName')
#         p = Patient.objects.filter(pName=name)
#         if len(p) == 0:
#             return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
#         else:
#             (Patient.objects.get(pName=name)).delete()
#             return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
#     else:
#         return JsonResponse({})
#
#
# def addDoctor(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         name = data_json.get('dName')
#         pwd = data_json.get('dPwd')
#         info = data_json.get('dInfo')
#         space = Doctor.objects.filter(dName=name)
#         if len(space) > 0:
#             return JsonResponse({'success': False, 'message': '用户名已存在'})
#         else:
#             new_d = Doctor()
#             new_d.dName = name
#             new_d.dPwd = pwd
#             new_d.dInfo = info
#             new_d.save()
#             return JsonResponse({'success': True, 'message': '新增成功'})
#     else:
#         return JsonResponse({})
#
#
# def deleDoctor(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         name = data_json.get('dName')
#         p = Doctor.objects.filter(dName=name)
#         if len(p) == 0:
#             return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
#         else:
#
#             (Doctor.objects.get(dName=name)).delete()
#
#             return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
#     else:
#         return JsonResponse({})
#
#
# def findPatient(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         qparam = data_json.get('qparam')
#         query = data_json.get('query')
#         pagenum = data_json.get('pagenum')  # 当前页码数
#         pagesize = data_json.get('pagesize')  # 每页显示条目数
#
#         if query is None:
#             result = Patient.objects.all()
#
#         if qparam == "1":
#             result = Patient.objects.filter(pName__contains=query)
#         else:
#             result = Patient.objects.filter(pID__contains=query)
#
#         apply_list = list(result.values('pName', 'pID', 'pPwd', 'pPhone', 'pAddr', 'pEmail',
#                                         'pTall', 'pWeight', 'pAge', 'pSex', 'pAller', 'pCharacter'))
#
#         print(list)
#         total = len(apply_list)
#         paginator = Paginator(apply_list, pagesize)
#         try:
#             p_info = paginator.page(pagenum)
#         except PageNotAnInteger as e:
#             p_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
#         except EmptyPage as e:
#             if int(pagenum) > paginator.num_pages:
#                 p_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
#             else:
#                 p_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据
#
#         return JsonResponse({'pInfo': list(p_info), 'total': total}, safe=False, status=200,
#                             json_dumps_params={'ensure_ascii': False})
#     else:
#         return JsonResponse({})
#
#
# def findDoctor(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         qparam = data_json.get('qparam')
#         query = data_json.get('query')
#         pagenum = data_json.get('pagenum')  # 当前页码数
#         pagesize = data_json.get('pagesize')  # 每页显示条目数
#
#         if query is None:
#             result = Patient.objects.all()
#
#         if qparam == "1":
#             result = Patient.objects.filter(dName__contains=query)
#         else:
#             result = Patient.objects.filter(dID__contains=query)
#
#         apply_list = list(result.values('dName', 'dID', 'dPwd', 'dInfo', ))
#         print(list)
#         total = len(apply_list)
#         paginator = Paginator(apply_list, pagesize)
#         try:
#             d_info = paginator.page(pagenum)
#         except PageNotAnInteger as e:
#             d_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
#         except EmptyPage as e:
#             if int(pagenum) > paginator.num_pages:
#                 d_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
#             else:
#                 d_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据
#
#         return JsonResponse({'pInfo': list(d_info), 'total': total}, safe=False, status=200,
#                             json_dumps_params={'ensure_ascii': False})
#     else:
#         return JsonResponse({})
#
#
# def changePatient(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         name = data_json.get('pName')
#         ctype = data_json.get('type')
#         info = data_json.get('info')
#         p = Patient.objects.filter(pName=name)
#         if len(p) == 0:
#             return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
#         else:
#             if ctype == '1':
#                 (Patient.objects.get(pName=name)).update(pName=info)
#             return JsonResponse({'success': True, 'message': '修改成功'}, status=200)
#     else:
#         return JsonResponse({})
#
#
# def changeDoctor(request):
#     if request.method == 'POST':
#         data_json = json.loads(request.body)
#         name = data_json.get('dName')
#         ctype = data_json.get('type')
#         info = data_json.get('info')
#         d = Doctor.objects.filter(dName=name)
#         if len(d) == 0:
#             return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
#         else:
#             if ctype == '1':
#                 (Doctor.objects.get(dName=name)).update(dName=info)
#             return JsonResponse({'success': True, 'message': '修改成功'}, status=200)
#     else:
#         return JsonResponse({})


# class DownloadQnaireToWord(View):
#     def read_file(self, file_name, size):
#         with open(file_name, mode='rb') as fp:
#             while True:
#                 c = fp.read(size)
#                 if c:
#                     yield c
#                 else:
#                     break
#
#     def post(self, request):
#         print("**********************")
#         print(MEDIA_ROOT)
#         filepath = MEDIA_ROOT + '/test/'
#         filename = 'bytemap.png'
#         response = StreamingHttpResponse(self.read_file(os.path.join(filepath, filename), 1024))
#         response['Content-Type'] = 'application/octet-stream'
#         response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
#         print(response['Content-Disposition'])
#         print(response)
#         if response:
#             return response
#         else:
#             return JsonResponse({'success': False, 'message': '导出失败，请联系管理员解决！'},
#                                 json_dumps_params={'ensure_ascii': False})
