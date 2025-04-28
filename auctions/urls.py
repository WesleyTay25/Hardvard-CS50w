from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listid>", views.list, name="list"),
    path("edit_watchlist", views.edit_watchlist, name="edit_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:itemid>", views.bid, name="bid"),
    path("winner", views.winner, name="winner"),
    path("history", views.history, name="history"),
    path("comment", views.addcomment, name="comment"),
    path("categories/<str:category>", views.categories, name="category"),
    path("categories", views.showcategories, name="categories"),
]
