from django.urls import path
from . import views


from .views import feedback

urlpatterns = [
    path('feedback/', feedback, name='feedback'),
]