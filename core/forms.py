from logging import PlaceHolder
from random import choices
from django import forms
from core.models import (User,Client,LoanAccount,Receipts,Payments)
import decimal

d = decimal.Decimal
    
class ClientForm(forms.ModelForm):
    created_by = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Client
        fields = ["first_name", "last_name", "date_of_birth","national_id",
                  "account_number", "gender", "occupation",
                  "annual_income", "country", "county", "subcounty", "city",
                  "area", "mobile", "pincode","email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.client = kwargs.pop('client', None)
        super(ClientForm, self).__init__(*args, **kwargs)
        not_required = ['city', 'area']
        for field in not_required:
            self.fields[field].required = False

    def clean_mobile(self):
        phone_number = self.cleaned_data.get('mobile')
        try:
            if int(phone_number):
                check_phone = str(phone_number)
                if not phone_number or not(len(check_phone) == 10):
                    raise forms.ValidationError(
                        'Please enter a valid 10 digit phone number')
                return phone_number
        except ValueError:
            raise forms.ValidationError('Please enter a valid phone number')

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if pincode:
            try:
                if int(pincode):
                    check_pin = str(pincode)
                    if not len(check_pin) == 6:
                        raise forms.ValidationError(
                            'Please enter a valid 6 digit pincode')
            except ValueError:
                raise forms.ValidationError(
                    'Please enter a valid pincode')
        return pincode

    def save(self, commit=True, *args, **kwargs):
        instance = super(ClientForm, self).save(commit=False, *args, **kwargs)
        # instance.created_by = User.objects.filter(
        #     username=self.cleaned_data.get('created_by')).first()
        if commit:
            instance.save()
        return instance
    
class UpdateClientProfileForm(forms.Form):
    photo = forms.FileField()
    signature = forms.FileField()

    def __init__(self, instance, *args, **kwargs):
        super(UpdateClientProfileForm, self).__init__(*args, **kwargs)
        
class UserForm(forms.ModelForm):
    
    date_of_birth = forms.DateField(
        required=False,
        input_formats=['%m/%d/%Y'])
    password = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ["email", "first_name", 'last_name',
                  "user_roles", "username", 'county',
                  'subcounty', 'city', 'area', 'mobile', 'pincode']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        #self.fields['gender'].widget.attrs.update({
         #       'placeholder': 'Gender',
         # #'class': 'text-box wid-form select-box-pad'})
        not_required_fields = [ 'county', 'subcounty',
                               'city', 'area', 'mobile',
                               'pincode', 'last_name']
        for field in not_required_fields:
            self.fields[field].required = False
        if not self.instance.pk:
            self.fields['password'].required = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 5:
                raise forms.ValidationError(
                    'Password must be at least 5 characters long!')
        return password

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if pincode:
            try:
                if int(pincode):
                    check_pin = str(pincode)
                    if not len(check_pin) == 6:
                        raise forms.ValidationError(
                            'Please enter a valid 6 digit pincode')
            except ValueError:
                raise forms.ValidationError(
                    'Please enter a valid pincode')
        return pincode

    def clean_mobile(self):
        phone_number = self.cleaned_data.get('mobile')
        try:
            if phone_number is not None:
                if int(phone_number):
                    check_phone = str(phone_number)
                    if not phone_number or not(len(check_phone) == 10):
                        raise forms.ValidationError(
                            'Please enter a valid 10 digit phone number')
                    return phone_number
        except ValueError:
            raise forms.ValidationError('Please enter a valid phone number')

    def save(self, commit=True, *args, **kwargs):
        instance = super(UserForm, self).save(commit=False, *args, **kwargs)
        if not instance.id:
            instance.pincode = self.cleaned_data.get('pincode')
            instance.set_password(self.cleaned_data.get('password'))
        if commit:
            instance.save()
        return instance
    
class LoanAccountForm(forms.ModelForm):
    
    class Meta:
        model = LoanAccount
        fields = ["account_no", "interest_type","interest_rate", "loan_amount","client",
                  "loan_repayment_period", "loan_repayment_every","loanpurpose_description"]

    def clean_loan_repayment_period(self):
        if self.data.get("loan_repayment_period") and self.data.get("loan_repayment_every"):
            if int(self.data.get("loan_repayment_period")) > int(self.data.get("loan_repayment_every")):
                return self.data.get("loan_repayment_period")
            else:
                raise forms.ValidationError("Loan Repayment Period should be greater than Loan Repayment Every")

class ReceiptForm(forms.ModelForm):
    
    class Meta:
        model = Receipts
        fields = ["date", "receipt_number"]


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payments
        fields = ["payment_id","client","payment_type","payment_method", "amount", "interest", "total_amount", "loan_account"]

class ChangePasswordForm(forms.Form):
    
    current_password = forms.CharField(max_length=50, required=True)
    new_password = forms.CharField(max_length=50, required=True)
    confirm_new_password = forms.CharField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current = self.cleaned_data.get("current_password")
        if not self.user.check_password(current):
            raise forms.ValidationError("Current Password is Invalid")
        return current

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password")
        if len(password) < 5:
            raise forms.ValidationError("Password must be at least 5 characters")
        return password

    def clean_confirm_new_password(self):
        password = self.cleaned_data.get("new_password")
        confirm = self.cleaned_data.get("confirm_new_password")
        if password != confirm:
            raise forms.ValidationError("Passwords does not match")
        return confirm

