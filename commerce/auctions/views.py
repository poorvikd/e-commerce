from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *


def index(request):
    context={}
    i=[]
    if request.user :
        for item in AuctionItem.objects.all():
            if WatchList.objects.filter(user=request.user.id, item=item).exists():
                i.append(item.name)
    context["watchlist"]=i
    context["items"] = AuctionItem.objects.all()
    return render(request, "auctions/index.html",context)


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
        first= request.POST["first_name"]
        last= request.POST["last_name"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,first_name=first,last_name=last)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
def create(request):
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html")
    if request.method=="POST":
        auction=AuctionItem()
        user_id = request.user.id
        auction.name= request.POST['name']
        auction.price=float(request.POST['price'])
        auction.description = request.POST.get('description','None')
        auction.photo=request.FILES['photo']
        auction.created_by=User.objects.get(pk=user_id)
        auction.category=request.POST['Category']
        auction.additional_description = request.POST.get(
            'additional_description','None')
        auction.save()
        return HttpResponseRedirect(reverse("index"))
            
    return render(request,"auctions/create.html")
def listing(request,auction_item_id):
    context={}
    auction = AuctionItem.objects.get(pk=auction_item_id)
    if WatchList.objects.filter(user=request.user.id, item=auction).exists():
        context['present']=True
    else:
        if request.method == "POST":
            watch_item=WatchList()
            watch_item.user=User.objects.get(pk=request.user.id)
            watch_item.item=auction
            watch_item.save()
            return HttpResponseRedirect(watchlist,request.user.id)
    context["items"]=auction
    return render(request,"auctions/listing.html",context)
def watchlist(request,user_id):
    watchlist=WatchList.objects.filter(user=user_id)
    return render(request,"auctions/watchlist.html",context={
        "items":watchlist
    })
