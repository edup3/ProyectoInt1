import chatbot as chatbot
from chatbot import models
from chatbot.models import MedicalCenter
from django.core.management.base import BaseCommand
import os
import numpy as np
from openai import OpenAI


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv('openAI.env')
client = OpenAI(

    api_key=os.environ.get('openAI_api_key'),
)

def responseDiagnosis(texto):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You provide a very short diagnosis based on the symtoms of the message"},
    {"role": "user", "content": texto}
  ])
    #Devuelve el contenido de la respuesta
    return completion.choices[0].message.content  
         
#Sugerir centro medico basandonos en su especialidad. Los emb de los medical centers estan basados en el campo speciality
#Se migrara el comando a forma de script para su posterior uso de forma normal. 

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        help = 'Modify path of images'

        promp="i have a headache"

        
        print(responseDiagnosis(promp))

        self.stdout.write(self.style.SUCCESS(f'Diagnostico realizado de forma exitosa!')) 