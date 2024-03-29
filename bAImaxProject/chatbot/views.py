from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse
from . import chatbotback
from chatbot.models import Chat,Message,User
# Create your views here.

def home(request):
    respuesta = chatbotback.answer_message()
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')
    
def chatbot(request, room):
    username = request.GET.get('username')
    room_details = Chat.objects.get(id_chat=room)
    return render(request, 'chatbot.html', {
        'username': username,
        'room': room,
        'chat': room_details
    })

def checkview(request):
    room = request.POST['chat_id']
    username = request.POST['username']

    if Chat.objects.filter(id_chat=room).exists():
        return redirect('chatbot/'+room+'/?username='+username)
    else:
        new_room = Chat.objects.create(id_chat=room)
        new_room.save()
        return redirect('chatbot/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['chat_id']
    user = User.objects.get(name=username)
    chati = Chat.objects.get(id_chat = room_id)

    new_message = Message.objects.create(content=message, id_user = user, id_chat=chati)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, chatid):
    room_details = Chat.objects.get(id_chat=chatid)
    messages = Message.objects.filter(id_chat=room_details)
    return JsonResponse({"messages":list(messages.values('id_user__name','content','time'))})