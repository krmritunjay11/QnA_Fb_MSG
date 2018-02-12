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
    url(r'^3fe31f84b0ea9e1bdc93868d9167293671a4537c43e848db14/?$', QnABotView.as_view(), name='fb_random') # Mritunjay
]
