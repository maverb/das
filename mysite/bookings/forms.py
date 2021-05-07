from bookings.models import Offer,Artist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms  


class ArtistForm(forms.ModelForm):
    class Meta:
        model=Artist
        fields=['name','description','rider','photo']
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'description': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'rider': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'photo': forms.FileInput(attrs={'class':'form-control shadow-none'}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model=Offer
        fields=['party','date','fee','hosting']
        widgets={
            'party': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'date': forms.TextInput(attrs={'class':'form-control shadow-none','placeholder': 'yyyy-mm-dd'}),
            'fee': forms.TextInput(attrs={'class':'form-control shadow-none'}),
            'hosting': forms.TextInput(attrs={'class':'form-control shadow-none'}), 
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User    
        fields=['username','email','password1','password2']    