# Create your views here.
# /fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http.response import HttpResponse
from datetime import datetime
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from fb_qnabot.models import Questions
from fb_qnabot.models import Answers
from django.shortcuts import render
import requests

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAAC0mYf4lo4BAIMH6cRhfenIymo36CdY1TQ2hZB1htaTIFdoYiNQcPsGhwjvPjZBZBaQMWDoVH5d9BpUS7dX22yoZCOiIWb0vvIv9YjqMShMFSv8DsOLkoYOB7itaI8uIblmw1zF8KjrZBgmZA0bJqM1Jh8gHb3wQWmRtTLS0eCQZDZD"
VERIFY_TOKEN = "85888988911"

jokes = { 'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                     """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':      ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                      """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb': ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                  """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] }

# Helper function
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!"

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'Yo '+user_details['first_name']+'..! ' + joke_text

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Helper function
def post_facebook_message_autoreply(fbid, recevied_message):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'Hi '+user_details['first_name']+', thanks for posting question here, our team will reply soon...'

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Helper function
def post_facebook_message_send(fbid, recevied_message):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = recevied_message

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.
class QnABotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # event_entry=json.loads(self.request.body.decode('utf-8'))
        # if event_entry['entry'][0]['messaging'][0]:
        #     messaging_event = event_entry['entry'][0]['messaging'][0]
        #     msg_txt   = messaging_event['message']['text']
        #     sender_id = messaging_event['sender']['id']
        #     pprint(messaging_event)
        #     post_facebook_message(sender_id, msg_txt)
        # return HttpResponse()

        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        # pprint(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    # pprint(message)
                    msg_mid   = message['message']['mid']
                    msg_txt   = message['message']['text']
                    recipient_id = message['recipient']['id']
                    sender_id = message['sender']['id']
                    timestamp = message['timestamp']
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    post_facebook_message_autoreply(message['sender']['id'], message['message']['text'])
                    q = Questions(mid=msg_mid, question=msg_txt, recipient=recipient_id, sender=sender_id, timestamp=timestamp)
                    q.save()
        return HttpResponse()

# Create your views here.

# class QnABotView(generic.View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse("Hello World!")
#     # def get(self, request, *args, **kwargs):
#     #     if self.request.GET['hub.verify_token'] == '85888988911':
#     #         return HttpResponse(self.request.GET['hub.challenge'])
#     #     else:
#     #         return HttpResponse('Error, invalid token')

class QuestionListView(ListView):
    model = Questions
    template_name = 'questions.html'

class QuestionDetailView(DetailView):
    model = Questions
    template_name = 'question_detail.html'
    context_object_name = 'question_detail'

class AnswerCreateView(CreateView):
    model = Answers
    template_name = 'answer_new.html'
    # fields = '__all__'
    fields = ['qid', 'answer']
    success_url = reverse_lazy('questions')

    # def get_context_data(self, **kwargs):
    #     print(kwargs)
    #     return HttpResponse(kwargs)

    def get_initial(self):
        initials = super(AnswerCreateView, self).get_initial()
        initials['qid'] = self.kwargs['qid']
        # return HttpResponse(self.kwargs['qid'])
        return initials

    def form_valid(self, form):
        Qdata = Questions.objects.values_list('sender', flat=True).filter(id=self.kwargs['qid'])
        if Qdata:
            for sender in Qdata:
                # form.instance.answer = self.kwargs['qid']
                # form.instance.answer = Event.objects.get(pk=self.kwargs['qid'])
                # form.instance.answer = 'll'
                form.instance.timestamp = datetime.now()
                post_facebook_message_send(sender, form.instance.answer)
        return super(AnswerCreateView, self).form_valid(form)
