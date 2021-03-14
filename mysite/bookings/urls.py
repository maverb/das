from django.urls import path
from . import views 


#urls 
urlpatterns = [
    path('?P<pk>\d+/artist_info',views.artist_info,name='artist_info'),
    path('home',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('?P<pk>\d+/calendar_data',views.calendar_data,name='calendar_data'),
    path('', views.index, name='index'),
    path('artist_search/',views.artist_search, name='artist_search'),
    path('?P<pk>\d+/eliminate_artist',views.eliminate_artist, name='eliminate_artist'),
    path('?P<pk>\d+/cancel_offer',views.cancel_offer, name='cancel_offer'),
    path('?P<pk>\d+/contract',views.contract, name='contract'),
    path('?P<pk>\d+/accept_offer',views.accept_offer, name='accept_offer'),
    path('?P<pk>\d+/update_artist',views.update_artist,name='update_artist'),
    path('add_artist/',views.add_artist, name='add_artist'),
    path('all_offers/',views.booking_request, name='all_offers'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('register/',views.register, name='register'),
    path('login/',views.loginPage,name='login'),
    path('?P<pk>\d+', views.profile,name='artist_profile'),
    path('?P<pk>\d+/makeoffer',views.send_offer, name='booking_offer')   
]