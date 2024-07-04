from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from customer.models import Customer
from django.contrib import messages
from django.contrib.auth import authenticate,login as userLogin , logout as userLogout
from django.contrib.auth.decorators import login_required

# Create your views here.


def account(request):

    context = {}

    if request.POST and 'register' in request.POST:
        context['register'] = True
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:

            # creating user object
            user = User.objects.create_user(
                            username=username,
                            password=password,
                            email=email,
                            first_name=fullname,
            )
            
            # creating customer object
            customer = Customer.objects.create(
                            user=user,
                            address=address,
                            phone=phone
            )
            messages.success(request,'Account created successfully')
            return redirect('account')
        except:
            messages.error(request,'Username already creation failed')
            return redirect('account')
        
    if request.POST and 'login' in request.POST:
        context['register'] = False
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        if user is not None:
            if user.check_password(password):
                userLogin(request,user)
                return redirect('index')
            else:
                messages.error(request,'Invalid credentials')
                return redirect('account')
        else:
            messages.error(request,'Invalid username')
            return redirect('account')    
    return render(request,'account.html',context)

@login_required(login_url='account')
def logout(request):
    userLogout(request)
    return redirect('index')