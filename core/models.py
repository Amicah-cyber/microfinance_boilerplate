from multiprocessing.sharedctypes import Value
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin,User,Permission


GENDER_TYPES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

USER_ROLES = (
    ('OfficeAdmin', 'OfficeAdmin'),
    ('Supervisor', 'Supervisor'),
    ('LoanOfficer', 'LoanOfficer'),
    ('Cashier', 'Cashier')
)

ACCOUNT_STATUS = (
    ('Applied', 'Applied'),
    ('Withdrawn', 'Withdrawn'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Closed', 'Closed'),
)


INTEREST_TYPES = (
    ('Flat', 'Flat'),
    ('Declining', 'Declining'),
)

RECEIPT_TYPES = (
    ('EntranceFee', 'EntranceFee'),
    ('MembershipFee', 'MembershipFee'),
    ('BookFee', 'BookFee'),
    ('LoanProcessingFee', 'LoanProcessingFee'),
    ('AdditionalSavings', 'AdditionalSavings'),
    ('LoanDeposit', 'LoanDeposit'),
)

FD_RD_STATUS = (
    ('Opened', 'Opened'),
    ('Paid', 'Paid'),
    ('Closed', 'Closed'),
)

PAYMENT_TYPES = (
    ('Loans', 'Loans'),
    ('LoanProcessingFee', 'LoanProcessingFee'),
    ('Penalty', 'Penalty'),
)



class UserManager(BaseUserManager):
    def create_superuser(self, username, first_name, email, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to is_staff=True')
        if other_fields.get('is_admin') is not True:
            raise ValueError('SuperUser must be assigned to is_admin=True')
        return self.create_user(username, first_name, email, password, **other_fields)

    def create_user(self, username,first_name, email, password,**other_fields):
        if not username:
            raise ValueError('Users must have an username')

        # Save the user
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,first_name=first_name,**other_fields)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    


class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)
    user_roles = models.CharField(choices=USER_ROLES, max_length=20)
    date_of_birth = models.DateField(default='2000-01-01', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    county = models.CharField(max_length=50, null=True)
    subcounty = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=150, null=True)
    mobile = models.CharField(max_length=10, default='0', null=True)
    pincode = models.CharField(default='', max_length=10, null=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='user_permissions', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=['email','first_name']

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_admin:
            return True
        # return _user_has_perm(self, perm, obj)
        else:
            try:
                user_perm = self.user_permissions.get(codename=perm)
            except ObjectDoesNotExist:
                user_perm = False

            return bool(user_perm)

    class Meta:
        permissions = (
            ("OfficeAdmin",
             "Can manage all users accounts."),
        )


class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    national_id= models.PositiveIntegerField(default=0)
    email = models.EmailField(max_length=255, null=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)
    account_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_TYPES, max_length=10)
    occupation = models.CharField(max_length=200)
    annual_income = models.BigIntegerField()
    country = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    subcounty = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20, default=True, null=True)
    pincode = models.CharField(max_length=20, default=True, null=True)
    photo = models.ImageField(upload_to=settings.PHOTO_PATH, null=True)
    signature = models.ImageField(upload_to=settings.SIGNATURE_PATH, null=True)
    is_active = models.BooleanField(default=True)
    is_client = models.BooleanField(default=True)
    status = models.CharField(max_length=50, default="UnAssigned", null=True)
    bookfee_amount = models.DecimalField(max_digits=19, decimal_places=6, default=0)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    def __str__(self):
        return f"{self.first_name},{self.last_name}"
    
    @property
    def get_loan(self):
        self.loan=LoanAccount()
        if self.loan.client == self:
            return self.loan
    


class LoanRepaymentEvery(models.Model):
    value = models.IntegerField()


class LoanAccount(models.Model):
    account_no = models.CharField(max_length=50, unique=True)
    interest_type = models.CharField(choices=INTEREST_TYPES, max_length=20)
    client = models.ForeignKey(Client, null=True, blank=True,on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT)
    status = models.CharField(choices=ACCOUNT_STATUS, max_length=20)
    opening_date = models.DateField(auto_now_add=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    loan_issued_date = models.DateField(null=True, blank=True)
    loan_issued_by = models.ForeignKey(User, null=True, blank=True, related_name="loan_issued_by",on_delete=models.PROTECT)
    closed_date = models.DateField(null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=19, decimal_places=6)
    loan_repayment_period = models.IntegerField()
    loan_repayment_every = models.IntegerField()
    loan_repayment_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True)
    total_loan_amount_repaid = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    loanpurpose_description = models.TextField()
    interest_charged = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    total_interest_repaid = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    total_loan_paid = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    total_loan_balance = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    loanprocessingfee_amount = models.DecimalField(max_digits=19, decimal_places=6, default=0)
    no_of_repayments_completed = models.IntegerField(default=0)

    def __unicode__(self):
        return self.account_no
    
    def __str__(self):
        return self.account_no
    


class Receipts(models.Model):
    date = models.DateField()
    receipt_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client, null=True, blank=True,on_delete=models.PROTECT)
    member_loan_account = models.ForeignKey(LoanAccount, null=True, blank=True,on_delete=models.PROTECT)
    group_loan_account = models.ForeignKey(LoanAccount, null=True, blank=True, related_name="group_loan_account",on_delete=models.PROTECT)
    sharecapital_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    entrancefee_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    membershipfee_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    bookfee_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    loanprocessingfee_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    savingsdeposit_thrift_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    fixeddeposit_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    recurringdeposit_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    loanprinciple_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    loaninterest_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    insurance_amount = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    staff = models.ForeignKey(User,on_delete=models.PROTECT)
    savings_balance_atinstant = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True)
    demand_loanprinciple_amount_atinstant = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    demand_loaninterest_amount_atinstant = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    principle_loan_balance_atinstant = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)

    def __unicode__(self):
        return self.receipt_number

    def __str__(self):
        return self.receipt_number


class Payments(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client, null=True, blank=True,on_delete=models.PROTECT)
    staff = models.ForeignKey(User, null=True, blank=True,on_delete=models.PROTECT)
    payment_type = models.CharField(choices=PAYMENT_TYPES, max_length=25)
    amount = models.DecimalField(max_digits=19, decimal_places=6)
    interest = models.DecimalField(max_digits=19, decimal_places=6, null=True, blank=True, default=0)
    total_amount = models.DecimalField(max_digits=19, decimal_places=6)
    totalamount_in_words = models.CharField(max_length=200)
    loan_account = models.ForeignKey(LoanAccount, related_name='payment_loanaccount', blank=True, null=True,on_delete=models.PROTECT)
    
    def __unicode__(self):
        return self.voucher_number
