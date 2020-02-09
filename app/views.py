#!/usr/bin/env python
import random, json
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.emailSend import send_code_email
from app_web.settings import MEDIA_URL
from web import forms, models
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from . import serializers
User = auth.get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


# 注册发送邮箱验证码
def SendEmail(request):
    data = {}
    if request.method == 'POST':
        email = request.POST.get("email", None)
        if send_code_email(email):
            data['status'] = 200
            return JsonResponse(data)
        else:
            data['status'], data['code'] = 403, 'identifying code error'
            return JsonResponse(data)


@csrf_exempt
def signup(request):
    data = {}
    if request.method == 'POST':
        email = request.POST.get("email", None)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        code = request.POST.get("code", None)
        # register_user = {"email": email, "username": username, "password": password, "code": code}
        # form = forms.UserCreationForm(register_user)
        try:
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                data['status'] = 403
                data['error'] = "User Exists"
            else:
                verifyCode = models.EmailVerifyRecord.objects.filter(email__exact=email).first()
                verifyCode = verifyCode.code
                if verifyCode == code:  # 表示注册成功
                    # user = form.save()
                    user = User.objects.create(username=username, password=password, email=email)
                    models.UserDepressionScore.objects.create(user_id=user, depression_score=100)
                    data['status'], data['user_id'], data['username'], data[
                        'password'] = 200, user.user_id, user.username, user.password
                else:
                    data['status'], data['error'] = 403, 'identifying code input error'
        except Exception as e:
            print("错误信息 : ", e)
            data['status'] = 500
            data['error'] = "Server Error"
    return JsonResponse(data)


@csrf_exempt
def result_api(request):
    # 图片传回以图片id方式
    # global new_result, user_score
    if request.method == 'POST':
        result = json.loads(request.body)
        test_user = User.objects.get(user_id=result['user_id'])
        if result['test_type'] == 'BECK':
            # 不同量表
            user_score = models.UserDepressionScore.objects.filter(user_id=test_user).update(scale=result['test_score'])
            new_result = models.TestResultScale.objects.create(user_id=test_user, score=result['test_score'],
                                                               user_option=result['user_option'])
        if result['test_type'] == 'HBQCS':
            user_score = models.UserDepressionScore.objects.filter(user_id=test_user).update(grand=result['test_score'])
            new_result = models.TestResultGrand.objects.create(user_id=test_user, score=result['test_score'],
                                                               picture=result['picture_id'],
                                                               reaction_time=result['reaction_time'],
                                                               user_option=result['user_option'])
        if result['test_type'] == 'JBFS':
            user_score = models.UserDepressionScore.objects.filter(user_id=test_user).update(
                gradual=result['test_score'])
            new_result = models.TestResultGradual.objects.create(user_id=test_user, score=result['test_score'],
                                                                 picture=result['picture_id'],
                                                                 reaction_time=result['reaction_time'],
                                                                 user_option=result['user_option'])
            # d_value = result['d_value']
        if result['test_type'] == 'DTCFS':
            user_score = models.UserDepressionScore.objects.filter(user_id=test_user).update(point=result['test_score'])
            new_result = models.TestResultPoint.objects.create(user_id=test_user, score=result['test_score'],
                                                               picture=result['picture_id'],
                                                               reaction_time=result['reaction_time'])
            # d_value = result['d_value']coordinate = result['coord'], target = result['target'],
        if result['test_type'] == 'DZSB':
            user_score = models.UserDepressionScore.objects.filter(user_id=test_user).update(short=result['test_score'])
            new_result = models.TestResultShort.objects.create(user_id=test_user, score=result['test_score'],
                                                               picture=result['picture_id'],
                                                               reaction_time=result['reaction_time'],
                                                               user_option=result['user_option'])
        if result['test_type'] == 'STROOP':
            user_score = models.UserDepressionScore.objects.filter(user_id=test_user).update(
                stroop=result['test_score'])
            new_result = models.TestResultStroop.objects.create(user_id=test_user, score=result['test_score'],
                                                                picture=result['picture_id'],
                                                                reaction_time=result['reaction_time'],
                                                                user_option=result['user_option'])
            # interfere_word = result['inter_word']

        """更新总分数"""
        new_score = models.UserDepressionScore.objects.filter(user_id=test_user).values_list('grand', 'gradual',
                                                                                             'short', 'point', 'stroop',
                                                                                             'scale')
        new_score = sum([i // 6 for i in new_score[0]])
        models.UserDepressionScore.objects.filter(user_id=test_user).update(depression_score=new_score)

        if new_result and user_score:  # 出现错误返回信息
            return JsonResponse({'status': 201, 'error': ''})
    return JsonResponse({'status': 403, 'error': ''})


@csrf_exempt
def test_api(request):
    if request.method == 'POST':
        # 图片随机处理，同时发送图片id和图片，接收只接受图片id
        result = json.loads(request.body)
        if result['test_type'] == 'DTCFS':
            pics = models.TablePicture.objects.filter(picsign='1').values('pid', 'img')
            rand_img = random.sample(list(pics), 30)
        elif result['test_type'] in ['JBFS', 'HBQCS', 'STROOP', 'DTCFS', 'DZSB']:
            pics = models.TablePicture.objects.filter(picsign='1').values('pid', 'img')
            rand_img = random.sample(list(pics), 10)
        for i in range(len(rand_img)):
            rand_img[i]['img'] = "http://218.244.148.142" + MEDIA_URL + str(rand_img[i]['img'])

        return HttpResponse(json.dumps(rand_img))
    return JsonResponse({'status': 500, 'error': ''})


@csrf_exempt
def app_media(request):
    if request.method == 'POST':
        result = json.loads(request.body)
        if result['type'] == 'essay':
            all_essays = models.TableEssay.objects.values()
            return HttpResponse(json.dumps(list(all_essays)))
        if result['type'] == 'video':
            video = models.TableVideo.objects.values()
            return HttpResponse(json.dumps(list(video)))


@csrf_exempt
def login_view(request):
    message = ""
    if request.method == "POST":
        login_user = json.loads(request.body)
        username = login_user['username']
        password = login_user['password']
        try:
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:  # 这里只是由于开发时，用的django的超级用户，没有自动创建score
                    models.UserDepressionScore.objects.get_or_create(user_id=user)
                auth.login(request, user)
                return JsonResponse(
                    {"status": 201, "user_id": user.user_id, 'username': username, 'password': password})
            else:
                message = "密码不正确！"
        except:
            message = "用户不存在！"
    return JsonResponse({"status": 403, "error": message})


def logout_view(request):
    auth.logout(request)
    return HttpResponse('logout')


@csrf_exempt
def profile(request):
    user = request.user
    if request.method == 'GET':
        data = {'nickname': user.nickname, 'age': user.age, 'sex': user.sex, 'address': user.address,
                'phone': user.phone, 'introduction': user.introduction}
        return JsonResponse(data)
    elif request.method == 'POST':
        default_data = {
            'nickname': user.nickname,
            'email': user.email,
            'avatar': user.avatar,
            'age': user.age,
            'sex': user.sex,
            'address': user.address,
            'occupation': user.occupation,
            'phone': user.phone,
            'introduction': user.introduction,
        }
        default_data.update(request.POST.dict())
        form = forms.UserInfo(default_data, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 201})
        else:
            message = '请检查填写信息~'
            return JsonResponse({'status': 403, 'msg': message})
    return JsonResponse({'status': 500})


@csrf_exempt
def score(request, pk, score_type):
    if request.method == 'GET':
        if score_type == 'SCORE':
            score = models.UserDepressionScore.objects.filter(user_id=pk).values('depression_score', 'grand', 'gradual',
                                                                                 'short', 'point', 'stroop', 'scale')
            data = {'score': list(score)}
            return render(request, 'app/score.html', {'score': data})
        if score_type == 'HBQCS':
            grand = models.TestResultGrand.objects.filter(user_id=pk).values('score').order_by('-date')[:7]
            data = {'score': list(grand)}
            return render(request, 'app/score_grand.html', {'score': data})
        if score_type == 'JBFS':
            gradual = models.TestResultGradual.objects.filter(user_id=pk).values('score').order_by('-date')[:7]
            data = {'score': list(gradual)}
            return render(request, 'app/score_gradual.html', {'score': data})
        if score_type == 'DTCFS':
            point = models.TestResultPoint.objects.filter(user_id=pk).values('score').order_by('-date')[:7]
            data = {'score': list(point)}
            return render(request, 'app/score_point.html', {'score': data})
        if score_type == 'STROOP':
            stroop = models.TestResultStroop.objects.filter(user_id=pk).values('score').order_by('-date')[:7]
            data = {'score': list(stroop)}
            return render(request, 'app/score_stroop.html', {'score': data})
        if score_type == 'DZSB':
            short = models.TestResultShort.objects.filter(user_id=pk).values('score').order_by('-date')[:7]
            data = {'score': list(short)}
            return render(request, 'app/score_short.html', {'score': data})
        if score_type == 'BECK':
            scale = models.TestResultScale.objects.filter(user_id=pk).values('score').order_by('-date')[:7]
            data = {'score': list(scale)}
            return render(request, 'app/score_scale.html', {'score': data})
