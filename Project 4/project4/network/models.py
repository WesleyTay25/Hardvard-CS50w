from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import localtime


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    content = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    edited = models.BooleanField(default=False)

    def formattedtime(self):
        sg_timezone = localtime(self.timestamp)
        return sg_timezone.strftime('%b %d, %Y, %I:%M %p')