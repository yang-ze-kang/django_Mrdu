#!/usr/bin/env python
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth.admin import UserAdmin
from . import forms

"""
测试后台
"""


class GradualAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'score', 'date')


admin.site.register(TestResultGradual, GradualAdmin)


class StroopAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'score', 'date')


admin.site.register(TestResultStroop, StroopAdmin)


class ShortAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'score', 'date')


admin.site.register(TestResultShort, ShortAdmin)


class PointAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'score', 'date')


admin.site.register(TestResultPoint, PointAdmin)


class ScaleAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'score', 'type_scale', 'date')


admin.site.register(TestResultScale, ScaleAdmin)


class GrandAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'score', 'date')


admin.site.register(TestResultGrand, GrandAdmin)

"""
其他后台
"""


class EmailAdmin(admin.ModelAdmin):
    list_display = (  'email','code', 'send_type', 'send_time')


admin.site.register(EmailVerifyRecord, EmailAdmin)


class TableScaleAdmin(admin.ModelAdmin):
    list_display = ('content', 'type_scale', 'option_score')


admin.site.register(TableScale, TableScaleAdmin)


class TableEssayAdmin(admin.ModelAdmin):
    list_display = ('essay_content', 'essay_name', 'essay_thumb')


admin.site.register(TableEssay, TableEssayAdmin)


class TableVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'video_name', 'video_thumb')


admin.site.register(TableVideo, TableVideoAdmin)


class UserDepressionScoreAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'depression_score', 'update')


admin.site.register(UserDepressionScore, UserDepressionScoreAdmin)


class TablePictureAdmin(admin.ModelAdmin):
    list_display = ['pid', 'name', 'picsign', 'emotion', 'parameter', 'img']


admin.site.register(TablePicture, TablePictureAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'phone')
    add_form = forms.UserCreationForm  # 添加用户表单，使用自定义的表单
    form = forms.ProfileForm  # 编辑用户表单，使用自定义的表单
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {'fields': ('avatar', 'nickname', 'email', 'age', 'sex', 'address', 'occupation', 'phone',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'), }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password')}
         ),
    )


admin.site.register(UserTable, CustomUserAdmin)

admin.site.unregister(Group)

admin.site.site_header = "APP后台"
admin.site.site_title = "APP登录系统"
