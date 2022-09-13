from http import client
from multiprocessing import context
import re
import decimal
from core import urls
from .models import ACCOUNT_STATUS, LoanAccount,Client,Payments,Receipts, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404,JsonResponse
from django.template import Context
from django.contrib import messages
#from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, View
from django.views.generic import ListView, DetailView, RedirectView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models import Sum, Avg, Count, Min,Q
from django.contrib.auth.models import Permission, ContentType
# from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.urls import reverse

from.forms import (ClientForm,UserForm,LoanAccountForm,ChangePasswordForm,PaymentForm,ReceiptForm,UpdateClientProfileForm)

def loginPage(request):
    page= 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(username=username, password=password)
        print(username + password)
        print(user)
        #if user is not None:
        if user is not None:
            login(request, user)
            return redirect('home')
            #return reverse('home')
        else:
            messages.error(request, 'Username or password does not exist.')
        
        #else:
          #  messages.error(request, 'Username or password does not exist.')
            
    context = {'page': page}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerPage(request):
    page='register'
    form= ClientForm()
    if request.method =="POST":
        form= ClientForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.created_by = 'SELF'
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
            
    #context = {'page': page}
    return render(request, 'login.html', {'form': form})
@login_required(login_url ='login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_active and user.is_staff: 
            loans=LoanAccount.objects.filter(created_by=request.user) 
            loans_count=LoanAccount.objects.filter(created_by=request.user).count()
            pending_loans_A = LoanAccount.objects.filter(status='Applied').aggregate(Sum('loan_amount'))
            pending_loans_T = LoanAccount.objects.filter(status='Applied').count()
            disbursed_loans = LoanAccount.objects.filter(status='Approved').aggregate(Sum('loan_amount'))
            disbursed_loans_T = LoanAccount.objects.filter(status='Approved').count()
            loan_amount=LoanAccount.objects.aggregate(Sum('loan_amount'))
            staff_count = User.objects.count()
            clients_count = Client.objects.filter(created_by=request.user).count()
            clients = Client.objects.filter(created_by=request.user)
            context={"user": user,
                     "clients":clients,
                     'loans':loans,
                     'loans_count':loans_count,
                     'disbursed_loans':disbursed_loans,
                     'disbursed_loans_T': disbursed_loans_T,
                    "clients_count": clients_count,
                    "loan_amount" : loan_amount,
                    "staff_count": staff_count,
                    "pending_loans_A" : pending_loans_A,
                    "pending_loans_T" : pending_loans_T
                    }
            return render(request, "admin.html", context)
        elif user.is_client:
            login(request, user)
            messages.error(request, 'Logged in successfully.')
            return redirect('client')
        else:
            messages.error(request, 'user does not exist.')
        #receipts_list = Receipts.objects.all().order_by("-id")
        #payments_list = Payments.objects.all().order_by("-id")
        #"receipts": receipts_list, 
        #"payments": payments_list,
        
        return render(request, "admin.html", context)
    return render(request, "login.html")

def loans(request):
    if request.user.is_authenticated:
        #client_list = Client.objects.filter(created_by=request.user)
        loans=LoanAccount.objects.filter(created_by=request.user)
        context={
            'loans':loans,
        } 
    return render(request,'loans_list.html',context)

def adminview(request):
    return render(request,'admin.html')

def logoutUser(request):
    logout(request)
    return redirect('home')


    
def create_client_view(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            print( JsonResponse({
                "error": False,
                "success_url": reverse('clientprofile', kwargs={"pk": client.id})}))
            return HttpResponseRedirect(reverse("clientprofile",kwargs={"pk": client.id}))
        else:
            return messages.error(request,form.errors)
    return render(request, "client/create.html")

def client_profile_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    return render(request, "client/profile.html", {'client': client})


def update_client_view(request, pk):
    form = ClientForm()
    client_obj = get_object_or_404(Client, id=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, user=request.user, client=client_obj, instance=client_obj)
        if form.is_valid():
            client = form.save()
            return JsonResponse({
                "error": False,
                "success_url": reverse('clientprofile', kwargs={"pk": client.id})
            })
        else:
            return JsonResponse({"error": True, "errors": form.errors})
    return render(request, "client/edit.html", {'client':client_obj})


def updateclientprofileview(request, pk):
    form = UpdateClientProfileForm()
    client_obj = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = UpdateClientProfileForm(request.POST)
        if form.is_valid():
            client_obj.photo = request.FILES.get("photo")
            client_obj.signature = request.FILES.get("signature")
            client_obj.save()
            return JsonResponse({
                "error": False,
                "success_url": reverse('clientprofile', kwargs={"pk": client_obj.id})
            })
        else:
            data = {"error": True, "errors": form.errors}
            return JsonResponse(data)

    photo = str(client_obj.photo).split('/')[-1] if client_obj.photo else None
    signature = str(client_obj.signature).split('/')[-1] if client_obj.signature else None

    return render(request, "client/update-profile.html", {
        'form': form, 'photo': photo, 'signature': signature})


def clients_list_view(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_active and user.is_staff and user.user_roles=='LoanOfficer':
            client_list = Client.objects.filter(created_by=user)
            return render(request, "clients_list.html", {'client_list': client_list})
        elif user.is_active and user.is_staff and user.user_roles=='Supervisor':
            client_list = Client.objects.all()
            return render(request, "clients_list.html", {'client_list': client_list})
        elif user.is_active and user.is_staff and user.user_roles=='OfficeAdmin':
            client_list = Client.objects.filter(created_by=user)
            return render(request, "clients_list.html", {'client_list': client_list})
        else:
            client_list=None
    return render(request, "clients_list.html", {'client_list': client_list})

class SearchClientsView(ListView):
    model = Client
    template_name = "clients_list.html"

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        client_list = Client.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )
        return client_list

def client_inactive_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    if client.is_active:
        count = 0
        loans = LoanAccount.objects.filter(client=client)
        if loans:
            if loans and loans.count() != loans.filter(total_loan_balance=0).count():
                raise Http404("Oops! Member is involved in loan, Unable to delete.")
            else:
                    client.is_active = False
                    client.save()
                    # return HttpResponseRedirect(reverse("micro_admin:viewclient")
            for loan in loans:
                if loan.total_loan_balance == 0:
                    count += 1
                    if count == loans.count():
                        client.is_active = False
                        client.save()
                else:
                    raise Http404("Oops! Member is involved in loan, Unable to delete.")
        else:
            client.is_active = False
            client.save()
    return HttpResponseRedirect(reverse("viewclient"))

def create_loanaccount(request):
    form = LoanAccountForm()
    client_list = Client.objects.filter(created_by=request.user)
    context = {
        'client_list':client_list,
    }
    if request.method == 'POST':
        form = LoanAccountForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.created_by = request.user
            loan.status='Applied'
            loan.interest_charged = (loan.loan_amount*decimal.Decimal(0.05)*2)
            
            if request.POST.get('client'):
                client_id= request.POST.get('client')
                loan.client = Client.objects.get(id=client_id)
            print(request.POST.get('client'))
            loan.loanprocessingfee_amount = 300
            loan.save()
            print(JsonResponse({
                "error": False,
                "success_url": reverse('loans')
            }))
            return HttpResponseRedirect(reverse('loans'))
        else:
            return JsonResponse({"error": True, "errors": form.errors})
    return render(request, "loan/create.html",context)



