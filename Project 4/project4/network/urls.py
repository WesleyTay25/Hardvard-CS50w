
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("edit_follow", views.edit_follow, name="edit_follow"),
    path("following", views.following, name="following"),
    path("edit_post/<int:postid>", views.edit_post, name="edit_post"),
    path("like_post/", views.like_post, name="like_post")
]
