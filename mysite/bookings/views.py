from django.shortcuts import render,redirect 
from django.http import HttpResponse,Http404,HttpResponseRedirect 
from django.shortcuts import render
from .models import Artist,Offer
from .forms import OfferForm,CreateUserForm,ArtistForm 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import calendar 
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger



#index view with all the artists available in the platform
def index (request):
    #this variable queries all the artists in the database
    artist_name=Artist.objects.all()
    paginator=Paginator(artist_name,7)
    page=request.GET.get('page',1)
    try:
       p=paginator.page(page) 
    except PageNotAnInteger:  
       p=pagintor.page(1)
    except EmptyPage:   
       p=paginator.page(paginator.num_pages)
    context={
          'page': page,
          'p': p,
          'artist_name': artist_name,
    }
    return render(request,'index.html',context)

#profile view for every single artist in the platform
def profile (request,pk=None):
    user=request.user
    user_id=user.id
    roster=Artist.objects.filter(user=user.id)
    if pk:
      artist=Artist.objects.get(pk=pk)
    else:
      artist=request.artist  
    args={
        'artist': artist,
        'roster':roster,
    } 
    return render(request,'profile.html', args)    

#send offer is a view for sending contract offers to the artist or agency
def send_offer(request,pk=None):
     #using the offer form 
     form=OfferForm(request.POST or None)
     #artist_relation is a variable that let us relate the offer with the artist for saving matters
     artist_relation=Artist.objects.get(id=pk) 
     #once the offer is sent
     if form.is_valid():
       a=artist_relation.offer_set.create(
         party = form.cleaned_data['party'],
         date = form.cleaned_data['date'],
         fee = form.cleaned_data['fee'],
         hosting = form.cleaned_data['hosting'],
       )
       artist_relation.save()
       messages.success(request,'You sent your offer')
       return HttpResponseRedirect('/')
     context={
       'form':form,
     }  
     return render(request,'book_it.html',context) 

#just a regular log in page
@csrf_exempt
def loginPage(request):
  #the context is empty before the log in
  context={
  } 
  #getting the data from the form in the log in page
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    #authenticating the user
    user=authenticate(request,username=username,password=password)
    if user is not None:
      ur=request.user
      #querying all the artists in the platform
      all_artist=Artist.objects.all()
      paginator=Paginator(all_artist,6)
      page=request.GET.get('page',1)
      try:
           p=paginator.page(page) 
      except PageNotAnInteger:  
           p=paginator.page(1)
      except EmptyPage:   
           p=paginator.page(paginator.num_pages)
      context={
          'ur':ur,
          'all_artist':all_artist,
          'page':page,
          'p':p,
      } 
      login(request,user)
      return render(request,'index.html', context)
    else:
      messages.warning(request,'Incorrect user or password')    
  return render(request,'login.html', context)

#just a regular register page
def register(request):
  form=CreateUserForm(request.POST or None)
  #validating the form to evaluate if it has any error 
  if form.is_valid():
    form.save()
    messages.success(request,'Your account was created!')
    return redirect('login') 
  context={
        'form':form
  } 
  return render(request,'register.html',context) 

#view that contains all the artists that the USER has created
@csrf_exempt
@login_required
def user_profile(request):
  #requesting the user to load the data
  ur=request.user
  #filtering the artists that the user created
  roster=Artist.objects.filter(user=ur.id)
  paginator=Paginator(roster,6)
  page=request.GET.get('page',1)
  try:
      p=paginator.page(page) 
  except PageNotAnInteger:  
      p=paginator.page(1)
  except EmptyPage:   
      p=paginator.page(paginator.num_pages)
  context={
      'ur':ur,
      'roster':roster,
      'page':page,
      'p':p,
  }
  return render(request,'user_profile.html' , context) 

#a view to handle all the offers that the artists of the user received 
@csrf_exempt
@login_required
def booking_request(request):
  user=request.user
  #filtering the artists that the user created
  roster=Artist.objects.filter(user=user.id)
  #filtering all the offers that were not accepted at that given moment
  all_offers=Offer.objects.filter(accepted=False)
  paginator=Paginator(all_offers,4)
  page=request.GET.get('page',1)
  try:
      p=paginator.page(page) 
  except PageNotAnInteger:  
      p=paginator.page(1)
  except EmptyPage:   
      p=paginator.page(paginator.num_pages)
  context={
      'roster':roster,
      'all_offers':all_offers,
      'page':page,
      'p':p,
  }
  return render(request,'all_offers.html',context)

#a view to handle the creation of a new artist
@login_required
def add_artist(request):
  form=ArtistForm(request.POST or None,request.FILES or None) 
  user=request.user
  #establishing the relation between the artist and the user
  user_relation=User.objects.get(id=user.id) 
  #filtering the roster
  roster=Artist.objects.filter(user=user.id)
  context={
       'form':form  
  }
  #validating and saving the form 
  if form.is_valid():
       a=user_relation.artist_set.create(
         name = form.cleaned_data['name'],
         description = form.cleaned_data['description'],
         rider = form.cleaned_data['rider'],
         photo=request.FILES['photo']
       )
       messages.success(request,'You just added a new artist')
       return HttpResponseRedirect('/user_profile')    
  return render(request,'add_artist.html',context)

#a view to handle the initial information and the calendar of each artist created by the user
@login_required
def artist_info(request,pk=None):
  if pk:
      artist=Artist.objects.get(pk=pk)
  else:
      artist=request.artist  
  context={
      'artist':artist
  }    
  return render(request,'artist_info.html',context)

#a view to handle the actualization of the artist information
@login_required
def update_artist(request,pk=None): 
  if pk:
      artist=Artist.objects.get(pk=pk)
  else:
      artist=request.artist   
  #we are going to need the artist form later    
  form=ArtistForm(request.POST or None,request.FILES or None,instance=artist)
  user=request.user   
  all_offers=Offer.objects.filter(artist_id=pk) 
  arg={
     'user':user
  }
  #updating throw the form after running the validation
  if form.is_valid():
    artist=form.save(commit=False)
    artist.save()
    messages.success(request,'Information updated')
    return HttpResponseRedirect(reverse('user_profile'))
  context={
        'form':form,
        'all_offers':all_offers,
        'artist':artist,
  }  
  return render(request,'update_artist.html',context)

#a view to handle the deletion of a given artist 
@login_required
def eliminate_artist(request,pk=None):
  user=request.user
  roster=Artist.objects.filter(user=user.id)
  eliminate=Artist.objects.get(pk=pk)
  #deliting the offers that were done for this artist
  eliminate_offer=eliminate.offer_set.all()
  eliminate.delete()
  eliminate_offer.delete()
  messages.success(request,'Artist deleted')
  return HttpResponseRedirect('/user_profile')

#a view to handle the log out
@login_required
def logout(request): 
   django_logout(request)
   context={
   }
   return HttpResponseRedirect('/')

#a view to handle the acceptance of each offer   
@login_required
def accept_offer(request,pk=None):
   off=Offer.objects.get(pk=pk)
   context={
     'off':off,
   }
   return render(request,'accept_offer.html',context)

#a view to handle the confirmation of the acceptance    
@login_required 
def contract(request,pk=None):
  all_offers=Offer.objects.all()
  #when we accept an offer 
  off=Offer.objects.get(pk=pk)
  off.party=off.party
  off.date=off.date
  off.fee=off.fee
  off.hosting=off.hosting 
  off.accepted=True  
  off.save()
  messages.success(request,'Offer accepted')
  user=request.user
  roster=Artist.objects.filter(user=user.id)
  context={
    'user':user,
    'roster':roster,
    'all_offers':all_offers,
  }
  return HttpResponseRedirect('/all_offers')

#a view to handle the cancelation of each offer
@login_required
def cancel_offer(request,pk=None):
  all_offers=Offer.objects.all()
  #delete the offer 
  eliminate=Offer.objects.get(pk=pk) 
  eliminate.delete()
  user=request.user
  roster=Artist.objects.filter(user=user.id)
  messages.success(request,'You canceled the gig')
  context={
    'user':user,
    'roster':roster,
    'all_offers':all_offers 
  }
  return HttpResponseRedirect('/all_offers')

#a view to handle the search bar 
def artist_search(request):
  if request.method=='POST':
    search=request.POST.get('search')
    artist_founded=Artist.objects.all().filter(name=search) 
  context={
      'artist_founded':artist_founded,
  }
  return render(request,'artist_search.html',context)

#a view to handle the calendar with the gigs that every artist have setted
def calendar_data(request,pk=None):
    artist=Artist.objects.get(pk=pk)
    all_offers=Offer.objects.filter(artist_id=pk)
    context={
         'artist':artist,
         'all_offers':all_offers,
    }
    return render(request,'calendar_data.html',context)   

#a view to handle the specific of the gigs placed in the calendar
def event_data(request,pk=None):
  offer=Offer.objects.get(id=pk) 
  context={
    'offer':offer,
  }
  return render(request,'event_data.html',context)

  