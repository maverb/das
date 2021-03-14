from bookings.models import Offer,Artist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms  


class ArtistForm(forms.ModelForm):
    class Meta:
        model=Artist
        fields=['name','description','rider','photo']

class OfferForm(forms.ModelForm):
    class Meta:
        model=Offer
        fields=['party','date','fee','hosting']

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User    
        fields=['username','email','password1','password2']    