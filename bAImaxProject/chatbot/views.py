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
    respuesta = chatbotback.answer_message("hola")
    return render(request,'home.html')

def login_(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            idConversation = 1
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(f"/chatbot/{idConversation}")

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
    room = request.POST['chat_id']
    

    if Chat.objects.filter(id_chat=room).exists():
        return redirect('chatbot/'+room+'/?username='+request.user.get_username())
    else:
        new_room = Chat.objects.create(id_chat=room)
        new_room.save()
        return redirect('chatbot/'+room+'/?username='+request.user.get_username())

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
