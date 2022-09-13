from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import LoanAccount,Client,User,Payments,Receipts
from .forms import UserForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    model=User
    add_form = UserForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','first_name','last_name','email', 'date_of_birth','is_staff','is_admin',
                    'is_active','user_roles','county','subcounty','city','area','pincode','mobile')
    list_filter = ('is_admin','is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','email','date_of_birth','user_roles','county','subcounty','city','area','pincode','mobile')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_admin','groups', 'user_permissions')}),
    )
    print(fieldsets)
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password','first_name','last_name','date_of_birth','is_staff','is_admin',
                    'is_active','user_roles','county','subcounty','city','area','pincode','mobile'),
        }),
    )
    search_fields = ('username','email')
    ordering = ('username',)
    filter_horizontal = ()

# Register your models here.
admin.site.register(LoanAccount)
admin.site.register(Client)
admin.site.register(User,UserAdmin)
admin.site.register(Payments)
admin.site.register(Receipts)
