from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from . import chatbotback
from chatbot.models import Chat,Message
from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
import os
from dotenv import load_dotenv

User = get_user_model()

# Create your views here.

def home(request:HttpRequest):
    navbar = 'base.html'
    if request.user.is_authenticated:
        navbar = 'base3.html'
    return render(request,'home.html',{'navbar':navbar})

def login_(request:HttpRequest):
    if request.user.is_authenticated :
        return redirect('chat_page')
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat_page')

    context = {'loginform':form}    
    return render(request,'login.html', context=context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('chat_page')
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        
    context = {'registerform' : form}

    return render(request,'signup.html', context=context)

def logout_(request):
    logout(request)
    return redirect("/")


@login_required(login_url='/login')
def chatbot(request, room):
    username = request.GET.get('username')
    room_details = Chat.objects.get(id_chat=room)
    return render(request, 'chatbot.html', {
        'username': username,
        'room': room,
        'chat': room_details })

def checkview(request:HttpRequest):
    new_room = Chat.objects.create(user = request.user)
    return redirect('chat_page')

def send(request:HttpRequest):
    message = request.POST['message']
    room_id = request.POST['chat_id']
    user = User.objects.get(id=request.user.id)
    chatid = Chat.objects.get(id_chat = room_id)

    new_message = Message.objects.create(content=message, user = user, chat=chatid)
    new_message.save()

    new_message = Message.objects.create(content=chatbotback.answer_message(message), user = None, chat=chatid)
    new_message.save()


    return HttpResponse('Message sent successfully')

def getMessages(request, chatid):
    room_details = Chat.objects.get(id_chat=chatid)
    messages = Message.objects.filter(chat=room_details)
    return JsonResponse({"messages":list(messages.values('user__username','content','time').order_by('time'))[::-1]})

@login_required(login_url='/login')
def chat_page(request:HttpRequest):
    chats = Chat.objects.filter(user = request.user)
    chatsfirstmessage = []
    for chat in chats:
        firstmessage = Message.objects.filter(chat=chat).order_by('time')
        if firstmessage:
            chatsfirstmessage.append({'chat':chat,'message':firstmessage[0]})
        else:
            chatsfirstmessage.append({'chat':chat,'message':{'content':'Nuevo Chat'}})
    for chat in chatsfirstmessage:
        print(chat)
    return render(request,'chat_page.html',{'chats':chatsfirstmessage})

def emergency(request:HttpRequest):
    try:
        _ = load_dotenv('twilio.env')
        account_sid = os.environ.get('accSid')
        auth_token = os.environ.get('authToken')

        client = Client(account_sid, auth_token)

        call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+573053036284",
        from_="+15515537366"
        )

        return HttpResponse("Calling emergency services")
    except:
        _ = load_dotenv('twilio2.env')
        account_sid = os.environ.get('accSid2')
        auth_token = os.environ.get('authToken2')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='+12075604809',
        body=f"{request.user.username} is calling emergency services",
        to='+573053036284'
        )
        return HttpResponse("Messaging emergency contact")




