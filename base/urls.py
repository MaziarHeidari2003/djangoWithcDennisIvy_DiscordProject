from django.urls import path
from .views import *

app_name = 'base'
urlpatterns = [
path('',home, name="home"),
path('room/<str:pk>',room,name="room"),
path('profile/<int:pk>/',userProfile,name='user-profile'),
path('create-room',createRoom,name='create-room'),
path('update-room/<int:pk>',updateRoom,name='update-room'),
path('delet-room/<int:pk>',deleteRoom,name='delete-room'),
path('login/',loginPage,name='login'),
path('logout/',logoutUser,name='logout'),
path('register/',registerUser,name='register'),
path('delet-message/<int:pk>',deleteMessage,name='delete-message'),






]