#!/usr/bin/env python
from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('login/', views.login_view),
    path('signup/', views.signup, name="signup"),
    path('email/', views.SendEmail, ),
    path('app_media/', views.app_media),
    path('score/<int:pk>/<str:score_type>/', views.score),
    path('test/', views.test_api),
    path('result/', views.result_api),
    path('profile/', views.profile),
]
