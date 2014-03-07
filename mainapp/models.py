from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
## Create your models here.
#class Poll(models.Model):
    #question = models.CharField(max_length=200)
    #pub_date = models.DateTimeField('date published')
    #def __unicode__(self):  # Python 3: def __str__(self):
        #return self.question
    #def was_published_recently(self):
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

#class Choice(models.Model):
    #poll = models.ForeignKey(Poll)
    #choice_text = models.CharField(max_length=200)
    #votes = models.IntegerField(default=0)
    #def __unicode__(self):  # Python 3: def __str__(self):
        #return self.choice_text


class Rider(models.Model):
    
    #current_post = models.ForeignKey(Post)

    #dummy = models.IntegerField(default=0)
    #username = models.CharField(max_length=200, unique=True)
    user = models.OneToOneField(User)
    #name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    #email = models.CharField(max_length=200)
    gender = models.CharField(max_length=1)
    car_number = models.CharField(max_length=20)
    
    #0 - PAN
    #1 - Driving License
    #2 - Voter Card
    auth_type = models.IntegerField(default=0)
    auth_token = models.CharField(max_length=200, default = "")
    
    
    user_rating = models.IntegerField(default=5)
    neg_flags = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.user.username


class Post(models.Model):
    
    owner = models.ForeignKey(Rider, null=False, related_name='owner')
    
    car_number = models.CharField(max_length=20)
    total_seats = models.IntegerField(default=1)
    phone = models.CharField(max_length=10)
    fro = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    date_time = models.DateTimeField('date_time',default=timezone.now())
    
    #0 - No
    #1 - Yes
    ac = models.IntegerField(default=0)
    
    #pass1 = models.ForeignKey(Rider, related_name='pass1', default=Rider.objects.get(pk=1))
    #pass2 = models.ForeignKey(Rider, related_name='pass2', default=Rider.objects.get(pk=1))
    #pass3 = models.ForeignKey(Rider, related_name='pass3', default=Rider.objects.get(pk=1))
    #pass4 = models.ForeignKey(Rider, related_name='pass4', default=Rider.objects.get(pk=1))
    #pass5 = models.ForeignKey(Rider, related_name='pass5', default=Rider.objects.get(pk=1))
    #pass6 = models.ForeignKey(Rider, related_name='pass6', default=Rider.objects.get(pk=1))
    
    
    #0 - Both
    #1 - Women only
    #2 - Men only
    men_women = models.IntegerField(default=0)
    
    
    #0 - available to all
    #1 - available to only friends
    available_to = models.IntegerField(default=0)
    def __unicode__(self):
        return self.owner.user.username
    

class Reserved(models.Model):
    post = models.ForeignKey(Post)
    reserver = models.ForeignKey(Rider)
    #0 - pending
    #1 - accepted
    status = models.IntegerField(default=0)
    
#Here there also exists another table called 'User', provided by Django. It has username, email and password attributes.
