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
  if request.method == 'POST':
    username=request.POST.get('username').lower()
    password=request.POST.get('password')

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, "Username not fount.") 

    user = authenticate(request,username=username,password=password)
    if user:
      login(request,user)
      return redirect('base:home')
    else:
       messages.error(request, "Username or password does not exit.") 

  return render(request,'base/login_register.html',{
    'page':page
  })

def home(request):
  q=request.GET.get('q') if request.GET.get('q') != None else '' #nice syntax
  rooms = Room.objects.filter(
    Q(topic__name__icontains=q) |
      Q(name__icontains=q) |
      Q(description__icontains=q)) #nice syntax to reach the second layer
  topics=Topic.objects.all()
  room_count= rooms.count()

  return render(request,'base/home.html',{
    'rooms':rooms,
    'topics':topics,
    'room_count':room_count
  })

def room(request,pk):
  room = Room.objects.get(id=pk)
  room_messages = room.message_set.all().order_by('-created')

  if request.method=='POST':
    message=Message.objects.create(
      user=request.user,
      room=room,
      body=request.POST.get('body')
    )
    return redirect('base:room',pk=room.id) # we could just not do it but this is a post request and it was gonna mess somethings m so ...

  return render(request, 'base/room.html',{
    'room':room,
    'room_messages':room_messages
  })











@login_required(login_url='/login') # new syntax to make sure where the user is going to be 
def createRoom(request):
  form = RoomForm()
  if request.method == 'POST':
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('base:home')     # nice usage of redirect
  return render(request,'base/room_form.html',{
    'form':form
  })

@login_required(login_url='/login') # new syntax to make sure where the user is going to be 
def updateRoom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  # if a user who is not the host, he is not alloewd to update the room

  if request.user != room.host:
    return HttpResponse('You are not allowed to do it')

  if request.method == 'POST':
    form=RoomForm(request.POST,instance=room)
    if form.is_valid():
      form.save()
      return redirect("base:home")

  return render(request, 'base/room_form.html',{
    'form':form
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