from django.urls import path
from .views import foodListing
from .views import Cart
from .views import simpleCheckout
from .views import Checkout
from .views import OrderView
from .views import paymentRazor
from .views import success



from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path("custLogout",views.custLogout,name="custLogout"),
    path('foodListing', foodListing.as_view(), name='foodListing'),
    path('cart', Cart.as_view(), name='cart'),
    path('contactus',views.contactus, name='contactus'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('chefs',views.chefs, name='chefs'),
    path('checkout', Checkout.as_view(), name='checkout'),
    path('order', OrderView.as_view(), name='order'),
    path('simpleCheckout', views.simpleCheckout, name='simpleCheckout'),
    path('paymentRazor', views.paymentRazor, name='paymentRazor'),
    path('success', views.success, name='success'),
    # path('foodListing', views.foodListing, name='foodListing'),
]