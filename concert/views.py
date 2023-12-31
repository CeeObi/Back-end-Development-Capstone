from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req


# Create your views here.
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        passwrd = request.POST.get('password')
        try:
            user = User.objects.filter(username=username).exists()            
            if user:                
                return render(request,'signup.html',{"form": SignUpForm, "message":"user already exist"})
            else:
                #Remmeber to use the make_password method to create the password securely
                password=make_password(passwrd)                
                user = User.objects.create_user(username=username, password=passwrd)
                #insert code to log in the user with the django.contrib.aut. module
                login(request, user)
                #insert code to return the user back to the index page
                return HttpResponseRedirect(reverse("index"))
                #return render(request, "index.html")
        except User.DoesNotExist:
            # insert code to render the 'signup.html' page with the 'SignUpForm' form
            return render(request, "signup.html", {"form": SignUpForm})    
    # return {insert code to render the 'signup.html' page with the 'SignUpForm' form}
    return render(request, "signup.html", {"form": SignUpForm})


def index(request):
    return render(request, "index.html")


def songs(request):
    songs = req.get("http://songs-sn-labs-chukwudimaco.labs-prod-openshift-san-a45631dc5778dc6371c67d206ba9ae5c-0000.us-east.containers.appdomain.cloud/song").json()
    #songs = {"songs":[{"id":1,"title":"duis faucibus accumsan odio curabitur convallis","lyrics":"Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis."}]}
    return render(request, "songs.html", {"songs":songs["songs"]})


def photos(request):
    photos = req.get("https://pictures.17q4vce3627w.us-south.codeengine.appdomain.cloud/picture").json()
    # photos = [{
    # "id": 1,
    # "pic_url": "http://dummyimage.com/136x100.png/5fa2dd/ffffff",
    # "event_country": "United States",
    # "event_state": "District of Columbia",
    # "event_city": "Washington",
    # "event_date": "11/16/2022"
    #         }]
    return render(request, "photos.html", {"photos": photos})
    

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        passwrd = request.POST.get('password')
        try:
            #{insert code to find the user with the username}            
            user = User.objects.get(username=username)            
            #{insert code to check the username and password}            
            if user.check_password(passwrd):
                #{insert code to log in the using the django.contrib.auth module}
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        except User.DoesNotExist:
            #{insert code to render the `login.html` method using the `LoginForm` form}
            return render(request, "login.html", {"form": LoginForm})
    return render(request, "login.html", {"form": LoginForm})
    

def logout_view(request):
    #insert code to logout the user using the django.contrib.auth module}
    logout(request)
    #{insert code to return the user to the login page using the HttpResponseRedirect module}
    return HttpResponseRedirect(reverse("login"))

def concerts(request):    
    if request.user.is_authenticated:
        lst_of_concert = []        
        #{insert code to get all Concerts using the Concert.objects object}
        concert_objects = Concert.objects.all()
        #{insert code to loop through all items in the concert_objects}:
        for item in concert_objects:
            print(item)
            try:
                status = item.attendee.filter(
                    user=request.user).first().attending
            except:
                status = "-"
            lst_of_concert.append({
                "concert": item,
                "status": status
            })
        #{insert code to render the `concerts.html` page with the data of {"concerts": lst_of_concert}}
        return render(request, "concerts.html", {"concerts": lst_of_concert})
    else:
        #{insert code to redirect the user to the login page as the user is not authenticated}
        return HttpResponseRedirect(reverse("login"))

def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
