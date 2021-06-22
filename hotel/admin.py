from django.contrib import admin
from .models import Events
from .models import Item
from .models import FoodListing
from .models import Order

class AdminFoodListing(admin.ModelAdmin):
    list_display = ['food_name', 'food_category']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['customer', 'product', 'order_date']
    ordering = ['order_date']
    # search_fields = ['customer']

# Register your models here.
admin.site.register(Events)
admin.site.register(Item)
admin.site.register(FoodListing, AdminFoodListing)
