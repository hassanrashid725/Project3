from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import Menu, Toppings, Users, Orders, OrderDetails, ItemCategory, SubsExtra, Extras
from django.urls import reverse
import itertools, functools
from django.core import serializers
from django.contrib.auth import authenticate, logout, login as dj_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
import time, json

# Create your views here.
orderFlag=0
def index(request):
    context = {
        "categories": ItemCategory.objects.all(),
        "menus": Menu.objects.all(),
        "counter": functools.partial(next, itertools.count()),
        "toppings": Toppings.objects.all(),
        "subextras": SubsExtra.objects.all(),
        "extras": Extras.objects.all(),
        "message": "Sign in",
        "user": "Not Logged In"
    }
    if request.user.is_authenticated:
        context["message"]="Log out"
        context["user"]= f"User: {request.user}"

    return render(request, "index.html", context)

def login(request):
    context={
    "message1": "Please sign in to order.",
    "message2": "Log In"
    }
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, "login.html",context)

        logout(request)
        return HttpResponseRedirect(reverse("index"))

    elif request.method == 'POST':
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            context["message1"]="Invalid credentials."
            return render(request, "login.html", context)


def signup(request):
    context={
    "message1": "All fields are required.",
    "message2": "Log In"
    }
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "signup.html", context)
    elif request.method == 'POST':
        try:
            name = request.POST["name"]
            email = request.POST["email"]
            password = request.POST["pw"]
            address = request.POST["address"]
            number = request.POST["contactnumber"]

            if not name or not email or not password or not address or not number:
                raise ValueError('empty string')
        except ValueError:
            context["message1"]="Please enter all the fields."
            return render(request, "signup.html", context)

        if User.objects.filter(username=email).exists():
            context["message1"]="Email Already Registered."
            return render(request, "signup.html", context)

        else:
            user = User.objects.create_user(username=email,first_name=name)
            user.set_password(password)
            user.save()
            Users.objects.create(user=user,address=address,contactNumber=number)
            return HttpResponseRedirect(reverse("login"))

def checkout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    array_data = request.POST.get('arr')
    if type(array_data) is str:
         categories=[]
         pks=[]
         sizes=[]
         prices=[]
         data = json.loads(array_data)
         print(data)
         for n in range(len(data)-3):
             categories.append(data[n]['category'])
             pks.append(data[n]['pk'])

         for num,x in enumerate(data[(len(data)-1)],start=0):
             if (num % 2) == 0:
                 sizes.append(x)

         for p in data[(len(data)-3)]:
             prices.append(float(p))

         k=1
         userinfo=request.user
         user=User.objects.get(username=userinfo.username)
         user1=Users.objects.get(user=user)
         order = Orders(user=user1, totalAmount=data[(len(data)-2)])
         order.save()
         for j in range(len(categories)):
             if sizes[j]=="small":
                 sizes[j]="S"
             else:
                 sizes[j]="L"
             orderDetails = OrderDetails(orderId=order, menuId=Menu.objects.get(pk=pks[j]), size=sizes[j], price=prices[j])
             orderDetails.save()

             if "Pizza" in categories[j]:
                 if data[(len(data)-1)][k] is not None:
                     for l in range(len(data[(len(data)-1)][k])):
                         topping = Toppings.objects.get(name=data[(len(data)-1)][k][l])
                         orderDetails.toppingsId.add(topping)
             elif categories[j] == "Subs":
                 if data[(len(data)-1)][k] is not None:
                     for l in range(len(data[(len(data)-1)][k])):
                         topping = SubsExtra.objects.get(name=data[(len(data)-1)][k][l])
                         orderDetails.subsExtraId.add(topping)
             k+=2
         responseData = {
         'result' : "SUCCESS"
         }
         return JsonResponse(responseData)
    global orderFlag
    orderFlag=1
    time.sleep(3)
    return HttpResponseRedirect(reverse("order"))


def order(request):
    global orderFlag
    if orderFlag == 1:
        userinfo=request.user
        orderUser = User.objects.get(username=userinfo.username)
        orderUser1 = Users.objects.get(user=orderUser)
        orderUser2 = Orders.objects.filter(user=orderUser1)
        orderUser2 = orderUser2[(len(orderUser2)-1)]
        context={
        "orders":OrderDetails.objects.filter(orderId=orderUser2.pk),
        "totalAmount": orderUser2.totalAmount,
        "message": "Log Out",
        "user": f"User: {request.user}"
        }
        orderFlag = 0
        emailCompleteOrder = ""
        toppingList = ""
        for y in context["orders"]:
            if y.menuId.category.categoryName == "Subs":
                for topping in y.subsExtraId.in_bulk():
                    toppingList = toppingList + str(SubsExtra.objects.get(pk=topping)) + " - "
                if len(y.subsExtraId.in_bulk()) <= 0:
                    toppingList = "None"
            else:
                for topping in y.toppingsId.in_bulk():
                    toppingList = toppingList + str(Toppings.objects.get(pk=topping)) + " - "
                if len(y.toppingsId.in_bulk()) <= 0:
                    toppingList = "None"
            orderItem = f"Category: {y.menuId.category.categoryName}\nItem Name: {y.menuId.itemName}\nToppings/Extras: {toppingList}\nSize: {y.size}\nPrice: ${y.price}\n\n"
            emailCompleteOrder = emailCompleteOrder + orderItem
            toppingList = ""
        emailOrder = f'Your Order Details:\n{emailCompleteOrder}Total Amount: ${context["totalAmount"]}'
        send_mail(
        "Order Placed!",
        emailOrder,
        'donotreplycsfifty@gmail.com',
        [userinfo.username],
        fail_silently=False,
        )
        return render (request, "order.html", context)

    else:
        return HttpResponseRedirect(reverse("index"))


def getMenu(request):
    if request.method == 'GET':
        selectedItem = Menu.objects.all()
        menuSerialized = serializers.serialize('json', selectedItem)
        return JsonResponse(menuSerialized, safe=False)
    else:
        return HttpResponse("Request method is not a GET")

def getCategories(request):
    if request.method == 'GET':
        allCatagories = ItemCategory.objects.all()
        catagorySerialized = serializers.serialize('json', allCatagories)
        return JsonResponse(catagorySerialized, safe=False)
    else:
        return HttpResponse("Request method is not a GET")

def getSubsExtraPrices(request):
    if request.method == 'GET':
        subsExtraPrices = SubsExtra.objects.all()
        subsExtraPricesSerialized = serializers.serialize('json', subsExtraPrices)
        return JsonResponse(subsExtraPricesSerialized, safe=False)
    else:
        return HttpResponse("Request method is not a GET")

def contact(request):
    context={
    "message": "Sign in",
    "user": "Not Logged in"
    }
    if request.user.is_authenticated:
        context["message"]="Log out"
        context["user"]= f"User: {request.user}"
    return render(request,"contact.html",context)

def about(request):
    context={
    "message": "Sign in",
    "user": "Not Logged in"
    }
    if request.user.is_authenticated:
        context["message"]="Log out"
        context["user"]= f"User: {request.user}"

    return render(request,"about.html",context)
