#!/usr/bin/env python
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

category = (
    ("1", "其他测试"),
    ("2", "渐变测试"),
)
gender = (
    ("male", "男"),
    ("female", "女"),
)
location = (
    ('1', '北京市'), ('2', '天津市'), ('3', '河北省'), ('4', '山西省'), ('5', '内蒙古'), ('6', '辽宁省'), ('7', '吉林省'), ('8', '黑龙江省'),
    ('9', '上海市'), ('10', '江苏省'), ('11', '浙江省'), ('12', '安徽省'), ('13', '福建省'), ('14', '江西省'), ('15', '山东省'),
    ('16', '河南省'), ('17', '湖北省'), ('18', '湖南省'), ('19', '广东省'), ('20', '广西自治区'), ('21', '海南省'), ('22', ' 重庆市'),
    ('23', '四川省'), ('24', '贵州省'), ('25', '云南省'), ('26', '西藏自治区'), ('27', '陕西省'), ('28', '甘肃省'), ('29', '青海省'),
    ('30', '宁夏回族自治区'), ('31', '新疆维吾尔自治区'), ('32', '香港特别行政区'), ('33', '澳门特别行政区'), ('34', '台湾省'), ('35', '其它'),
)
types = (
    ('1', '贝克'), ('2', '汉密尔顿'),
    ('3', 'SDS'), ('4', '伯恩斯'),
    ('5', 'GAD-7'), ('6', 'PHQ-9'),
)


class UserTable(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    avatar = models.ImageField(verbose_name="头像", upload_to='avatar', default='avatar/default.jpg')
    nickname = models.CharField(max_length=50, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    sex = models.CharField(max_length=8, choices=gender, blank=True, null=True)
    address = models.CharField(max_length=64, choices=location, null=True, blank=True)
    occupation = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        verbose_name = "user_table"
        verbose_name_plural = verbose_name
        db_table = 'user_table'


# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)

    class Meta:
        verbose_name = "email_table"
        verbose_name_plural = verbose_name
        db_table = 'email_table'


class TableEssay(models.Model):
    essay_name = models.CharField(verbose_name='文章名', max_length=128)
    essay_thumb = models.ImageField(upload_to='essay_thumb/%Y/%m')
    essay_content = models.URLField(verbose_name="科普文章")

    class Meta:
        verbose_name = "table_essay"
        verbose_name_plural = verbose_name
        db_table = 'table_essay'


class TableVideo(models.Model):
    video_name = models.CharField(max_length=128, verbose_name='视频名')
    video_thumb = models.ImageField(upload_to='video_thumb/%Y/%m')
    video = models.URLField(verbose_name="视频")

    class Meta:
        verbose_name = "table_video"
        verbose_name_plural = verbose_name
        db_table = 'table_video'


class TablePicture(models.Model):
    """
    Picsign 图片标识用来标注图片用于哪个测试类别，渐变测试为 2 其余为 1，不同类型的图片其标注的内容不同。Parameter 表示 6 种情绪强度的参数。
    """
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    picsign = models.CharField(max_length=10, choices=category, blank=True, null=True)
    emotion = models.CharField(max_length=100, blank=True, null=True)
    parameter = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to='TestPic/%Y/%m')

    class Meta:
        verbose_name = "table_picture"
        verbose_name_plural = verbose_name
        db_table = 'table_picture'


class TableScale(models.Model):
    """
    option_score 选项的占比和分数
    """
    content = models.CharField(max_length=500, blank=True, null=True)
    type_scale = models.CharField(max_length=10, blank=True, null=True, choices=types, default='1')
    option_score = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "table_scale"
        verbose_name_plural = verbose_name
        db_table = 'table_scale'


class TestResultScale(models.Model):
    """
    user_option每组用 |表示
    """
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    reaction_time = models.CharField(max_length=500, blank=True, null=True)
    user_option = models.CharField(max_length=500, blank=True, null=True)
    questions = models.CharField(max_length=500, blank=True, null=True)
    type_scale = models.CharField(max_length=10, blank=True, null=True, choices=types, default='1')
    score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "test_result_scale"
        verbose_name_plural = verbose_name
        db_table = 'test_result_scale'


class TestResultGradual(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    option = models.CharField(max_length=500, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    reaction_time = models.CharField(max_length=500, blank=True, null=True)
    user_option = models.CharField(max_length=500, blank=True, null=True)
    right_option = models.CharField(max_length=500, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    d_value = models.PositiveIntegerField(verbose_name="差值", blank=True, null=True)

    class Meta:
        verbose_name = "test_result_gradual"
        verbose_name_plural = verbose_name
        db_table = 'test_result_gradual'


class TestResultPoint(models.Model):
    """
    picture，reaction_time每组用 |表示，以 ,分割
    target是目标图片的 id
    Coordinate是三张图片的坐标即最后按钮位置坐标，对应上面的图片信息顺序，用 ;表示，以 |分割，以，细分
    """
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.CharField(max_length=500, blank=True, null=True)
    reaction_time = models.CharField(max_length=500, blank=True, null=True)
    target = models.CharField(max_length=500, blank=True, null=True)
    coordinate = models.CharField(max_length=500, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "test_result_point"
        verbose_name_plural = verbose_name
        db_table = 'test_result_point'


class TestResultShort(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    option = models.CharField(max_length=100, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    reaction_time = models.CharField(max_length=500, blank=True, null=True)
    user_option = models.CharField(max_length=500, blank=True, null=True)
    right_option = models.CharField(max_length=500, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "test_result_short"
        verbose_name_plural = verbose_name
        db_table = 'test_result_short'


class TestResultGrand(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    option = models.CharField(max_length=255, blank=True, null=True)
    picture = models.CharField(max_length=100, blank=True, null=True)
    reaction_time = models.CharField(max_length=500, blank=True, null=True)
    user_option = models.CharField(max_length=500, blank=True, null=True)
    right_option = models.CharField(max_length=100, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "test_result_grand"
        verbose_name_plural = verbose_name
        db_table = 'test_result_grand'


class TestResultStroop(models.Model):
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.CharField(max_length=500, blank=True, null=True)
    reaction_time = models.CharField(max_length=500, blank=True, null=True)
    interfere_word = models.CharField(max_length=500, blank=True, null=True)
    user_option = models.CharField(max_length=500, blank=True, null=True)
    right_option = models.CharField(max_length=500, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "test_result_stroop"
        verbose_name_plural = verbose_name
        db_table = 'test_result_stroop'


class UserDepressionScore(models.Model):
    """
    此表中每项成绩为该用户所有该项成绩的加权处理，情绪分数为每项成绩的加权处理
    """
    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grand = models.FloatField(blank=True, null=True, default=0)
    gradual = models.FloatField(blank=True, null=True, default=0)
    short = models.FloatField(blank=True, null=True, default=0)
    point = models.FloatField(blank=True, null=True, default=0)
    stroop = models.FloatField(blank=True, null=True, default=0)
    scale = models.FloatField(blank=True, null=True, default=0)
    update = models.DateTimeField(auto_now=True)
    weight = models.CharField(max_length=100, blank=True, null=True, default='1|1|1|1|1|1')
    depression_score = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        verbose_name = "user_depression_score"
        verbose_name_plural = verbose_name
        db_table = 'user_depression_score'
