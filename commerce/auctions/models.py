from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
class User(AbstractUser):
    first_name=models.CharField(max_length=64)
    last_name=models.CharField(max_length=64)
class AuctionItem(models.Model):
    name=models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    photo = models.ImageField(blank=True,null=True,upload_to="items/%Y/%m/%d/")
    description = models.TextField(blank=True,null=True,max_length=80)
    additional_description=models.TextField(blank=True,null=True)
    category = models.CharField(max_length=64,blank=True,null=True)
    def __str__(self):
        return f"{self.name}"
class WatchList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user}-{self.item}"
class Bid(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    new_bid = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.item}-{self.new_bid}"
