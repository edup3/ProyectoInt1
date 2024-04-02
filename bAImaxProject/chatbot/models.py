from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  adress = models.CharField(max_length=255)
  phone = models.IntegerField()

class MedicalCenter(models.Model):
  name = models.CharField(max_length=255)
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

class Symptoms(models.Model):
  description = models.TextField()

class Diagnosis(models.Model):
  diagnosis = models.TextField()
  recomendations = models.TextField()


class Feedback(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.nombre}"