from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction", blank=True, null=True)


class Auction(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="winnings")
    title = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.TextField(default="https://static.vecteezy.com/system/resources/previews/015/568/001/original/question-mark-red-hand-drawn-doodle-faq-symbol-free-vector.jpg")
    description = models.TextField(blank=True)
    category = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True) # timestamp
    active = models.BooleanField(default=True)
    

    def formattedtime(self):
        return self.time.strftime('%b %d, %Y, %I:%M %p')


class bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items_bid")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bidders")
    bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    comment = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
