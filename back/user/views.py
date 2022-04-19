import subprocess
import cv2
import os
import json
import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, FileResponse, StreamingHttpResponse
from user.models import Doctor, Patient, Photo, Upload, Comment
from django.contrib.auth.hashers import make_password, check_password

# BASEURL = "http://localhost:8000/media/test/"


BASEURL ="http://10.251.0.251:8000/media/test/"

# if BASEURL == "http://10.251.0.251:8000/media/test/":
#     unloader = transforms.ToPILImage()
#     os.environ["CUDA_VISIBLE_DEVICES"] = '0,1,2,3'
#     model = torch.load('./user/DS_Model_100.pkl')


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, close_code):
#         pass
#
#     def receive(self, text_data):
#         """
#         接收消息
#         :param text_data: 客户端发送的消息
#         :return:
#         """
#         print(text_data)
#         poetryList = [
#             "云想衣裳花想容",
#             "春风拂槛露华浓",
#             "若非群玉山头见",
#             "会向瑶台月下逢",
#         ]
#         for i in poetryList:
#             time.sleep(0.5)
#             self.send(i)


def get_patient_icon(id):
    patient = Patient.objects.get(patient_id=id)
    if patient.patient_icon is not None and len(patient.patient_icon) > 0:
        return BASEURL + 'patient/' + patient.patient_icon + '.png'
    else:
        photo = Photo.objects.filter(photo_patient__patient_id=patient.patient_id)
        try:
            return photo.last().photo_promap
        except:
            return ""
            pass


def get_doctor_icon(id):
    doctor = Doctor.objects.get(doctor_id=id)
    if doctor.doctor_icon is not None and len(doctor.doctor_icon) > 0:
        return BASEURL + 'doctor/' + doctor.doctor_icon + '.png'
    else:
        return ""


def login(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        uname = data_json.get('username')
        pwd = data_json.get('password')
        print(uname)
        print(pwd)
        user = Doctor.objects.filter(doctor_username=uname)
        if len(user) == 0:
            return JsonResponse({'success': False, 'message': '用户不存在'})
        if len(user) > 0:
            if check_password(pwd, (user[0]).doctor_password):
                return JsonResponse({'success': True, 'message': '登录成功', 'userID': user[0].doctor_id,
                                     'role': 'Doctor'})
            else:
                return JsonResponse({'success': False, 'message': '密码错误'})
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
                if new_sex == 0 or new_sex == 1:
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
        show_all = data_json.get('showAll')
        if show_all:
            result = Photo.objects.filter(photo_realname__contains=title)
        else:
            if data_json.get('other_user_id') is not None:
                result = Photo.objects.filter(photo_realname__contains=title,
                                              photo_doctor__doctor_id=data_json.get('other_user_id'))
            else:
                result = Photo.objects.filter(photo_doctor__doctor_id=u_id, photo_realname__contains=title)
        apply_list = list(
            result.values('photo_id', 'photo_realname', 'photo_savename'))
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
        for photo in p_list:
            patient = Photo.objects.get(photo_id=photo['photo_id']).photo_patient
            doctor = Photo.objects.get(photo_id=photo['photo_id']).photo_doctor
            photo['patient'] = {
                'id': patient.patient_id,
                'name': patient.patient_name,
                'icon': get_patient_icon(patient.patient_id),
                'isDoctor': False,
                'age': patient.patient_age,
            }
            photo['photo_origin'] = BASEURL + photo['photo_savename'] + '_origin.png'
            photo['photo_promap'] = BASEURL + photo['photo_savename'] + '_promap.png'
            upload = Upload.objects.filter(doctor_id=u_id, photo_id=photo['photo_id'])
            if len(upload) > 0:
                photo['photo_upload'] = BASEURL + upload[0].upload_savename + '_upload.png'
            else:
                photo['photo_upload'] = ''
            if doctor.doctor_realname is not None and doctor.doctor_realname != '':
                name = doctor.doctor_realname
            else:
                name = doctor.doctor_username
            photo['doctor'] = {
                'id': doctor.doctor_id,
                'name': name,
                'icon': get_doctor_icon(doctor.doctor_id),
                'isDoctor': True,
                'age': doctor.doctor_age,
            }
        return JsonResponse({'success': True, 'message': '返回list成功', 'imageList': list(p_list), 'total': total},
                            safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})


def get_photo_list_for_patient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        u_id = data_json.get('user_id')
        d_id = data_json.get('id')
        pagenum = data_json.get('pagenum')  # 当前页码数
        pagesize = data_json.get('pagesize')  # 每页显示条目数
        print(u_id)
        result = Photo.objects.filter(photo_patient__patient_id=u_id)
        apply_list = list(
            result.values('photo_id', 'photo_realname', 'photo_savename'))
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
        for photo in p_list:
            patient = Photo.objects.get(photo_id=photo['photo_id']).photo_patient
            doctor = Photo.objects.get(photo_id=photo['photo_id']).photo_doctor
            photo['patient'] = {
                'id': patient.patient_id,
                'name': patient.patient_name,
                'icon': get_patient_icon(patient.patient_id),
                'isDoctor': False,
                'age': patient.patient_age,
            }
            photo['photo_origin'] = BASEURL + photo['photo_savename'] + '_origin.png'
            photo['photo_promap'] = BASEURL + photo['photo_savename'] + '_promap.png'
            upload = Upload.objects.filter(doctor_id=d_id, photo_id=photo['photo_id'])
            if len(upload) > 0:
                photo['photo_upload'] = BASEURL + upload[0].upload_savename + '_upload.png'
            else:
                photo['photo_upload'] = ''
            if doctor.doctor_realname is not None and doctor.doctor_realname != '':
                name = doctor.doctor_realname
            else:
                name = doctor.doctor_username
            photo['doctor'] = {
                'id': doctor.doctor_id,
                'name': name,
                'icon': get_doctor_icon(doctor.doctor_id),
                'isDoctor': True,
                'age': doctor.doctor_age,
            }
        return JsonResponse({'success': True, 'message': '返回list成功', 'imageList': list(p_list), 'total': total},
                            safe=False, status=200,
                            json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({})


def get_photo_info(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        p_id = data_json.get('photo_id')
        d_id = data_json.get('id')
        photo = Photo.objects.get(photo_id=p_id)
        return_object = {}
        patient = Photo.objects.get(photo_id=photo.photo_id).photo_patient
        doctor = Photo.objects.get(photo_id=photo.photo_id).photo_doctor
        return_object['patient'] = {
            'id': patient.patient_id,
            'name': patient.patient_name,
            'icon': get_patient_icon(patient.patient_id),
            'isDoctor': False,
            'age': patient.patient_age,
        }
        if doctor.doctor_realname is not None and doctor.doctor_realname != '':
            name = doctor.doctor_realname
        else:
            name = doctor.doctor_username
        return_object['doctor'] = {
            'id': doctor.doctor_id,
            'name': name,
            'icon': get_doctor_icon(doctor.doctor_id),
            'isDoctor': True,
            'age': doctor.doctor_age,
        }
        return_object['photo_id'] = photo.photo_id
        return_object['photo_savename'] = photo.photo_savename
        return_object['photo_realname'] = photo.photo_realname
        return_object['photo_origin'] = BASEURL + photo.photo_savename + '_origin.png'
        return_object['photo_promap'] = BASEURL + photo.photo_savename + '_promap.png'
        upload_single = Upload.objects.filter(doctor_id=d_id, photo_id=p_id)
        if len(upload_single) > 0:
            return_object['photo_upload'] = BASEURL + upload_single[0].upload_savename + '_upload.png'
        else:
            return_object['photo_upload'] = ''
        upload = Upload.objects.filter(photo_id=photo.photo_id)
        if len(upload) > 0:
            upload_list = []
            for single_upload in upload:
                temp_doctor = single_upload.doctor
                if temp_doctor.doctor_realname is not None and temp_doctor.doctor_realname != '':
                    name = temp_doctor.doctor_realname
                else:
                    name = temp_doctor.doctor_username
                upload_list.append({
                    'id': single_upload.upload_id,
                    'savename': single_upload.upload_savename,
                    'photo_upload': BASEURL + single_upload.upload_savename + '_upload.png',
                    'doctor': {
                        'id': temp_doctor.doctor_id,
                        'name': name,
                        'icon': get_doctor_icon(temp_doctor.doctor_id),
                        'isDoctor': True,
                        'age': temp_doctor.doctor_age,
                    }
                })
                return_object['photo_upload_list'] = upload_list
        else:
            return_object['photo_upload_list'] = []
        return_object['comments']=[]
        comments = Comment.objects.filter(photo_id=photo.photo_id)
        for comment in comments:
            temp_doctor = comment.doctor
            if temp_doctor.doctor_realname is not None and temp_doctor.doctor_realname != '':
                name = temp_doctor.doctor_realname
            else:
                name = temp_doctor.doctor_username
            return_object['comments'].append({
                'id': comment.comment_id,
                'content': comment.content,
                'doctor': {
                    'id': temp_doctor.doctor_id,
                    'name': name,
                    'icon': get_doctor_icon(temp_doctor.doctor_id),
                    'isDoctor': True,
                    'age': temp_doctor.doctor_age,
                }
            })

        return JsonResponse({'success': True, 'message': '返回list成功', 'photo': return_object}, status=200)
    else:
        return JsonResponse({})


def send_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        photo_id = request.POST.get('photo_id')
        doctor_id = request.POST.get('doctor_id')
        if content is None or photo_id is None or doctor_id is None:
            return JsonResponse({'success': False, 'message': '参数错误'}, status=400)
        comment = Comment(
            content=content,
            photo_id=photo_id,
            doctor_id=doctor_id
        )
        comment.save()
        return JsonResponse({'success': True, 'message': '评论成功'}, status=200)
    else:
        return JsonResponse({})

def receive_origin(request):
    if request.method == 'POST':
        image = request.FILES.get('pic_img')
        u_id = request.POST.get('user_id')
        p_id = request.POST.get('id')

        obj = Photo()
        obj.photo_doctor = Doctor.objects.get(doctor_id=u_id)
        print(p_id)
        obj.photo_patient = Patient.objects.get(patient_id=p_id)

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fn = time.strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(base_dir, 'media', 'test', str(obj.photo_id))
        with open(file_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        img = cv2.imread(file_path)
        new_path = './media/test/' + str(obj.photo_patient.patient_id) + '-' + str(
            obj.photo_doctor.doctor_id) + '-' + fn + '.png'
        cv2.imwrite(new_path, img, )  # 保存为png
        os.remove(file_path)

        obj.photo_realname = os.path.basename(os.path.splitext(image.name)[0])
        obj.photo_savename = str(obj.photo_patient.patient_id) + '-' + str(obj.photo_doctor.doctor_id) + '-' + fn
        obj.save()
        if BASEURL.startswith("http://10.251.0.251"):
            subprocess.Popen("python ./test/test.py" + " " + os.path.basename(new_path), shell=True)
        else:
            print("dest_________________________________________")
            subprocess.Popen("python ./test/local_test.py" + " " + os.path.basename(new_path), shell=True)

        return JsonResponse('message="上传成功', safe=False)
    else:
        return JsonResponse({})


def receive_upload(request):
    if request.method == 'POST':
        image = request.FILES.get('pic_img')
        p_id = request.POST.get('photo_id')
        d_id = request.POST.get('id')
        photo = Photo.objects.get(photo_id=p_id)
        doctor = Doctor.objects.get(doctor_id=d_id)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, 'media', 'test', photo.photo_savename)
        with open(file_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        img = cv2.imread(file_path)
        fn = time.strftime('%Y%m%d%H%M%S')
        upload = Upload()
        upload.doctor = doctor
        upload.photo = photo
        upload.upload_savename = str(photo.photo_id) + '-' + str(doctor.doctor_id) + '-' + fn
        cv2.imwrite('./media/test/' + upload.upload_savename + '_upload.png', img, )  # 保存为png
        os.remove(file_path)
        upload.save()
        return JsonResponse('message="上传成功', safe=False)
    else:
        return JsonResponse({})


def delete_picture(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        photo_id = data_json.get('photoID')
        print(photo_id)
        p = Photo.objects.filter(photo_id=photo_id)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '图片'}, status=404)
        else:
            photo = Photo.objects.get(photo_id=photo_id)
            save_name = photo.photo_savename
            try:
                os.remove('./media/test/' + save_name + '_promap.png')
                os.remove('./media/test/' + save_name + '_origin.png')
            except FileNotFoundError as e:
                print(e)
            Comment.objects.filter(photo=photo).delete()
            photos = Upload.objects.filter(photo=photo)
            for single_photo in photos:
                os.remove('./media/test/' + single_photo.upload_savename + '_upload.png')
            photos.delete()
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


def add_patient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('name')
        if len(name) == 0:
            return JsonResponse({'success': False, 'message': '姓名不能为空'}, status=404)
        else:
            new_p = Patient()
            new_p.patient_name = name
            new_p.save()
            return JsonResponse({'success': True, 'message': '添加患者成功', 'patient_ID': new_p.patient_id}, status=200)
    else:
        return JsonResponse({})


def find_patient(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        name = data_json.get('name')
        p = Patient.objects.filter(patient_name__contains=name)
        res = []
        if len(p) == 0:
            # new_p = Patient()
            # new_p.patient_name = name
            # new_p.save()
            return JsonResponse({'success': False, 'message': '未查询到患者'}, status=200)
        else:
            for pa in p:
                usr = {}
                usr['id'] = pa.patient_id
                usr['name'] = pa.patient_name
                usr['isDoctor'] = False
                usr['age'] = pa.patient_age
                usr['icon'] = get_patient_icon(pa.patient_id)

                res.append(usr)
            return JsonResponse({'p_list': res, 'success': True, 'message': '查询患者成功'}, status=200)
    else:
        return JsonResponse({})


def get_patient_info(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        patient_id = data_json.get('id')
        p = Patient.objects.filter(patient_id=patient_id)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '不存在该患者'}, status=404)
        else:
            patient = Patient.objects.get(patient_id=patient_id)
            return JsonResponse(
                {'success': True, 'message': '查询成功',
                 'user': {'name': patient.patient_name,
                          'age': patient.patient_age,
                          'height': patient.patient_height,
                          'weight': patient.patient_weight,
                          'sex': patient.patient_sex,
                          'email': patient.patient_email,
                          'icon': get_patient_icon(patient_id),
                          'phone': patient.patient_phone,
                          'address': patient.patient_address,
                          'isDoctor': False,
                          'id': patient_id
                          }
                 },
                status=200)
    else:
        return JsonResponse({})


def receive_patient_icon(request):
    if request.method == 'POST':
        image = request.FILES.get('pic_img')
        p_id = request.POST.get('id')
        patient = Patient.objects.get(patient_id=p_id)
        if patient.patient_icon is not None and patient.patient_icon != '':
            try:
                os.remove("./media/test/patient/" + patient.patient_icon + ".png")
            except Exception as e:
                pass
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fn = time.strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(base_dir, 'media', 'test', 'patient', str(patient.patient_id))
        with open(file_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        img = cv2.imread(file_path)
        cv2.imwrite('./media/test/patient/' + str(patient.patient_id) + '-' + fn + '.png', img, )  # 保存为png
        os.remove(file_path)
        patient.patient_icon = str(patient.patient_id) + '-' + fn
        patient.save()
        return JsonResponse('message="上传成功', safe=False)
    else:
        return JsonResponse({})


def edit_patient_info(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        patient_id = data_json.get('id')
        p = Patient.objects.filter(patient_id=patient_id)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '不存在该患者'}, status=404)
        else:
            patient = Patient.objects.get(patient_id=patient_id)
            patient.patient_name = data_json.get('name')
            patient.patient_age = int(data_json.get('age'))
            patient.patient_height = int(data_json.get('height'))
            patient.patient_weight = int(data_json.get('weight'))
            patient.patient_address = data_json.get('address')
            patient.patient_phone = data_json.get('phone')
            patient.patient_email = data_json.get('email')
            if data_json.get('sex') is not None:
                patient.patient_sex = int(data_json.get('sex'))
                print("??")
            patient.save()
            return JsonResponse({'success': True, 'message': '修改信息成功'}, status=200)
    else:
        return JsonResponse({})


def get_doctor_info(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        doctor_id = data_json.get('id')
        p = Doctor.objects.filter(doctor_id=doctor_id)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '不存在该医生'}, status=404)
        else:
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            return JsonResponse(
                {'success': True, 'message': '查询成功',
                 'user': {
                     'username': doctor.doctor_username,
                     'name': doctor.doctor_realname,
                     'age': doctor.doctor_age,
                     'sex': doctor.doctor_sex,
                     'email': doctor.doctor_email,
                     'icon': get_doctor_icon(doctor_id),
                     'phone': doctor.doctor_phone,
                     'isDoctor': True,
                     'id': doctor_id
                 }
                 },
                status=200)
    else:
        return JsonResponse({})


def receive_doctor_icon(request):
    if request.method == 'POST':
        image = request.FILES.get('pic_img')
        p_id = request.POST.get('id')
        doctor = Doctor.objects.get(doctor_id=p_id)
        if doctor.doctor_icon is not None and doctor.doctor_icon != '':
            try:
                os.remove("./media/test/doctor/" + doctor.doctor_icon + ".png")
            except Exception as e:
                pass
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fn = time.strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(base_dir, 'media', 'test', 'doctor', str(doctor.doctor_id))
        with open(file_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        img = cv2.imread(file_path)
        cv2.imwrite('./media/test/doctor/' + str(doctor.doctor_id) + '-' + fn + '.png', img, )  # 保存为png
        os.remove(file_path)
        doctor.doctor_icon = str(doctor.doctor_id) + '-' + fn
        doctor.save()
        return JsonResponse('message="上传成功', safe=False)
    else:
        return JsonResponse({})


def edit_doctor_info(request):
    if request.method == 'POST':
        data_json = json.loads(request.body)
        doctor_id = data_json.get('id')
        p = Doctor.objects.filter(doctor_id=doctor_id)
        if len(p) == 0:
            return JsonResponse({'success': False, 'message': '不存在该患者'}, status=404)
        else:
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            doctor.doctor_name = data_json.get('name')
            doctor.doctor_age = int(data_json.get('age'))
            doctor.doctor_phone = data_json.get('phone')
            doctor.doctor_email = data_json.get('email')
            if data_json.get('sex') is not None:
                doctor.doctor_sex = int(data_json.get('sex'))
                print("??")
            doctor.save()
            return JsonResponse({'success': True, 'message': '修改信息成功'}, status=200)
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
