from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Events
from .models import Item
from .models import FoodListing
from .models import Order
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User, auth

from django.views import View

from django.urls import reverse
from urllib.parse import urlencode

from django.views.decorators.csrf import csrf_exempt


from django.http import JsonResponse
import json
# import razorpay


from myProject import settings



# Create your views here.


def index(request):
    # return HttpResponse("HELLO WORLD.....!")
    evnts = Events.objects.all()
    return render(request, 'index.html', {'evnts': evnts}) 


def menu(request):
    items = Item.objects.all()
    return render(request, 'menu.html', {'items':items})

def contactus(request):
    return render(request, 'contactus.html')

def aboutus(request):
    return render(request, 'aboutus.html')

def chefs(request):
    return render(request, 'chefs.html')


class foodListing(View):

    def post(self, request):
        fd = request.POST.get("fd")
        remove = request.POST.get("remove")
        # print(fd)

        cart = request.session.get('cart')
        # cart = request.session['cart']
        if cart:
            quantity = cart.get(fd)
            if quantity :
                if remove:
                    if quantity <= 1:
                        cart.pop(fd)
                    else:
                        cart[fd] = quantity-1
                else:
                    cart[fd] = quantity+1
            else:
                cart[fd] = 1
        else:
            cart = {}
            cart[fd] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        
        #------TRICK TO REDIRECT TO URL WHICH HAS A --QUERY STRING-- IN IT---------
        q = request.META['QUERY_STRING']
        return redirect(reverse('foodListing')+'?'+q)
        

    
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        foodList = None
        # request.session.clear()
        items = Item.get_all_categories()

        categoryID = request.GET['category']
        if categoryID:
            foodList = FoodListing.get_food_by_id(categoryID)
        else:
            foodList = FoodListing.get_all_food()

        data={}
        data['foodList'] = foodList
        data['items'] = items
        print("You are : ", request.session.get('id'))
        # return render(request, 'foodListing.html', {'foodList':foodList})
        return render(request, 'foodListing.html', data)



def custLogout(request):
    auth.logout(request)
    return redirect('/') 

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        foods = FoodListing.get_food_list_by_id(ids)
        print(foods) 
        return render(request, 'cart.html', {'foods': foods})




class OrderView(View):
    def get(self, request):
        customer = request.session.get('id')
        orders = Order.get_order_by_customerid(customer)
        print(orders)
        return render(request, 'order.html', {'orders': orders})



def simpleCheckout(request):
    return render(request, 'simple_checkout.html')

def paymentRazor(request):
    ids = list(request.session.get('cart').keys())
    foods = FoodListing.get_food_list_by_id(ids)
    print(foods) 
    return render(request, 'paymentRazor.html', {'foods': foods})



#Adding  Payment  Gateway-----------
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

# @login_required
class Checkout(View):
    def post(self, request):
        
        # customer = request.session.get('username')
        customer = request.session.get('id')
        cart = request.session.get('cart')
        product = FoodListing.get_food_list_by_id(list(cart.keys()))
        final_price = 0
        # p = Order(customer_confirm = True)
        # p.save()

        
        for prod in product:
            order = Order(customer=User(id=customer), product = prod, price = prod.food_price, quantity = cart.get(str(prod.id)), customer_confirm = True)
            print(order.place_order())
            final_price = final_price + (prod.food_price * cart.get(str(prod.id)))
        print(customer, cart, product)
        print("------------------")
        request.session['cart'] = {}
        order.save()

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/hotel/success"
        # q = request.META['QUERY_STRING']
        # return redirect(reverse('foodListing')+'?'+q)
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=final_price*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))

        # return redirect('paymentRazor')

        return render(request, 'paymentRazor.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':final_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})


@csrf_exempt
def success(request):
    return render(request, "success.html")