from http import client
from multiprocessing import context
from os import PRIO_USER
import re
import decimal
from core import urls
from .models import ACCOUNT_STATUS, LoanAccount,Client,Payments,Receipts, User,USER_ROLES
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
from django.forms import modelformset_factory,inlineformset_factory,modelform_factory

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
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')   
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
    return render(request, 'login.html', {'form': form})


@login_required(login_url ='login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_active and user.is_staff: 
            loans=LoanAccount.objects.filter(created_by=request.user) 
            loans_count=LoanAccount.objects.filter(created_by=request.user).count()
            pending_loans_A = LoanAccount.objects.filter(status='Applied',created_by=request.user).aggregate(Sum('loan_amount'))
            pending_loans_T = LoanAccount.objects.filter(status='Applied',created_by=request.user).count()
            disbursed_loans = LoanAccount.objects.filter(status='Approved',created_by=request.user).aggregate(Sum('loan_amount'))
            disbursed_loans_T = LoanAccount.objects.filter(status='Approved',created_by=request.user).count()
            loan_amount=LoanAccount.objects.filter(created_by=request.user).aggregate(Sum('loan_amount'))
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



def logoutUser(request):
    logout(request)
    return redirect('home')


####----- CLIENT MANAGEMENT -----####
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

####-----LOAN  MANAGEMENT-----####

def loans(request):
    if request.user.is_authenticated:
        #client_list = Client.objects.filter(created_by=request.user)
        loans=LoanAccount.objects.filter(created_by=request.user)
        context={
            'loans':loans,
        } 
    return render(request,'loans_list.html',context)

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
            print(loan)
            loan.created_by = request.user
            loan.status='Applied'
            interest_charged=0
            loan_amount= loan.loan_amount
            print(loan.interest_rate)
            if loan.interest_rate is not None:
                i=decimal.Decimal(loan.interest_rate)
                principle=[]
                n = loan_amount/loan.loan_repayment_period
                for x in range(0,loan.loan_repayment_period,loan.loan_repayment_every):
                    interest_charged += (i/100 * loan_amount)
                    principle.append(interest_charged+loan_amount)
                    loan_amount = loan_amount - n
                    print(interest_charged)
                loan.interest_charged =  interest_charged
            
            if request.POST.get('client'):
                client_id= request.POST.get('client')
                loan.client = Client.objects.get(id=client_id)
            loan.loanprocessingfee_amount = 300
            loan.save()
            return HttpResponseRedirect(reverse('loans'))
        else:
            return JsonResponse({"error": True, "errors": form.errors})
    return render(request, "loan/create.html",context)

def delete_loanaccount(request,pk):
    loan =  LoanAccount.objects.get(id=pk)
    print(loan)
    return HttpResponseRedirect(reverse('loans'))
    
def show_allloandets(request,pk):
    loan=LoanAccount.objects.get(id=pk)
    context={
        'loan':loan
    }
    return render(request,'loan/loan_profile.html',context)

def update_loan_view(request, pk):
    loanform=modelform_factory(LoanAccount,form=LoanAccountForm,exclude=('client',))
    loan_obj = get_object_or_404(LoanAccount, id=pk)
    form = loanform(instance=loan_obj)
    #queryset = LoanAccount.objects.filter(id=pk)
    #formset = LoanAccountFormset(queryset=queryset)
    #print(formset)
    #forms = formset[0]
    if request.method == 'POST':
        form = LoanAccountForm(request.POST, instance=loan_obj)
        if form.is_valid():
            loan = form.save(commit=False)
            interest_charged=0
            loan_amount= loan.loan_amount
            if loan.interest_rate is not None:
                i=decimal.Decimal(loan.interest_rate)
                principle=[]
                n = loan_amount/loan.loan_repayment_period
                for x in range(0,loan.loan_repayment_period,loan.loan_repayment_every):
                    interest_charged += (i/100 * loan_amount)
                    principle.append(interest_charged+loan_amount)
                    loan_amount = loan_amount - n
                    print(interest_charged)
                loan.interest_charged =  interest_charged
            loan.save()
            return HttpResponseRedirect(reverse('loandetails', kwargs={"pk": loan.id}))
        else:
            return JsonResponse({"error": True, "errors": form.errors})
    return render(request, "loan/edit.html", {'loan':loan_obj, 'form':form})

###-------------USER MANAGEMENT---------###
def create_user_view(request):
    contenttype = ContentType.objects.get_for_model(request.user)
    print(contenttype)
    permissions = Permission.objects.filter(content_type_id=contenttype, codename__in=["OfficeAdmin","edit_clients","Add_user","view_clients","manage_clients"])
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if len(request.POST.getlist("user_permissions")):
                user.user_permissions.add(*request.POST.getlist("user_permissions"))
            if request.POST.get("user_roles") == "OfficeAdmin":
                if not user.user_permissions.filter(id__in=request.POST.getlist("user_permissions")).exists():
                    user.user_permissions.add(Permission.objects.get(codename="OfficeAdmin"))
            return HttpResponseRedirect(reverse("userprofile",kwargs={"pk": user.id}))
        else:
            return JsonResponse({"error": True, "errors": form.errors})

    return render(request, "user/create.html", {
        'form': form, 'userroles': USER_ROLES, 'permissions': permissions})
    

def update_user_view(request, pk):
    contenttype = ContentType.objects.get_for_model(request.user)
    permissions = Permission.objects.filter(content_type_id=contenttype, codename__in=["OfficeAdmin","edit_clients","Add_user","view_clients","manage_clients"])
    form = UserForm()
    selected_user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=selected_user)
        if form.is_valid():
            if not (
               request.user.is_admin or request.user == selected_user or
               (
                   request.user.has_perm("OfficeAdmin") and
                   request.user.branch == selected_user.branch
               )):
                return JsonResponse({
                    "error": True,
                    "message": "You are unbale to Edit this staff details.",
                    "success_url": reverse('userslist')
                })
            else:
                user = form.save()
                user.user_permissions.clear()
                user.user_permissions.add(*request.POST.getlist("user_permissions"))
                if request.POST.get("user_roles") == "OfficeAdmin":
                    if not user.user_permissions.filter(id__in=request.POST.getlist("user_permissions")).exists():
                        user.user_permissions.add(Permission.objects.get(codename="OfficeAdmin"))

                return JsonResponse({
                    "error": False,
                    "success_url": reverse('OfficeAdmin', kwargs={"pk": user.id})
                })
        else:
            return JsonResponse({"error": True, "errors": form.errors})

    return render(request, "user/edit.html", {
        'form': form, 'userroles': USER_ROLES, 'permissions': permissions, 'selecteduser': selected_user})


def user_profile_view(request, pk):
    selecteduser = get_object_or_404(User, id=pk)
    return render(request, "user/profile.html", {'selecteduser': selecteduser})


def users_list_view(request):
    list_of_users = User.objects.filter(is_admin=0)
    return render(request, "user/list.html", {'list_of_users': list_of_users})


def user_inactive_view(request, pk):
    user = get_object_or_404(User, id=pk)
    if (request.user.is_admin or (request.user.has_perm("OfficeAdmin") and
                                  request.user.branch == user.branch)):
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
    return HttpResponseRedirect(reverse('userslist'))


class SearchUserView(ListView):
    model = User
    template_name = "user/list.html"
    def get_queryset(self):  # new3000
        query = self.request.GET.get("q")
        user_list = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)
        )
        return user_list
    
def view_permissions(request):
    permissions=Permission.objects.all()
    return render(request, "permissionn.html", {'permissions': permissions})

####---------PAYMENT----------####

def loan_payment(request):
    form = PaymentForm()
    if request.method=='POST':
        form=PaymentForm(request.POST)
        if form.is_valid():
            form.save()
    context={}
    return render(request,'Payments/pay_loan.html',context)