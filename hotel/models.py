from django.db import models
from django.contrib.auth.models import User, auth
from django.db.models.fields import DateTimeCheckMixin
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone


# Create your models here.

class Events(models.Model):
    event_id = models.IntegerField()
    event_img = models.ImageField(upload_to = 'eventPics')
    event_name = models.CharField(max_length=100)
    event_desc = models.TextField()
    
    def __str__(self):
        return self.event_name

class Item(models.Model):
    item_img = models.ImageField(upload_to = 'itemPics')
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name

    def get_all_categories():
        return Item.objects.all()

class FoodListing(models.Model):
    food_category = models.ForeignKey(Item, blank = True, null = True, on_delete = models.CASCADE)
    food_name = models.CharField(max_length=100)
    food_desc = models.TextField(blank=True)
    food_img = models.ImageField(upload_to = 'foodListPics', blank=True)
    food_price = models.FloatField()

    def __str__(self):
        return self.food_name

    def get_food_list_by_id(ids):
        return FoodListing.objects.filter(id__in = ids)

    def get_all_food():
        return FoodListing.objects.all()

    def get_food_by_id(category_id):
        if category_id:
            return FoodListing.objects.filter(food_category_id = category_id)
        else:
            return FoodListing.get_all_food();


class Order(models.Model):

    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )

    product = models.ForeignKey(FoodListing, on_delete = models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    price = models.IntegerField()
    order_date = models.DateTimeField(default=timezone.now)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    customer_confirm = models.BooleanField(default=False, blank=False)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    status = models.BooleanField(default=False)

    #related to razorpay
    # razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    # razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    # razorpay_signature = models.CharField(max_length=500, null=True, blank=True)

    def place_order(self):
        self.save()

    def save(self, *args, **kwargs):
        if self.order_id is None and self.order_date and self.id:
            self.order_id = self.order_date.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

    def __str__(self):
            return self.customer.email + " " + str(self.id)

    # @staticmethod
    def get_order_by_customerid(customer_id):
        return Order.objects.filter(customer = customer_id).order_by('-order_date')


    
# class ProductInOrder(models.Model):
#     class Meta:
#         unique_together = (('order', 'product'),)
#     order = models.ForeignKey(Order, on_delete = models.CASCADE)
#     product = models.ForeignKey(FoodListing, on_delete = models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.FloatField()



