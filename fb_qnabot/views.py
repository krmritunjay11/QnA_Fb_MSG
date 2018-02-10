from django.shortcuts import render

# Create your views here.
# /fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
class QnABotView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello World!")
