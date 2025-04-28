from django.contrib import admin
from .models import Auction, bidding, comment

# Register your models here.
class auctionadmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'description', 'category','time')
admin.site.register(Auction, auctionadmin)

class biddingadmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'bid', 'time')
admin.site.register(bidding, biddingadmin)

class commentadmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'comment','time')
admin.site.register(comment, commentadmin)