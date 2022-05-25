from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Menu, Cart
from datetime import datetime,date
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required

# Create your views here.

#menu admin routes/urls
def index (request):
    return render(request,'index.html')

def menu_list_admin (request):
    menu_items = Menu.objects.all();
    return render(request,'menu-item-list-admin.html',{'menu_items':menu_items})

def edit_menu_item (request,id):    
    #
    menu_item = Menu.objects.get(id=id)
    #
    if request.method == "POST":
        item = Menu.objects.get(id=id)
        #getting data
        item_name = request.POST.get('name')
        item_active = request.POST.get('active')
        item_category = request.POST.get('category')
        item_dateoflaunch = datetime.strptime(request.POST.get('date_of_launch'), "%Y-%m-%d").strftime("%Y-%m-%d")
        item_delivery = request.POST.get('freeDelivery')
        item_price = request.POST.get('price')
        # print(f"Item name - {item_name} its price {item_price} is active {item_active} category type {item_category} delivery {item_delivery} and date of launch {item_dateoflaunch}")
        
        if(item_name==None):
            messages.add_message(request, messages.ERROR, 'Required Item Name !')
            return redirect(f'/menu/admin/edit/{id}',{'menu_item':menu_item})
        elif(item_active==None):
            item_active = "No"
        elif(item_category==None):
            messages.add_message(request, messages.ERROR, 'Required Item Category !')
            return redirect(f'/menu/admin/edit/{id}',{'menu_item':menu_item})
        elif(item_delivery==None):
             item_delivery = "No"
        elif(item_dateoflaunch==None):
            messages.add_message(request, messages.ERROR, 'Required Item Date of Launch !')
            return redirect(f'/menu/admin/edit/{id}',{'menu_item':menu_item})
        
        item.name = item_name
        item.price = item_price
        if(item_active=="Yes"):            
            item.active = True
        else:
            item.active = False        
        item.date_of_launch = item_dateoflaunch
        if(item_delivery=="Yes"):            
            item.delivery_free = True
        else:
            item.delivery_free = False
        item.category_type = item_category
        item.save()
        
        return redirect('/menu/admin/edit/status')
    
    #Normal Render
    return render(request,'edit-menu-item.html',{'menu_item':menu_item})

def menu_item_status (request):
    return render(request,'edit-menu-item-status.html')


#menu customer routes/url
def signup (request):
    #
    if(request.method == "POST"):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if(password == confirmpassword):
            if(User.objects.filter(email=email).exists()):
                messages.info(request,'This email is already taken, try with another one !')
                return redirect('/signup')            
            elif(User.objects.filter(username=username).exists()):
                messages.info(request,'This username is already taken, try with another one !')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
        else:
            messages.info(request,'Password and confirm password does not match !')
            return redirect('/signup')
        
    
    return render(request,'signup.html')

def signin (request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/customer/menu')
        else:
            messages.info(request,'Invalid username or password !')
            return redirect('/signin')
        
    return render(request,'signin.html')

@login_required(login_url='signin')
def logout (request):
    auth.logout(request)
    return redirect('/signin')

@login_required(login_url='signin')
def menu_list_customer (request):
    menu_items = Menu.objects.filter(active=True, date_of_launch__lte=date.today())
    return render(request,'menu-item-list-customer.html',{'menu_items':menu_items})

@login_required(login_url='signin')
def cart_list_customer (request):
    carts = Cart.objects.filter(user_id=request.user)
    return render(request,'cart.html',{'carts':carts})


@login_required(login_url='signin')
def cart_list_customer_add (request,id,name,delivery,price,category):
    #
    carts = Cart.objects.filter(user_id = request.user)
    #
    current_user = request.user
    cart_object = Cart()
    cart_object.user_id = current_user
    cart_object.name = name
    cart_object.price = price
    if(delivery == 'False'):
        cart_object.delivery_free=False
    else:
        cart_object.delivery_free=True
        
    cart_object.category_type=category
    cart_object.save()
    
    messages.info(request,'Item added to cart successfully')
    return redirect('/customer/cart',{'carts':carts})

@login_required(login_url='signin')
def delete_cart_item(request,id):
    cart_obj = Cart.objects.filter(user_id=request.user,id=id)
    # print(cart_obj)
    cart_obj.delete()
    messages.info(request,"Item removed from cart successfully !")
    return redirect('/customer/cart')
    