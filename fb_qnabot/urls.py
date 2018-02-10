# fb_qnabot/urls.py
from django.conf.urls import url, include
from django.contrib import admin
from .views import QnABotView

urlpatterns = [
    url(r'^d94ce56ad36fc0bcc902706e06aa445340023a194be489e1e9/?$', QnABotView.as_view(), name='fb_random') # Mritunjay
]
