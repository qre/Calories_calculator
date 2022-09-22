from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .filters import fooditemFilter
# Create your views here.

@login_required(login_url='login')
#@admin_only #uncomment that if you want the main page to nly be accessible to users with admin rights
def home(request):
    bread=Category.objects.filter(name='bread, cereal')[0].fooditem_set.all()[:5]
    meat=Category.objects.filter(name='meat, fish')[0].fooditem_set.all()[:5]
    fruits=Category.objects.filter(name='fruits, vegetables')[0].fooditem_set.all()[:5]
    milk=Category.objects.filter(name='milk, dairy')[0].fooditem_set.all()[:5]
    fats = Category.objects.filter(name='fats, sugars')[0].fooditem_set.all()[:5]
    customers=Customer.objects.all()
    context={'bread':bread,
              'meat':meat,
              'fruits':fruits,
              'milk':milk,
              'fats':fats,
              'customers':customers,
            }
    return render(request,'main.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fooditem(request):
    bread=Category.objects.filter(name='bread, cereal')[0].fooditem_set.all()
    bcnt=bread.count()
    meat=Category.objects.filter(name='meat, fish')[0].fooditem_set.all()
    mcnt=meat.count()
    fruits=Category.objects.filter(name='fruits, vegetables')[0].fooditem_set.all()
    fcnt=fruits.count()
    milk=Category.objects.filter(name='milk, dairy')[0].fooditem_set.all()
    mcnt=milk.count()
    fats=Category.objects.filter(name='fats, sugars')[0].fooditem_set.all()
    facnt=fats.count()
    context={'bread':bread,
              'bcnt':bcnt,
              'mcnt':mcnt,
              'mcnt':mcnt,
              'fcnt':fcnt,
              'facnt':facnt,
              'meat':meat,
              'fruits':fruits,
              'milk':milk,
              'fats':fats,
            }
    return render(request,'fooditem.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createfooditem(request):
    
    # f = ProductFilter(request.GET, queryset=Product.objects.all())
    # has_filter = any(field in request.GET for field in set(f.get_fields()))

    # return render(request, 'my_app/template.html', {
    #     'filter': f,
    #     'has_filter': has_filter
    # })
    form = fooditemForm()
    if request.method == 'POST':
        form = fooditemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'createfooditem.html',context)

@unauthorized_user
def registerPage(request):
    form=createUserForm()
    if request.method=='POST':
        form=createUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='user')
            user.groups.add(group)
            email=form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=username,email=email)
            messages.success(request,'Account created for '+username)
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)

@unauthorized_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/user')
        else:
            messages.info(request,'username or password is invalid')
    return render(request,'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

def userPage(request):
    user=request.user or request.admin
    cust=user.customer
    action = request.POST.get('action', '')
    fooditems=Fooditem.objects.filter()
    myfilter = fooditemFilter(request.GET,queryset=fooditems)
    has_filter = any(field in request.GET for field in set(myfilter.get_fields()))
    fooditems=myfilter.qs
    total=UserFooditem.objects.all()
    myfooditems=total.filter(customer=cust)
    cnt=myfooditems.count()
    querysetFood=[]
    for food in myfooditems:
        querysetFood.append(food.fooditem.all())
    finalFoodItems=[]
    for items in querysetFood:
        for food_items in items:
            finalFoodItems.append(food_items)
    totalCalories=0
    for foods in finalFoodItems:
        totalCalories+=foods.calories
    # if action == 'reset':
    #     querysetFood.delete()

    CaloriesLeft=2000-totalCalories
    context={'CaloriesLeft':CaloriesLeft,'totalCalories':totalCalories,'cnt':cnt,'foodlist':finalFoodItems,
    'fooditem':fooditems,'myfilter':myfilter, 'has_filter': has_filter}
    return render(request,'user.html',context)

def addFooditem(request):
    user=request.user
    cust=user.customer
    if request.method=="POST":
        form =addUserFooditem(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/user')
    form=addUserFooditem()
    context={'form':form}
    return render(request,'addUserFooditem.html',context)

def delete(request, id):
    #user=request.user
    #cust=user.customer
    #total=UserFooditem.objects.all()
    fooditems=Fooditem.objects.filter()
    #myfilter = fooditemFilter(request.GET,queryset=fooditems)
    #myfooditems=myfilter.filter(customer=cust)
    fooditem=fooditems.get(id=id)
    fooditem.delete()
    # fooditem=Fooditem.objects.get(id=id)
    # fooditem.delete()
    return redirect('/user')