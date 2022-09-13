from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login',views.loginPage, name='login'),
   
    path('register/', views.registerPage, name="register"),
    
    
    path('loans/', views.loans, name='loans'),
    path('manage/',views.adminview,name='manage'),
    path('logout/', views.logoutUser, name='logout'),
    path('clients_list/', views.clients_list_view, name='viewclient'),
    path('loan/account/', views.create_loanaccount, name='createloan'),
    path('search/', views.SearchClientsView.as_view(), name='SearchClients'),
    path('client/create/', views.create_client_view, name='createclient'),
    path('client/edit/<str:pk>/', views.update_client_view, name='editclient'),
    path('client/delete/<str:pk>/', views.client_inactive_view, name='deleteclient'),
    path('client/profile/<str:pk>/', views.client_profile_view, name='clientprofile'),
    path('client/profile/update/<str:pk>/', views.updateclientprofileview, name='updateclientprofile'),
]
