from django.shortcuts import render

# Create your views here.
# /fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
class QnABotView(generic.View):
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Hello World!")
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '8588898891':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
