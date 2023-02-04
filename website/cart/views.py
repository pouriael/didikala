from django.shortcuts import get_object_or_404, redirect, render
from requests import session
from home.models import *
from .models import *
from django.contrib import messages
from order.models import *
from django.contrib.auth.decorators import login_required
from accounts.models import *
from django.contrib.auth.models import User
from django.db.models import Q,Max,Min,Sum


def cart_detail(request):
    nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    Profile = ''
    if request.user.is_authenticated:
        Profile = formprofile.objects.get(user_id = request.user.id)
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        
    category = Category.objects.filter(sub_cat = False)
    cart = Cart.objects.filter(user_id = request.user.id)
    total = 0
    form = OrderForm()
    user = request.user
    for p in cart:
        if p.product.status != "None":
            total += p.variants.total_price * p.quantity
        else:
            total += p.quantity * p.product.total_price 
    total_n = 20000 + total
    return render(request,'cart/cart.html',{'compare':compare,'nums':nums,'cart':cart,'total':total,'form':form,'user':user,'category':category,'Profile':Profile,'total_n':total_n})
     
@login_required(login_url="accounts:login")
def add_cart(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.status != 'None':
        var_id = request.POST.get('select')
        data = Cart.objects.filter(user_id = request.user.id,variants_id = var_id)
        if data:
            check= 'yes'
        else:
            check = 'no'
    else:
        data = Cart.objects.filter(user_id = request.user.id,product_id=id)
        if data:
            check = 'yes'
        else:
            check = 'no'
    if request.method == 'POST':
        form = CartForm(request.POST)
        var_id = request.POST.get('select')
        if form.is_valid():
            info = form.cleaned_data['quantity'] 
            if check == 'yes':
                if product.status != 'None':
                    shop = Cart.objects.get(product_id = id,user_id = request.user.id,variants_id=var_id)
                    messages.success(request,"product add to basketshop","success")
                else:
                    shop = Cart.objects.get(product_id = id,user_id =request.user.id)
                    messages.success(request,"product add to basketshop","success")
                shop.quantity +=info
                shop.save()
            else:
                Cart.objects.create(user_id=request.user.id,product_id=id,quantity = info, variants_id = var_id)
        return redirect(url)

def remove_cart(request,id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.get(id = id).delete()
    return redirect(url)

def remove_single(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get( id = id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)

def add_single(request,id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart.objects.get(id = id )
    if cart.product.status == 'None':
        product = Product.objects.get(id= cart.product.id)
        if product.amount > cart.quantity:
            cart.quantity +=1
    else:
        variant = Variantproduct.objects.get( id =cart.variants.id)
        if variant.amount > cart.quantity:
            cart.quantity +=1
    cart.save()
    return redirect(url)

def compare(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        item = get_object_or_404(Product,id =id )
        qs = Compare.objects.filter(user_id = request.user.id, product_id = id)
        if qs.exists():
            messages.success(request,"ok user")
        else:
            Compare.objects.create(user_id=request.user.id,product_id = id,session_key =None)
    else:
        item = get_object_or_404(Product,id =id )
        qs = Compare.objects.filter(user_id = None, product_id = id,session_key = request.session.session_key)
        if qs.exists():
            messages.success(request,"ok user")
        else:
            if not request.session.session_key:
                request.session.create()
            Compare.objects.create(user_id=request.user.id,product_id = id,session_key =request.session.session_key)
            
    return redirect(url)

def show(request):
    
    category = Category.objects.filter(sub_cat = False)
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        return render(request,'cart/show.html',{'compare':compare})
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        return render(request,'cart/show.html',{"compare":compare,'category':category})

def compare_remove(request,id):
    url = request.META.get('HTTP_REFERER')
    Compare.objects.get(id = id).delete()
    return redirect(url)

def compare_filter(request):
    compare= Compare.objects.all()
    return render(request,'home/product.html',{'compare':compare})