import chatbot as chatbot
from chatbot import models
from chatbot.models import Specialist
from django.core.management.base import BaseCommand
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv('openAI.env')
client = OpenAI(

    api_key=os.environ.get('openAI_api_key'),
)

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class Command(BaseCommand):
    help='Comando para asignar los embeddings a los medical centers'
    def handle(self, *args, **kwargs):
        help = 'Modify path of images'
        Specialistlist=Specialist.objects.all()
        for specialist in Specialistlist:
            item=get_embedding(Specialist.embspecialist)
            Specialist.embspecialist=np.array(item).tobytes()
            specialist.save()
        self.stdout.write(self.style.SUCCESS(f'Se actualizaron los embeddings')) 