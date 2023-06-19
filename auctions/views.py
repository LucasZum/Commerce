from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Category, Comments, Listing, User, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
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
    
def create_view(request):

    categories = Category.objects.all()

    return render(request, 'auctions/create.html', {
        "categories": categories
    })

@login_required
def create(request):
    if not request.POST:
        HttpResponseRedirect(reverse("create"))
    
    title = request.POST["title"]
    description = request.POST["description"]
    price = request.POST["price"]
    category = request.POST["category"]
    user = request.user
    img_url = request.POST["img_url"]

    listing = Listing.objects.create(
        title=title,
        description=description,
        price=price,
        category=Category.objects.get(category=category),
        author=user,
        img_url=img_url,        
    )

    listing.save()

    return HttpResponseRedirect(reverse("index"))

def listing(request, id):

    
    listing = Listing.objects.get(id=id)
    bid = Bid.objects.filter(listing=listing).order_by("-bid")
    last_bid = Bid.objects.filter(listing=listing).order_by("-bid").first()
    comments = Comments.objects.filter(listing=listing)
    

    is_added = True
    if request.user.is_authenticated:
        my_user = request.user
        is_on_my_watchlist = Watchlist.objects.filter(author=my_user, listing=listing).first()
        if not is_on_my_watchlist:
            is_added = False

    im_author = False
    if request.user == listing.author:
        im_author = True

    return render(request, "auctions/listing_view.html", {
        "listing": listing,
        "is_added": is_added,
        "bid": bid,
        "last_bid": last_bid,
        "im_author": im_author,
        "comments": comments
    })

@login_required
def add_watchlist(request, id):

    user = request.user
    listing = Listing.objects.filter(id=id).first()
        
    watchlist = Watchlist.objects.create(
        author=user,
        listing=listing     
    )
    watchlist.save()

    return HttpResponseRedirect(f"/listing/{id}")    

def del_watchlist(request, id):

    user = request.user
    listing = Listing.objects.filter(id=id).first()

    watchlist = Watchlist.objects.filter(author=user, listing=listing)
    watchlist.delete()
    
    return HttpResponseRedirect(f"/listing/{id}")    

def watchlist(request):

    user = request.user
    watchlist = Watchlist.objects.filter(author=user)
    

    return render(request, 'auctions/my_watchlist.html', {
        'watchlist': watchlist
    })

@login_required
def bid(request):

    user = request.user
    bid = int(request.POST["bid"])
    id = request.POST["id"]
    listing = Listing.objects.get(id=id)


    if bid <= listing.price:
        messages.error(request, "the bid must be greater than the current value of the product")
        return HttpResponseRedirect(f"listing/{id}")
    

    Listing.objects.filter(id=id).update(price=bid)
    Bid.objects.create(
        author=user,
        bid=bid,
        listing=listing
    )

    return HttpResponseRedirect(f"listing/{id}")

def close_auction(request, id):

    Listing.objects.filter(id=id).update(is_active=False)
    return HttpResponseRedirect(f"/listing/{id}")


def add_comment(request):

    author = request.user
    comment = request.POST["comment"]
    id = request.POST["id"]
    listing = Listing.objects.get(id=id)

    Comments.objects.create(
        author=author,
        comment=comment,
        listing=listing
    )

    return HttpResponseRedirect(f"listing/{id}")

def all_categories(request):

    categories = Category.objects.all()
    return render(request, 'auctions/all_categories.html', {
        "categories": categories
    })

def category(request, category):

    category = Category.objects.get(category=category)
    listings = Listing.objects.filter(category=category)

    return render(request, 'auctions/index.html', {
        'listings': listings
    })
