from django.contrib import admin
from home.models import Project,Bug,Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class CustomizedUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Project)
admin.site.register(Bug)
admin.site.register(Profile)
