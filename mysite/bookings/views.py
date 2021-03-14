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



@login_required



def index (request):
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
    return render(request,'bookings/index.html',context)

def home(request):
  context={

  }
  return render(request,'bookings/home.html',context) 

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
    return render(request,'bookings/profile.html', args)    

def send_offer(request,pk=None):
     form=OfferForm(request.POST or None)
     artist_relation=Artist.objects.get(id=pk) 
     if form.is_valid():
       a=artist_relation.offer_set.create(
         party = form.cleaned_data['party'],
         date = form.cleaned_data['date'],
         fee = form.cleaned_data['fee'],
         hosting = form.cleaned_data['hosting'],
       )
       messages.success(request,'You sent your offer')
       return HttpResponseRedirect('/bookings/')
     context={
       'form':form,
     }  
     return render(request,'bookings/book_it.html',context) 

@csrf_exempt
def loginPage(request):
  ur=request.user
  roster=Artist.objects.filter(user=ur.id)
  context={
    'ur':ur,
    'roster':roster,
  } 
  if request.method=='POST':
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      ur=request.user
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
      return render(request,'bookings/index.html', context)
    else:
      messages.warning(request,'Incorrect user or password')    
  return render(request,'bookings/login.html', context)

def register(request):
  form=CreateUserForm(request.POST or None)
  if form.is_valid():
    form.save()
    messages.success(request,'Your account was created!')
    return redirect('login')
  context={
        'form':form
  } 
  return render(request,'bookings/register.html',context) 

@csrf_exempt
@login_required
def user_profile(request):
  ur=request.user
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
  return render(request,'bookings/user_profile.html' , context) 

@csrf_exempt
@login_required
def booking_request(request):
  user=request.user
  roster=Artist.objects.filter(user=user.id)
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
  return render(request,'bookings/chat.html',context)

@login_required
def add_artist(request):
  form=ArtistForm(request.POST or None,request.FILES or None) 
  user=request.user
  user_relation=User.objects.get(id=user.id) 
  roster=Artist.objects.filter(user=user.id)
  context={
       'form':form  
  }
  if form.is_valid():
       a=user_relation.artist_set.create(
         name = form.cleaned_data['name'],
         description = form.cleaned_data['description'],
         rider = form.cleaned_data['rider'],
         photo=request.FILES['photo']
       )
       messages.success(request,'You just added a new artist')
       return HttpResponseRedirect('/bookings/user_profile')    
  return render(request,'bookings/add_artist.html',context)

@login_required
def artist_info(request,pk=None):
  if pk:
      artist=Artist.objects.get(pk=pk)
  else:
      artist=request.artist  
  context={
      'artist':artist
  }    
  return render(request,'bookings/artist_info.html',context)

@login_required
def update_artist(request,pk=None): 
  if pk:
      artist=Artist.objects.get(pk=pk)
  else:
      artist=request.artist   
  form=ArtistForm(request.POST or None,request.FILES or None,instance=artist)
  user=request.user   
  all_offers=Offer.objects.filter(artist_id=pk) 
  arg={
     'user':user
  }
  #updating throw the form
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
  return render(request,'bookings/update_artist.html',context)

@login_required
def eliminate_artist(request,pk=None):
  user=request.user
  roster=Artist.objects.filter(user=user.id)
  elim=Artist.objects.get(pk=pk)
  #puede ser que se webee cuando no hay ofertsa
  elim_offer=elim.offer_set.all()
  #si hae el query y si elimina
  elim.delete()
  elim_offer.delete()
  messages.success(request,'Artist deleted')
  return HttpResponseRedirect('/bookings/user_profile')

@login_required
def logout(request): 
   django_logout(request)
   context={
   }
   #return render(request,"bookings/home.html",context)
   return HttpResponseRedirect('/bookings/login')
   
@login_required
def accept_offer(request,pk=None):
   off=Offer.objects.get(pk=pk)
   context={
     'off':off,
   }
   return render(request,'bookings/accept_offer.html',context)
   
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
  #return render(request,'bookings/chat.html',context)
  return HttpResponseRedirect('/bookings/all_offers')

@login_required
def cancel_offer(request,pk=None):
  all_offers=Offer.objects.all()
  #delete an offer 
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
  return HttpResponseRedirect('/bookings/all_offers')

def artist_search(request):
  if request.method=='GET':
    search=request.GET.get('search')
    artist_founded=Artist.objects.all().filter(name=search) 
  context={
      'artist_founded':artist_founded,
  }
  return render(request,'bookings/artist_search.html',context)

def calendar_data(request,pk=None):
    artist=Artist.objects.get(pk=pk)
    all_offers=Offer.objects.filter(artist_id=pk)
    context={
         'artist':artist,
         'all_offers':all_offers,
    }
    return render(request,'bookings/calendar_data.html',context)   


 