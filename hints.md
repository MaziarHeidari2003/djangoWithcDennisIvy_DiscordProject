Dennis Ivy Discord Project


so th whole project is about building website just like discord off course with lower level functionality and optins, but as the expression goes practice makes perfect.
So no matter simple or complicated projects, i must learn more!
Im going to share what i learn and the challenges here.



problem1:

Imagine your home page which is going to display the available rooms, well based on what ? how to filter some specific rooms?

base/home.html:
              <div class="mobile-menu">
                <form method="GET" action="{% url 'base:home' %}" class="header__search">
                    <input placeholder="Search for posts" />
                </form>
              </div>
 views/def home:

from django.db.models import Q

"""
Q is a useful object in Django's ORM that allows you to perform complex lookups by creating query objects that can be combined using bitwise operators | (OR) and & (AND). 
"""

   def home(request):
        q=request.GET.get('q') if request.GET.get('q')  !=None else ''
        rooms = Room.objects.filter(
          Q(topic__name__icontains=q) |
          Q(name__icontains=q) |
          Q(description__icontains=q)
        )
        room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q))



problem2:

  Suppose you want to count the parents of a child, for example Room has a foeign eky to Topic and you want to know how many rooms have the foreign key to a topic
            <ul class="topics__list">
              <li>
                <a href="/" class="active">All <span>553</span></a>
              </li>
              <li>
                <a href="{% url 'base:room' %}">Python <span>{{topics.room_set.all.count}}</span></a>
              </li>
            </ul>
  topics.room_set.all.count is the key          
  topics.room_set.all.count is a Django ORM code snippet typically used to count the number of related objects in a reverse relationship.
  .room_set: The .room_set part refers to a related manager that connects the topics model to another model (probably Room) via a foreign key or a many-to-many relationship. room_set is the default name for a reverse relationship manager if no related_name is specified in the model field.





 problem3:

How do you call a view from a template? Suppose the view has some inputs, 
well I know to ways to pass the inputs:
Using keyword arguments:  {% url 'base:home' sth %}
Using positional arguments: {% url 'base:home' %}?q={{topic.name}}
How to retrieve positional args: q=request.GET.get('q') 






problem4:

topic,created=Topic.objects.get_or_create(name=topic_name) # this is wild !!

The get_or_create method is indeed a powerful and convenient feature in Django's ORM. It attempts to fetch an object from the database based on the provided filters. If an object with those filters doesn't exist, it creates one with the given parameters.


problem5:
  Well while using django model forms for posting data you might use .is_valid() and form.save() syntax, Well that is great, But what if you want to treat a field a bit defferent?
  Im going to show two ways:

  def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # if a user who is not the host, he is not alloewd to update the room

    if request.user != room.host:
      return HttpResponse('You are not allowed to do it')

    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created =Topic.objects.get_or_create(name=topic_name)
        form= RoomForm(request.POST,instance=room)
        room.topic=topic
        room.description = request.POST.get('description')
        room.name = request.POST.get('name')
        room.save()
        return redirect("base:home") 


Well this way is ignoring a big part of vakidation 
now the next solution:
    if request.method=='POST':
      topic_name=request.POST.get('topic')
      form = RoomForm(request.POST,instance=room)
      if form.is_valid():
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room = form.save(commit=False)  # Create the instance without saving it yet
        room.topic=topic
        room.save()
        return redirect("base:home")
      else:
        # Handle invalid form data
      



problem6:
    Im always confused to user redirect or reverse , well i gotta learn this kinda methods someday!

      return redirect('base:user-profile',pk=user.id)

      All I need from this syntax is that the first arg should be the name of the desired url.






problem7:
While working with django rest_framework


  First error to solve => Object of type Room is not JSON serializable
  You cant just pass quesryset which is a python list to Response


  Do you know anything about CORES? CROSS ORIGINE RESOURCE SHARING
  DJANGO-CORES-HEADERS





  problem8:

      to customizer the user built in model of django you have to delete the migration and sqlite file first

      
      class User(AbstractUser):
        pass



      to be added in settings.py:
         AUTH_USER_MODEL='base.User'

