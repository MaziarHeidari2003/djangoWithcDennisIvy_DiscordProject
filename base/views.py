from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from django.db.models import Q
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm

def logoutUser(request):
  logout(request)
  return redirect('base:home')  # im curious to see the url for this veiw




def registerUser(request):
  form = UserCreationForm()

  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user=form.save(commit=False)
      user.username=user.username.lower() # this is the way to clean the input data which is validated before saving it to the datebase
      user.save()
      login(request,user)
      return redirect('base:home')
    else:
      messages.error(request,'An error occured during registration')
  return render(request,'base/login_register.html',{
    'form':form
  })



def loginPage(request):
  if request.user.is_authenticated:  # nice syntax to avoid the user from logging in twice
    return redirect('base:home')
  
  page= 'login'
  form = UserForm()
  if request.method == 'POST':
    username=request.POST.get('username').lower()
    password=request.POST.get('password')

    try:
      user = User.objects.get(username=username) # why should i have this tyr and except block? why dont i just move to authenticate
    except:
      messages.error(request, "Username not found.") 


      # handling custom user models, security,more accurate error messages

    user = authenticate(request,username=username,password=password)
    if user:
      login(request,user)
      return redirect('base:home')
    else:
       messages.error(request, "Username or password does not exit.") 

       """
        Django's authenticate function, used in user = authenticate(request,username=username,password=password), also raises a User.DoesNotExist exception if the user doesn't exist. However, relying on this exception alone doesn't provide a clear error message for the user. By using the try-except block to check for the user's existence first, you can provide a more accurate error message like "Username not found" instead of "Username or password does not exist."
       """

  return render(request,'base/login_register.html',{
    'page':page,
    'form':form
  })

def home(request):
  q=request.GET.get('q') if request.GET.get('q') != None else '' #nice syntax
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)) #nice syntax to reach the second layer
  topics=Topic.objects.all()
  room_count= rooms.count()
  room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))# this is for the third fraction in the home

  return render(request,'base/home.html',{
    'room_messages':room_messages,
    'rooms':rooms,
    'topics':topics,
    'room_count':room_count
  })
"""

This behavior allows you to organize your templates into smaller, reusable components without having to make significant changes to your views. As long as the context variables needed by the included template are provided by the view, the included template will have access to the necessary data.
Your view function continues to work as expected because it is still rendering the main template. The view function doesn't need to know about the included templates, as the main template will take care of including the additional content.
"""

def room(request,pk):
  room = Room.objects.get(id=pk)
  room_messages = room.message_set.all().order_by('-created')
  participants = room.participants.all()

  if request.method=='POST':   # this kind of form handling is somehow new and wierd and simple
    message=Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')
    )
    room.participants.add(request.user)
    return redirect('base:room',pk=room.id) # we could just not do it but this is a post request and it was gonna mess somethings m so ...

  return render(request, 'base/room.html',{
    'room':room,
    'room_messages':room_messages,
    'participants':participants
  })











@login_required(login_url='/login') # new syntax to make sure where the user is going to be 
def createRoom(request):
  form = RoomForm()
  topics=Topic.objects.all()
  if request.method == 'POST':
      topic_name=request.POST.get('topic')
      topic, created = Topic.objects.get_or_create(name=topic_name)
      Room.objects.create(
        host=request.user,
        topic=topic,
        name=request.POST.get('name'),
        description=request.POST.get('description')
      )
    #form = RoomForm(request.POST)
    #if form.is_valid():
      #room=form.save(commit=False)
      #room.host=request.user
      #room.save()
      return redirect('base:home')     # nice usage of redirect
  return render(request,'base/room_form.html',{
    'form':form,
    'topics':topics
  })

@login_required(login_url='/login') # new syntax to make sure where the user is going to be 
def updateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  topics = Topic.objects.all()
  # if a user who is not the host, he is not alloewd to update the room

  if request.user != room.host:
    return HttpResponse('You are not allowed to do it')

  if request.method == 'POST':
    topic_name=request.POST.get('topic')
    topic,created=Topic.objects.get_or_create(name=topic_name) # this is wild !!
    form=RoomForm(request.POST,instance=room)
    room.topic=topic
    room.description = request.POST.get('description')
    room.name = request.POST.get('name')
    room.save()
    return redirect("base:home")

  return render(request, 'base/room_form.html',{
    'form':form,
    'topics':topics,
    'room':room
  })


@login_required(login_url='/login') 
def deleteRoom(request,pk):
  room = Room.objects.get(id=pk)

  # if a user who is not the host, he is not alloewd to delete the room

  if request.user != room.host:
    return HttpResponse('You are not allowed to do it')

  if request.method == 'POST':
    room.delete()
    return redirect('base:home')
  return render(request,'base/delete.html',{
    'obj':room
  })






@login_required(login_url='/login') 
def deleteMessage(request,pk):
  message = Message.objects.get(id=pk)

  # if a user who is not the host, he is not alloewd to delete the room

  if request.user != message.user:
    return HttpResponse('You are not allowed to do it')

  if request.method == 'POST':
    message.delete()
    return redirect('base:home')
  return render(request,'base/delete.html',{
    'obj':message
  })



def userProfile(request,pk):
  user= User.objects.get(id=pk)
  rooms = user.room_set.all() # all the rooms which have a foreign key to the user
  room_messages = user.message_set.all() 
  topics = Topic.objects.all()
  return render(request,'base/profile.html',{
    'user':user,
    'rooms':rooms,
    'topics':topics,
    'room_messages':room_messages

  })# im goinh to use include tags wich i have used before, so its important to take care
  # of the names given so taht there is no conflict between them and template names


@login_required(login_url='/login')
def updateUser(request):
  user = request.user
  form = UserForm(instance=user)
  if request.method=='POST':
    form = UserForm(request.POST,instance=user)
    if form.is_valid():
      form.save()
      return redirect('base:user-profile',pk=user.id)
  return render(request,'base/update-user.html',{
    'form':form,

  })



def topics(request):
  q=request.GET.get('q') if request.GET.get('q') != None else ''
  topics=Topic.objects.filter(name__icontains=q)
  return render(request,'base/topics.html',{
      'topics':topics
  })






def activityPage(request):
  room_messages=Message.objects.all()
  return render(request,'base/activity.html',{
      'room_messages':room_messages
  })