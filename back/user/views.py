import datetime
import operator
import os
import subprocess

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
import json
from user.models import Doctor, Patient, Manager, Pho
from django.views import View
from eyes.settings import MEDIA_ROOT
import random
import string
import urllib

def login(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        uname = data_json.get('username')
        pwd = data_json.get('password')
        print(uname)
        print(pwd)
        user = Patient.objects.filter(pName=uname)
        user2 = Doctor.objects.filter(dName=uname)
        user3 = Manager.objects.filter(mID=uname)
        print(user)
        print(user2)
        print(user3)
        if len(user) == 0 and len(user2) == 0 and len(user3) == 0:
            return JsonResponse({'success': False, 'message': '用户不存在'})
        if len(user) > 0:
            if (user[0]).pPwd == pwd:
                return JsonResponse({'success': True, 'message': '登录成功', 'user_id': user[0].pID,
                                     'role': 'Patient'})
            else:
                return JsonResponse({'success': False, 'message': '密码错误', 'user_id': user[0].pID,
                                     'role': 'Patient'})
        if len(user2) > 0:
            if (user[0]).pPWD == pwd:
                return JsonResponse({'success': True, 'message': '登录成功', 'user_id': user[0].pID,
                                     'role': 'Doctor'})
            else:
                return JsonResponse({'success': False, 'message': '密码错误', 'user_id': user[0].pID,
                                     'role': 'Doctor'})
        if len(user3) > 0:
            if (user[0]).pPWD == pwd:
                return JsonResponse({'success': True, 'message': '登录成功', 'user_id': user[0].pID,
                                     'role': 'Manager'})
            else:
                return JsonResponse({'success': False, 'message': '密码错误', 'user_id': user[0].pID,
                                     'role': 'Manager'})
    else:
        return JsonResponse({})


def register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_name = data_json.get('username')
        new_pwd = data_json.get('password')
        new_email = data_json.get('email')
        new_sex = data_json.get('sex')
        new_ph = data_json.get('phone')
        print(new_name)
        print(new_pwd)
        print(new_email)
        print(new_sex)
        print(new_ph)
        if new_name is None:
            return JsonResponse({'success': False, 'message': '未输入'})
        else:
            space = Patient.objects.filter(pName=new_name)
            if len(space) > 0:
                return JsonResponse({'success': False, 'message': '用户名已存在'})
            else:
                new_p = Patient()
                new_p.pName = new_name
                new_p.pPwd = new_pwd
                new_p.pEmail = new_email
                new_p.pSex = new_sex
                new_p.pPhone = new_ph
                new_p.save()
                return JsonResponse({'success': True, 'message': '注册成功'})
    else:
        return JsonResponse({})


def addPatient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_name = data_json.get('username')
        new_pwd = data_json.get('password')
        new_email = data_json.get('email')
        new_sex = data_json.get('sex')
        new_ph = data_json.get('phone')
        print(new_name)
        print(new_pwd)
        print(new_email)
        print(new_sex)
        print(new_ph)
        space = Patient.objects.filter(pName=new_name)
        if len(space) > 0:
            return JsonResponse({'success': False, 'message': '用户名已存在'})
        else:
            new_p = Patient()
            new_p.pName = new_name
            new_p.pPwd = new_pwd
            new_p.pEmail = new_email
            new_p.pSex = new_sex
            new_p.pPhone = new_ph
            new_p.save()
            return JsonResponse({'success': True, 'message': '新增成功'})
    else:
        return JsonResponse({})


def delePatient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('pName')
        p = Patient.objects.filter(pName=name)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
        else:
            (Patient.objects.get(pName=name)).delete()
            return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    else:
        return JsonResponse({})


def addDoctor(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('dName')
        pwd = data_json.get('dPwd')
        info = data_json.get('dInfo')
        space = Doctor.objects.filter(dName=name)
        if len(space) > 0:
            return JsonResponse({'success': False, 'message': '用户名已存在'})
        else:
            new_d = Doctor()
            new_d.dName = name
            new_d.dPwd = pwd
            new_d.dInfo = info
            new_d.save()
            return JsonResponse({'success': True, 'message': '新增成功'})
    else:
        return JsonResponse({})


def deleDoctor(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('dName')
        p = Doctor.objects.filter(dName=name)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
        else:

            (Doctor.objects.get(dName=name)).delete()

            return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    else:
        return JsonResponse({})


def findPatient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数

        if query is None:
            result = Patient.objects.all()

        if qparam == "1":
            result = Patient.objects.filter(pName__contains=query)
        else:
            result = Patient.objects.filter(pID__contains=query)

        apply_list = list(result.values('pName', 'pID', 'pPwd', 'pPhone', 'pAddr', 'pEmail',
                                        'pTall', 'pWeight', 'pAge', 'pSex', 'pAller', 'pCharacter'))

        print(list)
        total = len(apply_list)
        paginator = Paginator(apply_list, pagesize)
        try:
            p_info = paginator.page(pagenum)
        except PageNotAnInteger as e:
            p_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                p_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                p_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'pInfo': list(p_info), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})


def findDoctor(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        qparam = data_json.get('qparam')
        query = data_json.get('query')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数

        if query is None:
            result = Patient.objects.all()

        if qparam == "1":
            result = Patient.objects.filter(dName__contains=query)
        else:
            result = Patient.objects.filter(dID__contains=query)

        apply_list = list(result.values('dName', 'dID', 'dPwd', 'dInfo', ))
        print(list)
        total = len(apply_list)
        paginator = Paginator(apply_list, pagesize)
        try:
            d_info = paginator.page(pagenum)
        except PageNotAnInteger as e:
            d_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
        except EmptyPage as e:
            if int(pagenum) > paginator.num_pages:
                d_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
            else:
                d_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'pInfo': list(d_info), 'total': total}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})


def changePatient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('pName')
        ctype = data_json.get('type')
        info = data_json.get('info')
        p = Patient.objects.filter(pName=name)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
        else:
            if ctype == '1':
                (Patient.objects.get(pName=name)).update(pName=info)
            return JsonResponse({'success': True, 'message': '修改成功'}, status=200)
    else:
        return JsonResponse({})


def changeDoctor(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('dName')
        ctype = data_json.get('type')
        info = data_json.get('info')
        d = Doctor.objects.filter(dName=name)
        if len(d) == 0:
            return JsonResponse({'success': False, 'message': '用户名不存在'}, status=404)
        else:
            if ctype == '1':
                (Doctor.objects.get(dName=name)).update(dName=info)
            return JsonResponse({'success': True, 'message': '修改成功'}, status=200)
    else:
        return JsonResponse({})

def getList(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        uId = data_json.get('user_id')
        # pagenum = data_json.get('pagenum')  # 当前页码数
        # pagesize = data_json.get('pagesize')  # 每页显示条目数
        result = Pho.objects.filter(uId=uId)
        apply_list = list(result.values('name','origin','bytemap','promap' ))
        # print(list)
        # total = len(apply_list)
        # paginator = Paginator(apply_list, pagesize)
        # try:
        #     d_info = paginator.page(pagenum)
        # except PageNotAnInteger as e:
        #     d_info = paginator.page(1)  # pagenum不是整数->返回第一页数据
        # except EmptyPage as e:
        #     if int(pagenum) > paginator.num_pages:
        #         d_info = paginator.page(paginator.num_pages)  # pagenum大于页码范围->获取最后一页数据
        #     else:
        #         d_info = paginator.page(1)  # pagenum小于页码范围->获取第一页数据

        return JsonResponse({'success': True, 'message': '返回list成功','imageList': list(apply_list)}, safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})

def receive(request):
    image = request.FILES.get('pic_img')
    title = request.POST.get('pic_title')
    uId=request.POST.get('user_id')
    obj = Pho.objects.create(name=title, img=image,bytemap="未上传",promap="未上传",uId=1,origin="未上传")
    obj.uId=uId
    obj.name=os.path.basename(os.path.splitext(obj.img.path)[0])
    obj.origin="http://10.251.0.251:8000/media/test/"+os.path.basename(os.path.splitext(obj.img.path)[0])+"_origin.png"
    obj.bytemap="http://10.251.0.251:8000/media/test/"+os.path.basename(os.path.splitext(obj.img.path)[0])+"_bytemap.png"
    obj.promap="http://10.251.0.251:8000/media/test/"+os.path.basename(os.path.splitext(obj.img.path)[0])+"_promap.png"
    obj.save()
    subprocess.Popen("python ./test/test.py"+" "+os.path.basename(obj.img.path), shell=True)
    # os.remove('./media/test/test.tif')
    # data = jsonResult.json_managresult(message="添加成功", result="success", data=[], form_data={})

    return JsonResponse('message="上传成功', safe=False)

def deletePicture(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('name')
        p = Pho.objects.filter(name=name)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '图片'}, status=404)
        else:
            os.remove('./media/test/'+name+'_promap.png')
            os.remove('./media/test/' + name + '_origin.png')
            os.remove('./media/test/' + name + '_bytemap.png')
            (Pho.objects.get(name=name)).delete()
            return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    else:
        return JsonResponse({})

class DownloadQnaireToWord(View):
    def read_file(self, file_name, size):
        with open(file_name, mode='rb') as fp:
            while True:
                c = fp.read(size)
                if c:
                    yield c
                else:
                    break

    def post(self, request):
        print("**********************")
        print(MEDIA_ROOT)
        filepath = MEDIA_ROOT + '/test/'
        filename = 'bytemap.png'
        response = StreamingHttpResponse(self.read_file(os.path.join(filepath, filename), 1024))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
        print(response['Content-Disposition'])
        print(response)
        if response:
            return response
        else:
            return JsonResponse({'success': False, 'message': '导出失败，请联系管理员解决！'},
                                json_dumps_params={'ensure_ascii': False})
