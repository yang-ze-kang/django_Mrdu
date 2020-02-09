#!/usr/bin/env python
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from app_web.settings import MEDIA_ROOT
from . import forms, models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime, os
from collections import Counter
from django.db.models import Max, Avg, Min

User = auth.get_user_model()


def timeRange(request):
    # from .scaleQues import bk_ques
    # for i in bk_ques.values():
    #     models.TableScale.objects.create(type_scale=1,content=i)
    # return JsonResponse({
    #     '200':'YES'
    # })
    return render(request, 'web/table/a.html', )


def page_stroop(request):
    try:
        data = models.TestResultStroop.objects.filter(user_id=request.user)
        if request.method == 'POST':
            start = [int(i) for i in request.POST['timerange1'].split('-')]
            end = [int(i) for i in request.POST['timerange2'].split('-')]
            start = datetime.datetime(start[0], start[1], start[2])
            end = datetime.datetime(end[0], end[1], end[2] + 1)
            data = data.filter(date__gte=start, date__lte=end)
        # 平均反应时间
        times = list(data.values_list('reaction_time'))
        lengthOftimes = len(times)
        lenOfEachTime = 25
        tmp = []
        for idx, each_time in enumerate(times):
            each_time = each_time[0].split('|')
            times[idx] = [int(t) for t in each_time]
            tmp.extend([max(times[idx]), min(times[idx])])
        avg_time = sum([sum([t / lenOfEachTime for t in each_time]) / lengthOftimes for each_time in times])
        # 最长反应时间
        max_time = max(tmp)
        stroop = data.filter(reaction_time__icontains=max_time)
        pics = []
        for test in stroop:
            pic_ids = [int(id) for id in sorted(Counter(test.picture.split('|')))[:2]]
            photos = models.TablePicture.objects.filter(pid__in=pic_ids)
            # 对应测试图片的id，方便显示
            # 找对应的用时最多的emotion
            highest_e = sorted(Counter([pho.emotion for pho in photos]))[0]
            pics.append([test, list(photos), highest_e])
        # 偏离程度
        from .stroopInter import emotions
        opts = list(data.values_list("interfere_word", "user_option", "id", 'date', 'picture'))
        maxDevia = []
        for idx in range(len(opts)):
            opts[idx] = list(opts[idx])
            opts[idx][0] = [emotions[i] for i in opts[idx][0].split('|')]  # interfere_word
            opts[idx][1] = [emotions[i] for i in opts[idx][1].split('|')]  # user_option
            opts[idx][4] = [int(id) for id in opts[idx][4].split('|')]  # picture
            photos = models.TablePicture.objects.filter(pid__in=opts[idx][4])
            emo = [pho.emotion for pho in photos]
            maxDevia.append(
                {'测试id': opts[idx][2], '测试时间': opts[idx][3], 'i_w': opts[idx][0], 'u_a': opts[idx][1], 'r_a': emo})
        # 最短反应时间
        min_time = min(tmp)
        # 平均分，最高分，最低分
        scores = data.aggregate(avg_score=Avg("score"), max_score=Max("score"), min_score=Min("score"))
    except:
        avg_time, max_time, min_time, pics, maxDevia, data = None, None, None, None, None, None
        scores = {'avg_score': None, 'max_score': None, 'min_score': None}
    return render(request, 'web/table/stroop.html',
                  {'avg_time': avg_time, 'max_time': max_time, 'min_time': min_time, 'pics': pics,
                   'avg_score': scores['avg_score'], 'max_score': scores['max_score'],
                   'min_score': scores['min_score'], 'devia': maxDevia, 'data': data})


def page_point(request):
    try:
        data = models.TestResultPoint.objects.filter(user_id=request.user)
        if request.method == 'POST':
            start = [int(i) for i in request.POST['timerange1'].split('-')]
            end = [int(i) for i in request.POST['timerange2'].split('-')]
            start = datetime.datetime(start[0], start[1], start[2])
            end = datetime.datetime(end[0], end[1], end[2] + 1)
            data = data.filter(date__gte=start, date__lte=end)
        # 平均反应时间
        times = list(data.values_list('reaction_time'))
        lengthOftimes = len(times)
        lenOfEachTime = 25
        tmp = []
        for idx, each_time in enumerate(times):
            each_time = each_time[0].split('|')
            times[idx] = [int(t) for t in each_time]
            tmp.extend([max(times[idx]), min(times[idx])])
        avg_time = sum([sum([t / lenOfEachTime for t in each_time]) / lengthOftimes for each_time in times])
        # 最长反应时间
        max_time = max(tmp)
        point = data.filter(reaction_time__icontains=max_time)
        pics = []
        for test in point:
            pic_ids = [[int(id) for id in ids.split(',')] for ids in test.picture.split('|')]
            tag_ids = [[int(id) for id in ids.split(',')] for ids in test.target.split('|')]
            photos = []
            thotos = []
            for pids, tids in zip(pic_ids, tag_ids):
                photos.append(models.TablePicture.objects.filter(pid__in=pids))
                thotos.append(models.TablePicture.objects.filter(pid__in=tids))
                # 对应测试图片的id，方便显示
            pics.append([test, photos, thotos])
        # 最短反应时间
        min_time = min(tmp)
        # 平均分，最高分，最低分
        scores = data.aggregate(avg_score=Avg("score"), max_score=Max("score"), min_score=Min("score"))
        # 坐标处理
        coors = list(data.values_list('id', 'date', 'coordinate', 'score'))
        tags = []
        for i in range(len(coors)):
            coors[i] = list(coors[i])
            coors[i][2] = coors[i][2].split(';')  # 图片组
            for j in range(len(coors[i][2])):
                tmp = coors[i][2][j].split('|')  # 坐标组
                coors[i][2][j] = tmp[:-1]
                tags.append([int(coor) for coor in tmp[-1].split(',')])
                for k in range(len(coors[i][2][j])):
                    coors[i][2][j][k] = [int(coor) for coor in coors[i][2][j][k].split(',')]
        cDetail = []
        cors = []
        for i in coors:
            cDetail.append({'id': i[0], 'date': i[1], 'coor': i[2], 'score': i[3]})
            cors += i[2][0]
        # 坐标均值处理
        l_tags = len(tags)
        l_coor = len(cors)
        avg_tar_x = sum([x[0] for x in tags]) / l_tags
        # avg_tar_y = sum([y[1] for y in tags])/l_tags
        avg_coor_x = sum([x[0] for x in cors]) / l_coor
        avg_coor_y = sum([y[1] for y in cors]) / l_coor
    except:
        avg_time, max_time, min_time, pics, cDetail, tags, cors, avg_coor_x, avg_coor_y, avg_tar_x = None, None, None, None, None, None, None, None, None, None
        scores = {'avg_score': None, 'max_score': None, 'min_score': None}
    return render(request, 'web/table/point.html',
                  {'avg_time': avg_time, 'max_time': max_time, 'min_time': min_time, 'pics': pics,
                   'avg_score': scores['avg_score'], 'max_score': scores['max_score'],
                   'min_score': scores['min_score'], 'cDetail': cDetail, 'tar': tags, 'coors': cors,
                   'a_c_x': avg_coor_x, 'a_c_y': avg_coor_y, 'a_t_x': avg_tar_x})


def page_short(request):
    try:
        data = models.TestResultShort.objects.filter(user_id=request.user)
        if request.method == 'POST':
            start = [int(i) for i in request.POST['timerange1'].split('-')]
            end = [int(i) for i in request.POST['timerange2'].split('-')]
            start = datetime.datetime(start[0], start[1], start[2])
            end = datetime.datetime(end[0], end[1], end[2] + 1)
            data = data.filter(date__gte=start, date__lte=end)
        # 平均反应时间
        times = list(data.values_list('reaction_time'))
        lengthOftimes = len(times)
        lenOfEachTime = 25
        tmp = []
        for idx, each_time in enumerate(times):
            each_time = each_time[0].split('|')
            times[idx] = [int(t) for t in each_time]
            tmp.extend([max(times[idx]), min(times[idx])])
        avg_time = sum([sum([t / lenOfEachTime for t in each_time]) / lengthOftimes for each_time in times])
        # 最长反应时间
        max_time = max(tmp)
        short = data.filter(reaction_time__icontains=max_time)
        pics = []
        for test in short:
            pic_ids = [int(id) for id in sorted(Counter(test.picture.split('|')))[:2]]
            photos = models.TablePicture.objects.filter(pid__in=pic_ids)
            # 对应测试图片的id，方便显示
            # 找对应的用时最多的emotion
            highest_e = sorted(Counter([pho.emotion for pho in photos]))[0]
            pics.append([test, list(photos), highest_e])
        # 偏离程度
        opts = list(data.values_list("right_option", "user_option", "id", 'date', 'picture'))
        maxDevia = []
        for idx in range(len(opts)):
            opts[idx] = list(opts[idx])
            opts[idx][0] = [int(i) for i in opts[idx][0].split('|')]
            opts[idx][1] = [int(i) for i in opts[idx][1].split('|')]
            pianli = [x - y for x, y in zip(opts[idx][1], opts[idx][0])]  # user-right
            index = pianli.index(max(pianli))  # 图片序列的位置
            opts[idx][4] = [int(id) for id in opts[idx][4].split('|')]
            index = opts[idx][4][index]  # 找到pid
            indexPho = list(models.TablePicture.objects.filter(pid=index))
            maxDevia.append(
                {'最大值': max(pianli), '测试位置': [index, indexPho], '测试id': opts[idx][2], '测试时间': opts[idx][3],
                 '偏离序列': pianli})
        # 最短反应时间
        min_time = min(tmp)
        # 平均分，最高分，最低分
        scores = data.aggregate(avg_score=Avg("score"), max_score=Max("score"), min_score=Min("score"))
    except:
        avg_time, max_time, min_time, pics, maxDevia, data = None, None, None, None, None, None
        scores = {'avg_score': None, 'max_score': None, 'min_score': None}
    return render(request, 'web/table/short.html',
                  {'avg_time': avg_time, 'max_time': max_time, 'min_time': min_time, 'pics': pics,
                   'avg_score': scores['avg_score'], 'max_score': scores['max_score'],
                   'min_score': scores['min_score'], 'devia': maxDevia, 'data': data})


def page_scale(request):
    try:
        data = models.TestResultScale.objects.filter(user_id=request.user)
        if request.method == 'POST':
            start = [int(i) for i in request.POST['timerange1'].split('-')]
            end = [int(i) for i in request.POST['timerange2'].split('-')]
            start = datetime.datetime(start[0], start[1], start[2])
            end = datetime.datetime(end[0], end[1], end[2] + 1)
            data = data.filter(date__gte=start, date__lte=end)
        # 平均反应时间
        times = list(data.values_list('reaction_time'))
        lengthOftimes = len(times)
        lenOfEachTime = 25
        tmp = []
        for idx, each_time in enumerate(times):
            each_time = each_time[0].split('|')
            times[idx] = [int(t) for t in each_time]
            tmp.extend([max(times[idx]), min(times[idx])])
        avg_time = sum([sum([t / lenOfEachTime for t in each_time]) / lengthOftimes for each_time in times])
        # 最长反应时间
        max_time = max(tmp)
        scale = data.filter(reaction_time__icontains=max_time)
        ques = []
        from .scaleQues import bk_ques
        for test in scale:
            que_ids = [int(id) for id in test.user_option.split('|')]
            ans = [bk_ques[ind+1][i] for ind,i in enumerate(que_ids)]
            ques.append([test.id,ans])
        # 最短反应时间
        min_time = min(tmp)
        # 平均分，最高分，最低分
        scores = data.aggregate(avg_score=Avg("score"), max_score=Max("score"), min_score=Min("score"))
    except:
        avg_time, max_time, min_time, data,ques = None, None, None, None, None
        scores = {'avg_score': None, 'max_score': None, 'min_score': None}
    return render(request, 'web/table/scale.html',
                  {'avg_time': avg_time, 'max_time': max_time, 'min_time': min_time,
                   'avg_score': scores['avg_score'], 'max_score': scores['max_score'],
                   'min_score': scores['min_score'], 'data': data,'ques':ques})


def page_gradual(request):
    try:
        data = models.TestResultGradual.objects.filter(user_id=request.user)
        if request.method == 'POST':
            start = [int(i) for i in request.POST['timerange1'].split('-')]
            end = [int(i) for i in request.POST['timerange2'].split('-')]
            start = datetime.datetime(start[0], start[1], start[2])
            end = datetime.datetime(end[0], end[1], end[2] + 1)
            data = data.filter(date__gte=start, date__lte=end)
        # 平均反应时间
        times = list(data.values_list('reaction_time'))
        lengthOftimes = len(times)
        lenOfEachTime = 25
        tmp = []
        for idx, each_time in enumerate(times):
            each_time = each_time[0].split('|')
            times[idx] = [int(t) for t in each_time]
            tmp.extend([max(times[idx]), min(times[idx])])
        avg_time = sum([sum([t / lenOfEachTime for t in each_time]) / lengthOftimes for each_time in times])
        # 最长反应时间
        max_time = max(tmp)
        gradual = data.filter(reaction_time__icontains=max_time)
        pics = []
        for test in gradual:
            pic_ids = [int(id) for id in sorted(Counter(test.picture.split('|')))[:2]]  # maxtime下前2个多的picture
            photos = models.TablePicture.objects.filter(pid__in=pic_ids)
            # 对应测试图片的id，方便显示
            # 找对应的用时最多的emotion
            highest_e = sorted(Counter([pho.emotion for pho in photos]))[0]
            pics.append([test, list(photos), highest_e])
        # D值处理
        opts = list(data.values_list("d_value", "id", 'date'))
        maxDevia = []
        dList = []
        maxDevia.append({'偏离序列': dList})
        for idx in range(len(opts)):
            dList.append(opts[idx][0])
            maxDevia.append(
                {'测试id': opts[idx][1], '测试时间': opts[idx][2],
                 'D值': opts[idx][0]})
        # 最短反应时间
        min_time = min(tmp)
        # 平均分，最高分，最低分
        scores = data.aggregate(avg_score=Avg("score"), max_score=Max("score"), min_score=Min("score"))
    except:
        avg_time, max_time, min_time, pics, maxDevia, data = None, None, None, None, None, None
        scores = {'avg_score': None, 'max_score': None, 'min_score': None}
    return render(request, 'web/table/gradual.html',
                  {'avg_time': avg_time, 'max_time': max_time, 'min_time': min_time, 'pics': pics,
                   'avg_score': scores['avg_score'], 'max_score': scores['max_score'],
                   'min_score': scores['min_score'], 'devia': maxDevia, 'data': data})


def page_grand(request):
    try:
        data = models.TestResultGrand.objects.filter(user_id=request.user)
        if request.method == 'POST':
            start = [int(i) for i in request.POST['timerange1'].split('-')]
            end = [int(i) for i in request.POST['timerange2'].split('-')]
            start = datetime.datetime(start[0], start[1], start[2])
            end = datetime.datetime(end[0], end[1], end[2] + 1)
            data = data.filter(date__gte=start, date__lte=end)
        # 平均反应时间
        times = list(data.values_list('reaction_time'))
        lengthOftimes = len(times)
        lenOfEachTime = 25
        tmp = []
        for idx, each_time in enumerate(times):
            each_time = each_time[0].split('|')
            times[idx] = [int(t) for t in each_time]
            tmp.extend([max(times[idx]), min(times[idx])])
        avg_time = sum([sum([t / lenOfEachTime for t in each_time]) / lengthOftimes for each_time in times])
        # 最长反应时间
        max_time = max(tmp)
        grand = data.filter(reaction_time__icontains=max_time)
        pics = []
        for test in grand:
            pic_ids = [int(id) for id in sorted(Counter(test.picture.split('|')))[:2]]
            photos = models.TablePicture.objects.filter(pid__in=pic_ids)
            # 对应测试图片的id，方便显示
            # 找对应的用时最多的emotion
            highest_e = sorted(Counter([pho.emotion for pho in photos]))[0]
            pics.append([test, list(photos), highest_e])
        # 偏离程度
        opts = list(data.values_list("right_option", "user_option", "id", 'date', 'picture'))
        maxDevia = []
        for idx in range(len(opts)):
            opts[idx] = list(opts[idx])
            opts[idx][0] = [int(i) for i in opts[idx][0].split('|')]
            opts[idx][1] = [int(i) for i in opts[idx][1].split('|')]
            pianli = [x - y for x, y in zip(opts[idx][1], opts[idx][0])]  # user-right
            index = pianli.index(max(pianli))  # 图片序列的位置
            opts[idx][4] = [int(id) for id in opts[idx][4].split('|')]
            index = opts[idx][4][index]  # 找到pid
            indexPho = list(models.TablePicture.objects.filter(pid=index))
            maxDevia.append(
                {'最大值': max(pianli), '测试位置': [index, indexPho], '测试id': opts[idx][2], '测试时间': opts[idx][3],
                 '偏离序列': pianli})
        # 最短反应时间
        min_time = min(tmp)
        # 平均分，最高分，最低分
        scores = data.aggregate(avg_score=Avg("score"), max_score=Max("score"), min_score=Min("score"))
    except:
        avg_time, max_time, min_time, pics, maxDevia, data = None, None, None, None, None, None
        scores = {'avg_score': None, 'max_score': None, 'min_score': None}
    return render(request, 'web/table/grand.html',
                  {'avg_time': avg_time, 'max_time': max_time, 'min_time': min_time, 'pics': pics,
                   'avg_score': scores['avg_score'], 'max_score': scores['max_score'],
                   'min_score': scores['min_score'], 'devia': maxDevia, 'data': data})


def table_score(request):
    data = models.UserDepressionScore.objects.filter(user_id=request.user)
    score = dict()
    score['grand'] = models.TestResultGrand.objects.filter(user_id=request.user).values('id', 'score', 'date')
    score['scale'] = models.TestResultScale.objects.filter(user_id=request.user).values('id', 'score', 'date')
    score['stroop'] = models.TestResultStroop.objects.filter(user_id=request.user).values('id', 'score', 'date')
    score['short'] = models.TestResultShort.objects.filter(user_id=request.user).values('id', 'score', 'date')
    score['point'] = models.TestResultPoint.objects.filter(user_id=request.user).values('id', 'score', 'date')
    score['gradual'] = models.TestResultGradual.objects.filter(user_id=request.user).values('id', 'score', 'date')
    if request.method == "POST":
        start = [int(i) for i in request.POST['timerange1'].split('-')]
        end = [int(i) for i in request.POST['timerange2'].split('-')]
        start = datetime.datetime(start[0], start[1], start[2])
        end = datetime.datetime(end[0], end[1], end[2] + 1)
        score['grand'] = score['grand'].filter(date__gte=start, date__lte=end)
        score['scale'] = score['scale'].filter(date__gte=start, date__lte=end)
        score['stroop'] = score['stroop'].filter(date__gte=start, date__lte=end)
        score['short'] = score['short'].filter(date__gte=start, date__lte=end)
        score['point'] = score['point'].filter(date__gte=start, date__lte=end)
        score['gradual'] = score['gradual'].filter(date__gte=start, date__lte=end)
    return render(request, 'web/table/Score.html', {'data': data, 'score': score})


@login_required
def logout_web(request):
    logout(request)
    return redirect("web:login")


@login_required
def profile_web(request):
    user = request.user
    return render(request, 'web/index/profile.html', locals())


@login_required
def profile_update(request):
    if request.method == "POST":
        form = forms.UserInfo(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            request.user.save()
            return redirect('web:profile')
    else:
        default_data = {
            'nickname': request.user.nickname,
            'email': request.user.email,
            'avatar': request.user.avatar,
            'age': request.user.age,
            'sex': request.user.sex,
            'address': request.user.address,
            'occupation': request.user.occupation,
            'phone': request.user.phone,
            'introduction': request.user.introduction,
        }
        form = forms.UserInfo(default_data)
    return render(request, 'web/index/profile_update.html', locals())


@login_required
def index(request):
    users = User.objects.all().count()
    male = User.objects.filter(sex='male').count()
    female = User.objects.filter(sex='female').count()
    low_score = models.UserDepressionScore.objects.filter(depression_score__lt=60).count()
    return render(request, 'web/index/index.html', locals())


def register(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            models.UserDepressionScore.objects.create(user_id=user)
            return redirect('web:login')
    else:
        form = forms.UserCreationForm()
    return render(request, 'web/login/signup.html', locals())


def login_web(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        models.UserDepressionScore.objects.get_or_create(user_id=user)
                    login(request, user)
                    return redirect('web:index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'web/login/login.html', locals())
    login_form = forms.LoginForm()
    return render(request, 'web/login/login.html', locals())


@login_required
def data_presentation(request):
    if request.method == 'GET':
        score = models.UserDepressionScore.objects.filter(user_id=request.user).values('depression_score', 'grand',
                                                                                       'gradual', 'short', 'point',
                                                                                       'stroop', 'scale')
        scale = models.TestResultScale.objects.filter(user_id=request.user).values('id', 'score').order_by('-date')[:7]
        grand = models.TestResultGrand.objects.filter(user_id=request.user).values('id', 'score').order_by('-date')[:7]
        gradual = models.TestResultGradual.objects.filter(user_id=request.user).values('id', 'score').order_by('-date')[
                  :7]
        point = models.TestResultPoint.objects.filter(user_id=request.user).values('id', 'score').order_by('-date')[:7]
        stroop = models.TestResultStroop.objects.filter(user_id=request.user).values('id', 'score').order_by('-date')[
                 :7]
        short = models.TestResultShort.objects.filter(user_id=request.user).values('id', 'score').order_by('-date')[:7]
        data = {'score': list(score), 'scale': list(scale), 'grand': list(grand), 'gradual': list(gradual),
                'point': list(point), 'stroop': list(stroop), 'short': list(short)}
        return render(request, 'web/index/charts.html', {'score': data})


@login_required
def data_analysis(request):
    if request.method == 'GET':
        imgs = models.TablePicture.objects.all()
    return render(request, 'web/index/TestPic.html', locals())


def get_all_files(dir):
    files_ = []
    list = os.listdir(dir)
    for i in range(0, len(list)):
        path = os.path.join(dir, list[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(path)
    return files_


# from .scaleQues import bk_ques
# # for i in bk_ques.values():
#     # models.TableScale.objects.create(type_scale=1,content=i)
# return JsonResponse({
#     '200':'YES'
# })


@csrf_exempt
def data_process(request):
    if request.user.is_superuser:
        all_imgs = []
        for i in os.listdir(MEDIA_ROOT + '/TestPic/jaffe'):
            os.chdir(MEDIA_ROOT + ('/TestPic/jaffe/%s' % i))
            all_imgs.append(get_all_files(os.getcwd()))
        for i in all_imgs:
            for j in i:
                models.TablePicture.objects.create(name=j.split('/')[-1], picsign='1', emotion=j.split('/')[-2],
                                                   img=j[19:])
        return JsonResponse({'status': '200', 'msg': '数据库上传成功'})
    else:
        return JsonResponse({'status': '403', 'msg': '非管理员无权限'})


from django.views.generic.edit import FormView


class ImageView(FormView):
    form_class = forms.ImageForm
    template_name = 'web/index/TestPic_update.html'
    success_url = 'process/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('img')
        if form.is_valid():
            for f in files:
                models.TablePicture.objects.create(img=f, name=f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
