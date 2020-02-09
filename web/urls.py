#!/usr/bin/env python
from django.urls import path, include
from . import views

app_name = "web"

urlpatterns = [
    path('register/', views.register, name='signup'),
    path('login/', views.login_web, name="login"),
    path('index/', views.index, name='index'),
    path('myprofile/', views.profile_web, name='profile'),
    path('my_profile/update/', views.profile_update, name='profile_update'),
    path('logout/', views.login_web, name='logout'),
    path('presentation/', views.data_presentation, name="presentation"),
    path('analysis/', views.data_analysis, name="analysis"),
    path('process/', views.data_process, name="process"),
    path('imgs_update/', views.ImageView.as_view(), name='imgs_update'),

    path('table/score/', views.table_score, name='table'),
    path('table/grand/', views.page_grand, name='grand'),
    path('table/timeRange/', views.timeRange, name='timeRange'),
    path('table/gradual/', views.page_gradual, name='gradual'),
    path('table/scale/',views.page_scale,name='scale'),
    path('table/short/',views.page_short,name='short'),
    path('table/point/',views.page_point,name='point'),
    path('table/stroop/',views.page_stroop,name='stroop'),
]
