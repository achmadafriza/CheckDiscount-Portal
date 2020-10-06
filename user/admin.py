from django.contrib import admin
from .models import Profile

class User(admin.ModelAdmin):
    list_display= ('user', 'phone_number', 'updated_at')

# Register your models here.
admin.site.register(Profile, User)