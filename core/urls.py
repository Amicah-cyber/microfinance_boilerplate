from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login',views.loginPage, name='login'),   
    path('register/', views.registerPage, name="register"),   
    path('loans/', views.loans, name='loans'),
    path('logout/', views.logoutUser, name='logout'),
    path('clients_list/', views.clients_list_view, name='viewclient'),
    path('loan/account/', views.create_loanaccount, name='createloan'),
    path('loan/account/<str:pk>/', views.show_allloandets, name='loandetails'),
    path('loan/update/<str:pk>/', views.update_loan_view, name='updateloandetails'),
    path('loan/delete/<str:pk>/', views.delete_loanaccount, name='deleteloan'),
    path('viewperm/', views.view_permissions, name='permit'),
    path('search/', views.SearchClientsView.as_view(), name='SearchClients'),
    path('search_user/', views.SearchUserView.as_view(), name='SearchUsers'),
    path('client/create/', views.create_client_view, name='createclient'),
    path('client/edit/<str:pk>/', views.update_client_view, name='editclient'),
    path('client/delete/<str:pk>/', views.client_inactive_view, name='deleteclient'),
    path('client/profile/<str:pk>/', views.client_profile_view, name='clientprofile'),
    path('client/profile/update/<str:pk>/', views.updateclientprofileview, name='updateclientprofile'),
    path('users/list/', views.users_list_view, name='userslist'),
    path('user/create/', views.create_user_view, name='createuser'),
    path('user/edit/<str:pk>/', views.update_user_view, name='edituser'),
    path('user/profile/<str:pk>/', views.user_profile_view, name='userprofile'),
    path('user/delete/<str:pk>/', views.user_inactive_view, name='deleteuser'),
    path('payments/payloan/', views.loan_payment, name='payloan'),
]
