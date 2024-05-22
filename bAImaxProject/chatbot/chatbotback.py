import numpy as np
from openai import OpenAI

import os


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv('openAI.env')

client = OpenAI(
    api_key="openAI.env",
)

#Funcion de respuesta
def response(texto,contexto,tools):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=contexto,
    tools=tools,
    tool_choice="auto", )
    #Devuelve el contenido de la respuesta
    x= completion.choices[0].message.content


    



    if x==None:
        return "Esta vacio tu mensaje"  
    else:
        return x




def answer_message(texto,contexto,tools):

    return response(texto,contexto,tools)
