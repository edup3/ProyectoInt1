from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from . import chatbotback
# Create your views here.

def home(request):
    respuesta = chatbotback.answer_message()
    return render(request,'home.html')

def chatbot(request):
    respuesta = chatbotback.answer_message()
    context = {}
    if request.method == 'POST':
        context['mensaje'] = request.POST.get('message')
    return render(request,'chatbot.html',context)

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')
    
