from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  adress = models.CharField(max_length=255)
  phone = models.IntegerField()

class MedicalAppointment(models.Model):
  id_specialist = models.IntegerField()
  id_user = models.IntegerField()
  confirmation = models.CharField(max_length=255)

class Symptoms(models.Model):
  description = models.TextField()

class Diagnosis(models.Model):
  diagnosis = models.TextField()
  recomendations = models.TextField()

class Specialist(models.Model):
  name = models.CharField(max_length=255)
  specialty = models.CharField(max_length=255)
  phone = models.IntegerField()
  location = models.CharField(max_length=255)
  schedule = models.CharField(max_length=255)
  id_medicalCenter = models.CharField(max_length=255)

class MedicalCenter(models.Model):
  name = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  adress = models.CharField(max_length=255)
  phone = models.IntegerField()
  schedule = models.CharField(max_length=255)