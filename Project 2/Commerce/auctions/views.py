from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Auction, bidding, comment, User

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.filter(active=True)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        if not title:
            return render(request, "auctions/create.html", {
                "message":"Enter item name"
            })
        price = request.POST["price"]
        if not price:
            return render(request, "auctions/create.html", {
                "message":"Enter starting bid"
            })
        if float(price) < 0:
            return render(request, "auctions/create.html", {
                "message":"Price cannot be below zero"
            })
        description = request.POST["description"]
        if not description:
            return render(request, "auctions/create.html", {
                "message":"Enter description"
            })
        imageurl = request.POST["image"]
        categories = request.POST["categories"]
        auction = Auction(
            title=title,
            price=price,
            description=description,
            image=imageurl,
            category=categories,
            creator=request.user,
            winner=None
        )
        auction.save()
        messages.success(request, "Auction created successfully!")
        return redirect('index')
    else:
        return render(request, "auctions/create.html")
    
def list(request, listid):
    try:
        list = Auction.objects.get(pk=listid)
    except Auction.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message":"Page not Found"
        })
    return render(request, "auctions/list.html", {
        "list":Auction.objects.get(pk=listid),
        "comments":comment.objects.filter(item=listid)
    })

@login_required
def edit_watchlist(request):
    if request.method == "POST":
        item = request.POST["item"]
        function = request.POST["function"]
        user = request.user
        if function == "add":
            user.watchlist.add(item)
            messages.success(request, "Item added to watchlist")
        elif function == "remove":
            user.watchlist.remove(item)
            messages.success(request, "Item removed from watchlist")
        
        return render(request, "auctions/list.html", {
        "list":Auction.objects.get(pk=item)
        })

@login_required   
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist":watchlist
    })
    

@login_required
def bid(request, itemid):
    try:
        auction = Auction.objects.get(pk=itemid)
    except Auction.DoesNotExist:
        return render(request, "auctions/error.html", {
            "message":"Page not Found"
        })
    if request.method == "POST":
        bid_now = request.POST["bid"]
        currentbid = auction.price
        if float(bid_now) < currentbid:
            messages.error(request,"Bid must be higher than current price!")
            return redirect('list', listid=itemid)
        
        bidding.objects.create(
            bid = bid_now,
            user = request.user,
            item = auction
        )

        auction.price = bid_now
        auction.save()

        messages.success(request, "Bid successful!")
        return redirect('list', listid=itemid)
    else:
        return redirect('list', listid = itemid)

@login_required
def winner(request):
    if request.method == "POST":
        item = request.POST["item"]
        auction = Auction.objects.get(pk=item)
        highestbid = auction.bidders.order_by('-bid').first()
        auction.winner = highestbid.user
        auction.active = False
        auction.save()

        messages.success(request, "Auction Closed sucessfully!")
        return redirect('list', listid = item)
    return redirect('list', listid=item)
        
def history(request):
    return render(request, "auctions/history.html", {
        "listings": Auction.objects.all()
    })

def addcomment(request):
    if request.method == "POST":
        item = request.POST["item"]
        auction = Auction.objects.get(pk=item)
        comments = request.POST["comment"]
        if not comments:
            messages.error(request, "Enter Comment!")
            return redirect('list', listid=item)
        comment.objects.create(
            comment = comments,
            user = request.user,
            item = auction
        )
        messages.success(request, "Comment entered successfully!")
        return redirect('list', listid=item)
    return redirect('list', listid=item)

def showcategories(request):
    unique_categories = Auction.objects.values_list('category', flat=True).distinct().order_by('category')
    print(unique_categories)
    return render(request, "auctions/categories.html", {
        "categories": unique_categories
    })

def categories(request, category):
    listing = Auction.objects.filter(category = category)
    return render(request, "auctions/category.html", {
        "listings": listing,
        "category":category
    })
