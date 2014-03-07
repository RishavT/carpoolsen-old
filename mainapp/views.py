# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from mainapp.models import *
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import Count, Min, Sum, Avg

#def index(request):
    #return HttpResponse("Hello, world. You're at the poll index.")
    
    
#pages

def signup_page(request):
    pass
def login_page(request):
    pass
def search_page(request):
    pass


def dashboard(request):
    return  HttpResponse(request.user.username)


def post_page(request):
    pass
def results_page(request):
    pass

#Actions
@csrf_exempt
def signup_do(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')

    username = request.REQUEST['username']
    password = request.REQUEST['password']
    first_name = request.REQUEST['first_name']
    last_name = request.REQUEST['last_name']
    phone = request.REQUEST['phone']
    email = request.REQUEST['email']
    gender = request.REQUEST['gender']
    car_number = request.REQUEST['car_number']
    
    try:
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        entry = Rider(user=user, phone=phone, gender=gender, car_number=car_number)
        entry.save()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("done")


def logout_do(request):
    logout(request)
    return HttpResponse("logged out")
def login_do(request):
    
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    username = request.REQUEST['username']
    password = request.REQUEST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse("done")
        else:
            # Return a 'disabled account' error message
            return HttpResponse("disabled account")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("invalid login")

def cancel_post(request):
    
    #using get for now.
    user = request.user
    if not user.is_authenticated:
        return HttpResponse("Need to log in")
    postid = request.REQUEST['postid']
    #return HttpResponse(postid)
    try:
        entry = Post.objects.get(pk=int(postid))
        if entry.owner.user.pk == user.pk:
            #Delete reserved entries too
            for y in entry.reserved_set.all():
                #SMS notification
                y.delete()
            entry.delete()
        else:
            return HttpResponse("not authenticated to delete this post")
    except Exception as e:
        return HttpResponse(e)
    
    return HttpResponse("done")

def post_new(request):
    
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    
    
    #New Post
    owner = request.user.rider
    car_number = request.REQUEST['car_number']
    total_seats = int(request.REQUEST['total_seats'])
    phone = request.REQUEST['phone']
    fro = request.REQUEST['fro']
    to = request.REQUEST['to']
    
    #yyyy-mm-dd-hh-mm
    date_time = request.REQUEST['date_time'].split("-")
    date_time = datetime.datetime(year=int(date_time[0]), month=int(date_time[1]), day=int(date_time[2]), hour=int(date_time[3]), minute=int(date_time[4]), second=0, microsecond=0)
    
    
    ac = int(request.REQUEST['ac'])
    men_women = int(request.REQUEST['men_women'])
    available_to = int(request.REQUEST['available_to'])
    
    entry = Post(owner=owner, car_number=car_number, total_seats=total_seats, phone=phone, fro=fro, to=to, date_time=date_time, ac=ac,men_women=men_women,available_to=available_to)
    
    entry.save()
    return HttpResponse("done")

def reserve(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    
    try:
        request.user.rider
    except:
        return HttpResponse("no rider associated")
    try:
        reserver = request.user.rider
        postid = request.REQUEST['postid']
        postobj = Post.objects.get(pk=postid)
        entry = Reserved(post = postobj, reserver = reserver)
        entry.save()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("done")

    
def accept(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    try:
        request.user.rider
    except:
        return HttpResponse("no rider associated")
    try:
        owner = request.user.rider
        resid = request.REQUEST['resid']
        try:
            Reserved.objects.get(pk=resid)
        except Exception as e:
            return HttpResponse(e)
        resobj = Reserved.objects.get(pk=resid)
        
        postobj = resobj.post
        if postobj.total_seats > postobj.reserved_set.aggregate(Sum('status'))['status__sum']:
            resobj.status = 1
            resobj.save()
        else:
            return HttpResponse("seats full")
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("done")

def revoke_res(request):
    #revoke permission from rider
    #opposite of accept
    #called by owner
    pass
def cancel_res(request):
    #cancel reservation
    #called by rider
    #opposite of reserve
    pass
    
    

def search_do(request):
    pass

def edit_post(request):
    pass