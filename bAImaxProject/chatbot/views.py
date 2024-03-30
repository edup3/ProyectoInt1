from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from . import chatbotback
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    respuesta = chatbotback.answer_message()
    return render(request,'home.html')

def chatbot(request):
    return render(request,'chatbot.html')

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("chatbot")

    context = {'loginform':form}    
    return render(request,'login.html', context=context)

def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        
    context = {'registerform' : form}

    return render(request,'signup.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect("")
