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

#Called when a user clicks logout button.
def logout_do(request):
    logout(request)
    return HttpResponse("logged out")
    
#Called when a user clicks login button. 
def login_do(request):
    
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    username = request.REQUEST['username']
    password = request.REQUEST['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            # Logged in now. Redirect to a success page.
            return HttpResponse("done")
        else:
            # Return a 'disabled account' error message
            return HttpResponse("disabled account")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("invalid login")

#Called when a user cancels his post
def cancel_post(request):
    
    #using get for now.
    user = request.user
    
    #Not allowed to delete if user is not logged in. Not called, but to take edge cases into consideration.
    if not user.is_authenticated:
        return HttpResponse("Need to log in")
    
    postid = request.REQUEST['postid']
    #return HttpResponse(postid)
    
    try:
        entry = Post.objects.get(pk=int(postid))
        if entry.owner.user.pk == user.pk:
            #Delete all reserved entries for that post too
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
    
    #Date and time format: yyyy-mm-dd-hh-mm
    date_time = request.REQUEST['date_time'].split("-")
    date_time = datetime.datetime(year=int(date_time[0]),
                                  month=int(date_time[1]), 
                                  day=int(date_time[2]), 
                                  hour=int(date_time[3]),
                                  minute=int(date_time[4]), 
                                  second=0, 
                                  microsecond=0)
    
    
    ac = int(request.REQUEST['ac'])
    men_women = int(request.REQUEST['men_women'])
    available_to = int(request.REQUEST['available_to'])
    
    entry = Post(owner=owner, 
                 car_number=car_number, 
                 total_seats=total_seats,
                 phone=phone, 
                 fro=fro, 
                 to=to, 
                 date_time=date_time, 
                 ac=ac,
                 men_women=men_women,
                 available_to=available_to)
    
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

def revoke(request):
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
        
        #postobj = resobj.post
        #if postobj.total_seats > postobj.reserved_set.aggregate(Sum('status'))['status__sum']:
            #resobj.status = 1
            #resobj.save()
        if resobj.status == 1:
            resobj.status = 0
            resobj.save()
        else:
            return HttpResponse("Already revoked/pending.")
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("done")

def cancel_res(request):
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
        resid = request.REQUEST['resid']
        resobj = Reserved.objects.get(pk=resid)
        
        if resobj.reserver.pk == reserver.pk:
            resobj.delete()
        else:
            return HttpResponse("invalid user")
        #entry = Reserved(post = postobj, reserver = reserver)
        
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("done")
    

def search_do(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    
    try:
        request.user.rider
    except:
        return HttpResponse("no rider associated")
    
    fro = request.REQUEST['fro']
    to = request.REQUEST['to']
    dtstart = request.REQUEST['dtstart'].split("-")
    dtend = request.REQUEST['dtend'].split("-")
    men_women = request.REQUEST['men_women']
    dtstart = datetime.datetime(year=int(dtstart[0]), month=int(dtstart[1]), day=int(dtstart[2]), hour=int(dtstart[3]),
                                minute=int(dtstart[4]), second=0, microsecond=0)
    dtend = datetime.datetime(year=int(dtend[0]), month=int(dtend[1]), day=int(dtend[2]), hour=int(dtend[3]),
                                minute=int(dtend[4]), second=0, microsecond=0)
    results = Post.objects.filter(fro=fro, to=to, date_time__lte=dtend, date_time__gte=dtstart, men_women=men_women)
    return HttpResponse(len(results))
    

def edit_post(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    
    #Get Post
    owner = request.user.rider
    postid = request.REQUEST['postid']
    postobj = None
    try:
        postobj = Post.objects.get(pk=postid)
    except Exception as e:
        return HttpResponse(e)
    
    #Get new details.
    
    if postobj.owner.user.username <> owner.user.username:
        return HttpResponse("You can't edit others posts!!")
    
    #owner = request.user.rider
    car_number = request.REQUEST['car_number']
    total_seats = int(request.REQUEST['total_seats'])
    phone = request.REQUEST['phone']
    fro = request.REQUEST['fro']
    to = request.REQUEST['to']
    
    #Date and time format: yyyy-mm-dd-hh-mm
    date_time = request.REQUEST['date_time'].split("-")
    date_time = datetime.datetime(year=int(date_time[0]),
                                  month=int(date_time[1]),
                                  day=int(date_time[2]),
                                  hour=int(date_time[3]), 
                                  minute=int(date_time[4]),
                                  second=0, 
                                  microsecond=0)
    ac = int(request.REQUEST['ac'])
    men_women = int(request.REQUEST['men_women'])
    available_to = int(request.REQUEST['available_to'])
    
    #entry = Post(owner=owner, 
                 #car_number=car_number, 
                 #total_seats=total_seats, 
                 #phone=phone, 
                 #fro=fro, 
                 #to=to,
                 #date_time=date_time, 
                 #ac=ac,
                 #men_women=men_women,
                 #available_to=available_to)
    if total_seats < postobj.reserved_set.aggregate(Sum('status'))['status__sum']:
        return HttpResponse("You already have more reserved users than seats.")
    
    postobj.car_number = car_number
    postobj.total_seats = total_seats
    postobj.phone = phone
    postobj.fro = fro
    postobj.to = to
    postobj.date_time = date_time
    postobj.ac = ac
    postobj.men_women = men_women
    postobj.available_to = available_to
    
    postobj.save()
    return HttpResponse("Post edited successfully. Contrary to what people say, Change is NOT good. Please keep edits as minimal as possible")


def send_message(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    sender = None
    try:
        sender = request.user.rider
    except:
        return HttpResponse("no rider associated")
    try:
        receiver = User.objects.get(username=request.REQUEST['to']).rider
        message = request.REQUEST['message']
        
        entry = Message(sender = sender, receiver = receiver, message = message)
        entry.save()
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse("sent")

def view_messages(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    rider = None
    
    try:
        rider = request.user.rider
    except:
        return HttpResponse("no rider associated")
    
    results1 = Message.objects.filter(sender = rider)
    results2 = Message.objects.filter(receiver = rider)
    
    return HttpResponse((len(results1) + len(results2)))

def delete_message(request):
    #if request.method == 'GET':
        #return HttpResponse('invalid request')
        
    #check for user login
    if not request.user.is_authenticated():
        return HttpResponse("need to log in")
    rider = None
    
    try:
        rider = request.user.rider
    except:
        return HttpResponse("no rider associated")
    
    mid = request.REQUEST['mid']
    message = None
    try:
        message = Message.objects.get(pk=mid)
    except:
        return HttpResponse("No such message exists")
    
    if message.sender.pk == rider.pk:
        message.smailbox = 0
    if message.receiver.pk == rider.pk:
        message.rmailbox = 0
    if message.rmailbox + message.smailbox == 0:
        #This means the message has been deleted from both the sender and the receiver's side.
        #The message will be deleted after one month
        #if message.date_time.month - timezone.now().month >= 1:
            #message.delete()
        
        #For now, message will be deleted. In the future, we may implement restoring of messages, in which case
        #We will keep the delete after one month feature.
        message.delete()
    else:
        message.save()
    return HttpResponse("done")