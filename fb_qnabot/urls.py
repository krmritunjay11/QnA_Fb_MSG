# fb_qnabot/urls.py
from django.conf.urls import url, include
from django.contrib import admin
from .views import QnABotView

urlpatterns = [
    url(r'^7cc599762b5f68f04acd104241513b333838150e5294fe0d82/?$', QnABotView.as_view(), name='fb_random') # Mritunjay
]
