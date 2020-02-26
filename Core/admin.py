from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Core.models import *

# Register your models here.
@admin.register(SCTFUser)
class SCTFUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_verified',)}),
    )

@admin.register(AccountVerification)
class AccountVerificationAdmin(admin.ModelAdmin):
    pass

@admin.register(PasswordGroup)
class PasswordGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    pass