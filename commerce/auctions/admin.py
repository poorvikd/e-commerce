# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import UserCreationForm,UserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form= UserCreationForm
    form= UserChangeForm
    model= User
    list_display=['email','username','first_name','last_name','is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Other info', {
         'fields': ('first_name', 'last_name')}),
        ('Permissions', {
         'fields': ( 'is_staff', )}),
    )
admin.site.register(User,CustomUserAdmin)
admin.site.register(AuctionItem)
admin.site.register(WatchList)
admin.site.register(Bid)
