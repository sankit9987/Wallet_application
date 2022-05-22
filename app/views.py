from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def User_sign_up(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            username = request.POST.get('email')
            password = request.POST.get('pswd')


            if username and password:
                user = User.objects.filter(username=username)
                if user:
                    messages.error(request, "User Already exits")
                    return redirect("register")
                else:
                    user = User.objects.create(username=username)
                    user.set_password(password)
                    user.save()
                    return redirect("login")
            messages.error(request,"All field is must")
            return redirect("register")
        return render(request,"register.html")
    else:
        return redirect("home")

def User_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            username = request.POST.get('email')
            password = request.POST.get('pswd')
            print(username)
            print(password)
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            messages.error(request,"Please check username and password")
            return redirect("login")
        return render(request,"login.html")
    else:
        return redirect("home")

def user_logout(request):
    logout(request)
    return redirect("login")


def home(request):
    if request.user.is_authenticated:
        try:
            if request.method=='POST':
                amount = request.POST.get('amount')
                balance_type = request.POST.get('type')
                
                if balance_type=='Add' and amount:
                    wallet = Wallet.objects.create(user=request.user,amount=amount,status="add")
                    total = Total_amount.objects.filter(user=request.user)
                    if total:
                        total[0].total = int(total[0].total)+int(amount)
                        total[0].save()
                        return redirect("home")
                    Total_amount.objects.create(user=request.user,total=amount)
                    return redirect("home")
                else:
                    total = Total_amount.objects.filter(user=request.user)
                    
                    if total:
                        total[0].total = int(total[0].total)-int(amount)
                        if total[0].total>=0:
                            wallet = Wallet.objects.create(user=request.user,amount=amount,status="remove")
                            total[0].save()
                            return redirect("home")
                        messages.error(request, "Insufficient money")
                        return redirect("home")
                    messages.error(request, "Insufficient money")
                    return redirect("home")

            wallet = Wallet.objects.filter(user = request.user)
            total = Total_amount.objects.filter(user=request.user)
            if total:
                return render(request,"home.html",{'wallet':wallet,"total":total[0]})
            return render(request,"home.html",{'wallet':wallet})
        except Exception as e:
            messages.error(request, "Something is wrong")
            return redirect("home")
    else:
        return redirect("login")