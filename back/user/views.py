import datetime
import operator

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from user.models import Doctor,Patient,Manager
import random
import string

def register(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        new_uid = data_json.get('uID')
        new_name = data_json.get('username')
        new_pwd1 = data_json.get('password')
        new_pwd2 = data_json.get('repassword')
        new_tel = data_json.get('phonenum')
        if new_uid is None:
            return JsonResponse({'success': False, 'message': '未输入'})
        else:
            space = User.objects.filter(uID=new_uid)
            if len(space) > 0:
                return JsonResponse({'success': False, 'message': '账号已存在'})
            else:
                if new_pwd2 != new_pwd1:
                    return JsonResponse({'success': False, 'message': '两次密码不一致'})
                else:
                    new_student = User()
                    new_student.uID = new_uid
                    new_student.uName = new_name
                    new_student.uPWD = new_pwd1
                    new_student.uPhone = new_tel
                    new_student.uCharacter = False
                    new_student.save()
                    return JsonResponse({'success': True, 'message': '注册成功'})
    else:
        return JsonResponse({})
