from django.db import models
from django.contrib.auth.forms import User
from datetime import datetime

# Create your models here.

class User(models.Model):
  def __str__(self) -> str:
    return f'{self.name} {self.lastname}'
  name = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  adress = models.CharField(max_length=255)
  phone = models.IntegerField()

class MedicalCenter(models.Model):
  name = models.CharField(max_length=255)
  specialty = models.CharField(max_length=255, null=True)
  adress = models.CharField(max_length=255)
  phone = models.IntegerField()
  schedule = models.CharField(max_length=255)

class Specialist(models.Model):
  name = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  specialty = models.CharField(max_length=255)
  phone = models.IntegerField()
  location = models.CharField(max_length=255)
  schedule = models.CharField(max_length=255)
  id_medicalCenter = models.ForeignKey(MedicalCenter, on_delete=models.DO_NOTHING)

class MedicalAppointment(models.Model):
  id_specialist = models.ForeignKey(Specialist, on_delete=models.DO_NOTHING)
  id_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  confirmation = models.CharField(max_length=255)

class Symptom(models.Model):
  description = models.TextField()

class Diagnosis(models.Model):
  diagnosis = models.TextField()
  recomendations = models.TextField()

class Chat(models.Model):
  id_chat = models.IntegerField(primary_key = True)

class Message(models.Model):
  def __str__(self) -> str:
    if self.id_user == None:
      return f'Author: bAImax : {self.content} '
    return f'Author: {self.id_user.name} : {self.content} '
  id_user = models.ForeignKey(User , on_delete=models.DO_NOTHING,blank = True, null = True)
  id_chat = models.ForeignKey(Chat, on_delete = models.DO_NOTHING)
  content = models.TextField()
  time = models.DateTimeField(default = datetime.now) 
