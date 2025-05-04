from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def post(request):
    if request.method == "POST":
        content = request.POST["content"]
        if not content:
            messages.error(request, "Enter Content")
        post = Post(
            content = content,
            user = request.user
        )
        post.save()

    posts = Post.objects.all().order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": page_obj
    })


def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user.id).order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "posts": page_obj,
        "profile": user
    })
@login_required
def edit_follow(request):
    if request.method == "POST":
        userid = request.POST["user"]
        user = User.objects.get(pk=userid)
        if request.user not in user.followers.all():
            user.followers.add(request.user)
            return redirect("profile", user.username)
        else:
            user.followers.remove(request.user)
            return redirect("profile", user.username)
    return redirect('index')

@login_required
def following(request):
    following_id = request.user.following.all()
    posts = Post.objects.filter(user__in = following_id).order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page_obj
    })

@csrf_protect
def edit_post(request, postid):
    try:
        post = Post.objects.get(pk=postid)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        if data.get("edited") is not None:
            post.edited = data["edited"]
        post.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)

@csrf_protect
@require_POST
@login_required
def like_post(request):
    data = json.loads(request.body)
    postid = data.get("postid")
    try:
        post = Post.objects.get(pk=postid)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return JsonResponse({
        "likecount": post.likes.count()
    })