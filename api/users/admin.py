"""
    Django Admin for User App
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.users.models import User

admin.site.register(User, UserAdmin)
