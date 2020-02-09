# Generated by Django 3.0.2 on 2020-02-08 08:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('avatar', models.ImageField(default='avatar/default.jpg', upload_to='avatar', verbose_name='头像')),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.CharField(blank=True, max_length=10, null=True)),
                ('sex', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], max_length=8, null=True)),
                ('address', models.CharField(blank=True, choices=[('1', '北京市'), ('2', '天津市'), ('3', '河北省'), ('4', '山西省'), ('5', '内蒙古'), ('6', '辽宁省'), ('7', '吉林省'), ('8', '黑龙江省'), ('9', '上海市'), ('10', '江苏省'), ('11', '浙江省'), ('12', '安徽省'), ('13', '福建省'), ('14', '江西省'), ('15', '山东省'), ('16', '河南省'), ('17', '湖北省'), ('18', '湖南省'), ('19', '广东省'), ('20', '广西自治区'), ('21', '海南省'), ('22', ' 重庆市'), ('23', '四川省'), ('24', '贵州省'), ('25', '云南省'), ('26', '西藏自治区'), ('27', '陕西省'), ('28', '甘肃省'), ('29', '青海省'), ('30', '宁夏回族自治区'), ('31', '新疆维吾尔自治区'), ('32', '香港特别行政区'), ('33', '澳门特别行政区'), ('34', '台湾省'), ('35', '其它')], max_length=64, null=True)),
                ('occupation', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user_table',
                'verbose_name_plural': 'user_table',
                'db_table': 'user_table',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EmailVerifyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': 'email_table',
                'verbose_name_plural': 'email_table',
                'db_table': 'email_table',
            },
        ),
        migrations.CreateModel(
            name='TableEssay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('essay_name', models.CharField(max_length=128, verbose_name='文章名')),
                ('essay_thumb', models.ImageField(upload_to='essay_thumb/%Y/%m')),
                ('essay_content', models.URLField(verbose_name='科普文章')),
            ],
            options={
                'verbose_name': 'table_essay',
                'verbose_name_plural': 'table_essay',
                'db_table': 'table_essay',
            },
        ),
        migrations.CreateModel(
            name='TablePicture',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('picsign', models.CharField(blank=True, choices=[('1', '其他测试'), ('2', '渐变测试')], max_length=10, null=True)),
                ('emotion', models.CharField(blank=True, max_length=100, null=True)),
                ('parameter', models.CharField(blank=True, max_length=100, null=True)),
                ('img', models.ImageField(upload_to='TestPic/%Y/%m')),
            ],
            options={
                'verbose_name': 'table_picture',
                'verbose_name_plural': 'table_picture',
                'db_table': 'table_picture',
            },
        ),
        migrations.CreateModel(
            name='TableScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('type_scale', models.CharField(blank=True, choices=[('1', '贝克'), ('2', '汉密尔顿'), ('3', 'SDS'), ('4', '伯恩斯'), ('5', 'GAD-7'), ('6', 'PHQ-9')], default='1', max_length=10, null=True)),
                ('option_score', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'table_scale',
                'verbose_name_plural': 'table_scale',
                'db_table': 'table_scale',
            },
        ),
        migrations.CreateModel(
            name='TableVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=128, verbose_name='视频名')),
                ('video_thumb', models.ImageField(upload_to='video_thumb/%Y/%m')),
                ('video', models.URLField(verbose_name='视频')),
            ],
            options={
                'verbose_name': 'table_video',
                'verbose_name_plural': 'table_video',
                'db_table': 'table_video',
            },
        ),
        migrations.CreateModel(
            name='UserDepressionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grand', models.FloatField(blank=True, default=0, null=True)),
                ('gradual', models.FloatField(blank=True, default=0, null=True)),
                ('short', models.FloatField(blank=True, default=0, null=True)),
                ('point', models.FloatField(blank=True, default=0, null=True)),
                ('stroop', models.FloatField(blank=True, default=0, null=True)),
                ('scale', models.FloatField(blank=True, default=0, null=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('weight', models.CharField(blank=True, default='1|1|1|1|1|1', max_length=100, null=True)),
                ('depression_score', models.FloatField(blank=True, default=0, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user_depression_score',
                'verbose_name_plural': 'user_depression_score',
                'db_table': 'user_depression_score',
            },
        ),
        migrations.CreateModel(
            name='TestResultStroop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('picture', models.CharField(blank=True, max_length=500, null=True)),
                ('reaction_time', models.CharField(blank=True, max_length=500, null=True)),
                ('interfere_word', models.CharField(blank=True, max_length=500, null=True)),
                ('user_option', models.CharField(blank=True, max_length=500, null=True)),
                ('right_option', models.CharField(blank=True, max_length=500, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test_result_stroop',
                'verbose_name_plural': 'test_result_stroop',
                'db_table': 'test_result_stroop',
            },
        ),
        migrations.CreateModel(
            name='TestResultShort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('option', models.CharField(blank=True, max_length=100, null=True)),
                ('picture', models.CharField(blank=True, max_length=100, null=True)),
                ('reaction_time', models.CharField(blank=True, max_length=500, null=True)),
                ('user_option', models.CharField(blank=True, max_length=500, null=True)),
                ('right_option', models.CharField(blank=True, max_length=500, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test_result_short',
                'verbose_name_plural': 'test_result_short',
                'db_table': 'test_result_short',
            },
        ),
        migrations.CreateModel(
            name='TestResultScale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reaction_time', models.CharField(blank=True, max_length=500, null=True)),
                ('user_option', models.CharField(blank=True, max_length=500, null=True)),
                ('questions', models.CharField(blank=True, max_length=500, null=True)),
                ('type_scale', models.CharField(blank=True, choices=[('1', '贝克'), ('2', '汉密尔顿'), ('3', 'SDS'), ('4', '伯恩斯'), ('5', 'GAD-7'), ('6', 'PHQ-9')], default='1', max_length=10, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test_result_scale',
                'verbose_name_plural': 'test_result_scale',
                'db_table': 'test_result_scale',
            },
        ),
        migrations.CreateModel(
            name='TestResultPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('picture', models.CharField(blank=True, max_length=500, null=True)),
                ('reaction_time', models.CharField(blank=True, max_length=500, null=True)),
                ('target', models.CharField(blank=True, max_length=500, null=True)),
                ('coordinate', models.CharField(blank=True, max_length=500, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test_result_point',
                'verbose_name_plural': 'test_result_point',
                'db_table': 'test_result_point',
            },
        ),
        migrations.CreateModel(
            name='TestResultGrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('option', models.CharField(blank=True, max_length=255, null=True)),
                ('picture', models.CharField(blank=True, max_length=100, null=True)),
                ('reaction_time', models.CharField(blank=True, max_length=500, null=True)),
                ('user_option', models.CharField(blank=True, max_length=500, null=True)),
                ('right_option', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test_result_grand',
                'verbose_name_plural': 'test_result_grand',
                'db_table': 'test_result_grand',
            },
        ),
        migrations.CreateModel(
            name='TestResultGradual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('option', models.CharField(blank=True, max_length=500, null=True)),
                ('picture', models.CharField(blank=True, max_length=100, null=True)),
                ('reaction_time', models.CharField(blank=True, max_length=500, null=True)),
                ('user_option', models.CharField(blank=True, max_length=500, null=True)),
                ('right_option', models.CharField(blank=True, max_length=500, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('d_value', models.PositiveIntegerField(blank=True, null=True, verbose_name='差值')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'test_result_gradual',
                'verbose_name_plural': 'test_result_gradual',
                'db_table': 'test_result_gradual',
            },
        ),
    ]
