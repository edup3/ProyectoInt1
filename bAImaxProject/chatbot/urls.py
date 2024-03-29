from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/<int:room>/',views.chatbot,name='chatbot'),
    path('checkview',views.checkview,name='checkview'),
    path('login/', views.login),
    path('signup/',views.signup),
    path('send', views.send, name='send'),
    path('getMessages/<int:chatid>/', views.getMessages, name='getMessages'),
]