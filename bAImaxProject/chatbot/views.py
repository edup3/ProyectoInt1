from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request,'home.html')

def chatbot(request):
    return render(request,'chatbot.html')