<div class="layout__body">
        <form class="form" action="" method="POST">
          {% csrf_token %}
          <div class="form__group">
            <label for="room_topic">Enter a Topic</label>
            <input required type="text" value="{{room.topic.name}}" name="topic" list="topic-list" />
            <datalist id="topic-list">
              <select id="room_topic">
                {% for topic in topics %}
                <option value="{{topic.name}}">{{topic.name}}</option>
                {% endfor %}
              </select>
            </datalist>
          </div>


          <div class="form__group">
            <label for="room_name">Room Name</label>
            {{form.name}}
          </div>

          <div class="form__group">
            <label for="room_description">Room Description</label>
            {{form.description}}
          </div>
          
          <!-- <div class="form__group">
            <label for="room_topic">Topic</label>
            <input required type="text" name="topic" id="room_topic" list="topic-list" />
            <datalist id="topic-list">
              <select id="room_topic">
                <option value="">Select your topic</option>
                <option value="Python">Python</option>
                <option value="Django">Django</option>
              </select>
            </datalist>

          </div> -->


          <div class="form__action">
            <a class="btn btn--dark" href="{{request.META.HTTP_REFERER}}">Cancel</a>
            <button class="btn btn--main" type="submit">Submit</button>
          </div>
        </form>
      </div>



      its is a new appearance and methdology to handle forms in the template for me . believe it or not , its wild!

      and before that, the design was like this 
      <fom>
          {% for field in form %}
          <div>
                <label for="room_name">{{field.label}}</label>
          </div>
      </form>





         <div class="layout__body">
        <form class="form" action="" method="POST">
          {% csrf_token %}
          {% for field in form %}
          <div class="form__group">
            <label for="room_name">{{field.label}}</label>
            {{field}}
            <!--<input id="room_name" name="room_name" type="text">-->
          </div>
          {% endfor %}