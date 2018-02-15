# fb_qnabot/urls.py
from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from . import views
from .views import QnABotView
# from fb_qnabot.views import AnswerCreateView

urlpatterns = [
    path('questions/', views.QuestionListView.as_view(), name='questions'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^answer/new/(?P<qid>\d+)/$', views.AnswerCreateView.as_view(), name='answer_new'),
    url(r'^c314fa24d1f9a96b1c0bec596be66450894ffae0d017ac09dd/?$', QnABotView.as_view(), name='fb_random') # Mritunjay
]
