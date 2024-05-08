import numpy as np
from openai import OpenAI

import os


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv('openAI.env')

client = OpenAI(
    api_key=os.environ.get('openAI_api_key'),
)

#Funcion de respuesta
def response(texto):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are bAimax, a health assistant who is there to kindly answer questions regarding health, receive symptoms and respond with diagnoses if possible."},
    {"role": "user", "content": texto}
  ])
    #Devuelve el contenido de la respuesta
    return completion.choices[0].message.content  
         




def answer_message(texto):

    return response(texto)
