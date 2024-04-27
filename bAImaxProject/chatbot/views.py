from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from . import chatbotback
from chatbot.models import Chat,Message
from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()

# Create your views here.

def home(request):
    if request.user is not None:
        return redirect('chat_page')
    respuesta = chatbotback.answer_message("hola")
    return render(request,'home.html')

def login_(request):
    if request.user is not None:
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
        'chat': room_details
    })

def checkview(request:HttpRequest):
    new_room = Chat.objects.create(user = request.user)
    new_room.save()
    print(new_room)
    print(new_room.user.get_username())
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
    print(chats)
    return render(request,'chat_page.html',{'chats':chats})