from accounts.models import cust
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth



# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import auth
from .models import cust


#Create your views here.
def custLogin(request):
    if request.method=="POST":
        cust_name = request.POST['username']
        # customer = User.objects.get(username=cust_name)
        # customer = get_object_or_404(User, username=cust_name)

        try:
            customer = User.objects.get(username=cust_name)
        except User.DoesNotExist:
            messages.info(request,'User Does Not Exist...Please Register :)')
            return redirect('custRegister')
        
        # cust_mail = request.POST['cust_mail']
        cust_password = request.POST['password']

        user=auth.authenticate(username=cust_name, password=cust_password)
        # if cust.objects.filter(password=password).exists():
        if user is not None:
            auth.login(request, user)
            request.session['id'] = customer.id
            request.session['username'] = cust_name
            request.session['cart'] = {}
            # print(cust_id)
            return redirect("/")

        else:
            print(cust_name)
            messages.info(request,'Invalid credentials...Please try again :(')
            return redirect('custLogin')
    else:
        return render(request, 'custLogin.html')




def custRegister(request):
    
    if request.method == 'POST':
        cust_name = request.POST['username']
        cust_mail = request.POST['email']
        cust_password = request.POST['password']

        if User.objects.filter(username=cust_name).exists():
            # print("Username taken")
            messages.info(request,'Username taken')
            return redirect('custRegister')
        elif User.objects.filter(email=cust_mail).exists():
            # print("Email already exists!!")
            messages.info(request,'Email already exists!!')
            return redirect('custRegister')
        else:
            custVar = User.objects.create_user(username=cust_name,password=cust_password,email=cust_mail)
            custVar.save();
            # custVar2 = cust(cust_name=cust_name, cust_mail=cust_mail,cust_password=cust_password)
            # custVar2.save();
            print("Customer regestered successfully!")
            messages.info(request,'Regestered successfully!...Please Login')
        return redirect('custLogin')

    else:
        return render(request, 'custRegister.html')


def custLogout(request):
    auth.logout(request)
    return redirect('/') 


