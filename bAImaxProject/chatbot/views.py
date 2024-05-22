from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpRequest
from . import chatbotback
from chatbot.models import Chat,Message,MedicalCenter
from . forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
import os
from dotenv import load_dotenv

import numpy as np
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
User = get_user_model()
import os

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



## Seccion de Tools
tools=[ 
            
            {
            "type": "function",
            "function": {
                "name": "getMedicalCenter",
                "description": "obtains the appropriate medical center for the medical diagnosis,It is used to suggest medical centers to the user or if the user asks for one",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "promp": { "type": "string", "description": "The diagnosis and symtops, e.g. Bone fracture and back pain", }
                    },
                    "required": ["promp"],
                },
            },
        } 
        
        ]

### Aqui se carga la Key de openAI

_ = load_dotenv('openAI.env')
client = OpenAI(

    api_key=os.environ.get('openAI_api_key'),
)


def get_embedding(text, model="text-embedding-3-small"):
   print(text)
   print(text)
   print(text)
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))







### Esta funcion toma un prompt y a partir de este devuelve el nombre del centro medico mas apropiado de acuerdo a la espcialidad
def getMedicalCenter(promp):
    embpromp=get_embedding(promp)
        
    centros_medicos=MedicalCenter.objects.all()
    lista=[]
    for centro in centros_medicos:
        item=centro.emb
        item=list(np.frombuffer(item))
        lista.append(cosine_similarity(item,embpromp))

    lista = np.array(lista)
    idx = np.argmax(lista)
    idx = int(idx)

    return json.dumps({"center":centros_medicos[idx].name})
##-------------------------------------------------------------------------------

# Envio y respuesta de mensaje 

def send(request:HttpRequest):
    message = request.POST['message']
    room_id = request.POST['chat_id']
    user = User.objects.get(id=request.user.id)
    chatid = Chat.objects.get(id_chat = room_id)

    new_message = Message.objects.create(content=message, user = user, chat=chatid)
    new_message.save()



# Seccion muy pero muy especial para la recoleccion del historial
#/////////////
    msglimit=20 # Limite de mensajes que recoge el modelo de lenguaje dentro del chat.

    messages = Message.objects.filter(chat=room_id) #Filtro de mensajes por room id
    x=list(messages)        #Lista de todos los mensajes de la respectiva room id
    x=x[-msglimit:]         #Lista ajustada al limite de mensajes
    
    # Aqui se carga el historia, incialmente era un QuerySet pero al ser convertido a lista se le pueden agregar campos.
    historial=[
    {"role": "system", "content": "You are bAimax, a health assistant who is there to kindly answer questions regarding health, receive symptoms and respond with diagnoses if possible. Don't give too long aswers, try to keep it direct and short"},
    ]
    for i in x:
        if i.user==None:
            autor="assistant"
        else:
            autor="user"
        historial.append({ "role": autor, "content": i.content })
#///////////
#Finaliza seccion


#Creacion del mensaje de respuesta

    #response_message=chatbotback.answer_message(message,historial,tools)

    client = OpenAI(
    api_key=os.environ.get('openAI_api_key'),
    )

    #Aqui se inicializa el mensaje, el cual recibe el historial y crea una respuesta inicial.
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=historial,
        tools=tools,
        tool_choice="auto", )
    #Devuelve el contenido de la respuesta
    z= completion.choices[0].message
    #Aqui se elige la respuesta guardada en la variable Z
    response_message=z
    z=completion.choices[0].message.content 
    tool_calls = response_message.tool_calls
    # Si existe una llamada a las herramientas, es decir, si se requiere una funcion de tools, se inicia el proceso para ejectural.
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "getMedicalCenter": getMedicalCenter,
        }  # Aqui van las funciones
        historial.append(response_message)  # extend conversation with assistant's reply
        # Aqui se envia la informacion a la funcion
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print(function_args)
            print(function_args)
            print(function_args)
            print(function_args)    #Esto era solo para checar los argumentos
            function_response = function_to_call(
                promp=function_args.get("promp"),
            )
            # En el historial de mensajes creado por el codigo (No confundir con el historial de la base de datos) se agrega cual fue la respuesta de la funcion.
            historial.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # Se repite la conversacion con esta nueva informacion
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=historial,
        )  

        #Respuesta final
        response_message=second_response.choices[0].message.content
        z=response_message

    contenidofinal=z
        
   
    






    #----------------------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------------------
    new_message = Message.objects.create(content=contenidofinal, user = None, chat=chatid)
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




