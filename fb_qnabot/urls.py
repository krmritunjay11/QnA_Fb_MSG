# fb_qnabot/urls.py
from django.conf.urls import url, include
from django.contrib import admin
from .views import QnABotView

urlpatterns = [
    url(r'^3fe31f84b0ea9e1bdc93868d9167293671a4537c43e848db14/?$', QnABotView.as_view(), name='fb_random') # Mritunjay
]
