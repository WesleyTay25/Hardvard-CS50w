from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User

# Register your models here.
@admin.register(User)
class Useradmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Social", {"fields": ("followers",)}),
    )



class Postadmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'time')
admin.site.register(Post, Postadmin)