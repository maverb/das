from django.db import models
import datetime 
import uuid
from django.contrib.auth.models import User
#By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.

# This is the table for the artist information
class Artist(models.Model):
   name=models.CharField(max_length=200)
   description=models.CharField(max_length=200)
   rider=models.CharField(max_length=200)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   photo=models.ImageField(default="nogenderavatar.png",upload_to="images/")
   def __str__(self):
       return '{},{},{}'.format(self.name, self.description, self.rider) 
   


#This is the table for offer 
class Offer(models.Model):
   party=models.CharField(max_length=200)
   date=models.DateField("day of the party")
   fee=models.IntegerField(default=0)
   #food and hotel expenses if necessary 
   hosting=models.IntegerField(default=0) 
   accepted=models.BooleanField(default=False)
   artist=models.ForeignKey(Artist,on_delete=models.CASCADE)

   def __str__(self):
      return '{},{},{},{}'.format(self.party,self.date,self.fee,self.hosting) 
