
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render ,get_object_or_404
from .models import *
from django.contrib import messages
from accounts.models import *
from .forms import *
from django.db.models import Q,Max,Min,Sum
from cart.models import *
from django.core.paginator import Paginator
from .filters import ProductFilter
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required

def home(requests):
    if requests.user.is_authenticated:
        compare = Compare.objects.filter(user_id = requests.user.id)
    else:
        compare = Compare.objects.filter(session_key__exact = requests.session.session_key,user_id =None)
    sell = Product.objects.all().order_by('sell')[:6]
    create = Product.objects.all().order_by('-create')[:6]
    category = Category.objects.filter(sub_cat = False)
    gallery =Gallery.objects.all()
    nums = Cart.objects.filter(user_id =requests.user.id ).aggregate(sum=Sum('quantity'))['sum']
    suggest = Product.objects.all().order_by('-create')
    context = {'category':category,'gallery':gallery,'create':create,'nums':nums,'sell':sell,'compare':compare,'suggest':suggest}
    return render(requests,"home/home.html",context)

def product(request,slug=None,id=None):
    nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        
    cart_form = CartForm()
    products = Product.objects.all()
    min = Product.objects.aggregate(unit_price = Min('unit_price'))
    min_price = int(min['unit_price'])
    max = Product.objects.aggregate(unit_price = Max('unit_price'))
    max_price = int(max['unit_price']+100)
    filter = ProductFilter(request.GET,queryset=products)
    products = filter.qs
    category = Category.objects.filter(sub_cat = False)
    paginator = Paginator(products,4 )
    page_num = request.GET.get('page')
    data = request.GET.copy()
    if 'page' in data:
        del data['page']
    page_obj = paginator.get_page(page_num)
    if slug and id:
        data = get_object_or_404(Category,slug =slug,id=id)
        page_obj = products.filter(category = data)
        paginator = Paginator(page_obj,4)
        page_num = request.GET.get('page')
        data = request.GET.copy()
        if 'page' in data:
            del data['page']
        page_obj = paginator.get_page(page_num)
    form  = SearchForm()
    if 'search' in request.GET:
        form  = SearchForm(request.GET)
        if form.is_valid():
            info = form.cleaned_data['search']
            page_obj = products.filter(Q(name__contains = info))
            paginator = Paginator(page_obj,8 )
            page_num = request.GET.get('page')
            data = request.GET.copy()
            if 'page' in data:
                del data['page']
            page_obj = paginator.get_page(page_num)
    context = {"products":page_obj,"category":category,'compare':compare,'form':form,'page_num':page_num,'filter':filter,'min_price':min_price,'max_price':max_price,'data':data,'nums':nums}
    return render(request,"home/product.html",context)
    

def detail_product(request,id):
    nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        
    product = get_object_or_404(Product,id =id)
    category = Category.objects.filter(sub_cat = False)
    ip = request.META.get('REMOTE_ADDR')
    view = Views.objects.filter(product_id =product.id,ip = ip)
    if not view.exists():
        Views.objects.create(product_id = product.id,ip = ip)
        product.num_view +=1
        product.save()
    if request.user.is_authenticated:
        product.view.add(request.user)
    update = Chart.objects.filter(product_id = id)
    change = Chart.objects.all()
    similar = product.tags.similar_objects()[:2]
    comment_form = CommentForm()
    comment = Comment.objects.filter(product_id = id , is_reply =False)
    reply_form = ReplyForm()
    cart_form = CartForm()
    images = Images.objects.filter(product_id= id)
    is_like =False
    is_unlike =False
    is_favourite =False
    if product.favourite.filter(id = request.user.id).exists():
        is_favourite = True
    if product.like.filter(id = request.user.id).exists():
        is_like =True
    if product.unlike.filter(id = request.user.id).exists():
        is_unlike =True
    if product.status != "None":
        if request.method == "POST" :
            variant =Variantproduct.objects.filter(product_variant_id = id)
            var_id = request.POST.get("select")
            variants = Variantproduct.objects.get(id = var_id)
            colors = Variantproduct.objects.filter(product_variant_id=id,size_variant_id = variants.size_variant_id)
            size = Variantproduct.objects.raw(
                'SELECT * FROM home_Variantproduct WHERE product_variant_id=%s GROUP BY size_variant_id',[id]
            )
        else:
            variant =Variantproduct.objects.filter(product_variant_id = id)
            variants = Variantproduct.objects.get(id = variant[0].id)
            colors = Variantproduct.objects.filter(product_variant_id=id,size_variant_id = variants.size_variant_id)
            size = Variantproduct.objects.raw(
                'SELECT * FROM home_Variantproduct WHERE product_variant_id=%s GROUP BY size_variant_id',[id]
            )
        context = {"product":product,'size':size,'colors':colors,"variant":variant,"variants":variants,'similar':similar,"is_like":is_like,'is_unlike':is_unlike,'cart_form':cart_form
                    ,"comment_form":comment_form,'compare':compare,'nums':nums,'comment':comment,'category':category,"reply_form":reply_form,'images':images,'cart_form':cart_form,'is_favourite':is_favourite,'change':change}
        return render(request,"home/detail.html",context)
    else:
        return render(request,"home/detail.html",{'compare':compare,'product':product , "similar":similar,"is_like":is_like,'is_unlike':is_unlike,'cart_form':cart_form,
                    "comment_form":comment_form,'category':category,'nums':nums,'comment':comment,"reply_form":reply_form,'images':images,'cart_form':cart_form,'is_favourite':is_favourite,"update":update})

def product_like(request,id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,id=id)
    is_like =False
    if product.like.filter(id = request.user.id).exists():
        product.like.remove(request.user)
        is_like =False
        messages.success(request,"unlike","warning")
    else:
        product.like.add(request.user)
        is_like =True
        messages.success(request,"like","success")
    return redirect(url)

def product_unlike(request,id):
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,id=id)
    is_unlike =False
    if product.unlike.filter(id = request.user.id).exists():
        product.unlike.remove(request.user)
        is_unlike =False
        messages.success(request,"dislike remove","warning")
    else:
        product.unlike.add(request.user)
        is_unlike =True
        messages.success(request,"dislike","danger")
    return redirect(url)
    
def product_comment(request,id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create( comment = data['comment'],rate = data["rate"],user_id = request.user.id,product_id = id)
            return redirect(url)
    
def remove_com(request,id):
    url = request.META.get('HTTP_REFERER')
    Comment.objects.get(id = id).delete()
    return redirect(url)

def product_reply(request,id,comment_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            data = reply_form.cleaned_data
            Comment.objects.create(comment = data['comment'],product_id = id,user_id = request.user.id,reply_id =comment_id,is_reply = True)
            messages.success(request,"tnx for reply","primary")
            return redirect(url)

def comment_like(request,id):
    url = request.META.get("HTTP_REFERER")
    comment = Comment.objects.get(id=id)
    if comment.comment_like.filter(id=request.user.id).exists():
       comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)
    return redirect(url)

def product_search(request):
    products =Product.objects.all()
    if request.method == "POST":
        form  = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['search']
            if data.isdigit():
                products = products.filter(Q(discount__exact = data)| Q(unit_price__exact = data))
            else:
                products = products.filter(Q(name__contains = data))
            return render(request,"home/product.html",{"products":products,'form':form})

@login_required
def favourite_product(request,id):
    
    url = request.META.get("HTTP_REFERER")
    product = get_object_or_404(Product,id=id)
    is_favourite =False
    if product.favourite.filter(id = request.user.id).exists():
        product.favourite.remove(request.user)
        product.total_favourite -=1
        product.save()
        is_favourite =False
        messages.success(request,"this product removed at favourite","warning")
    else:
        product.favourite.add(request.user)
        product.total_favourite +=1
        product.save()
        is_favourite =True
        messages.success(request,"this product added to favourite","success")
    return redirect(url)

def contact(request):
    nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    if request.user.is_authenticated:
        compare = Compare.objects.filter(user_id = request.user.id)
        
    else:
        compare = Compare.objects.filter(session_key__exact = request.session.session_key,user_id =None)
        
    category = Category.objects.filter(sub_cat = False)
    if request.method == "POST":
        subject = request.POST['subject']
        email = request.POST['email']
        msg = request.POST['message']
        body = subject + '\n' + email + '\n' + msg
        form = EmailMessage(
            'contact form', 
            body,
            'test',
            ('pouriael2002@gmail.com',),
        )
        form.send(fail_silently = False)
    return render(request,'home/contact.html',{'compare':compare,'category':category,'nums':nums})

def privacy(request):
    return render(request,'home/privacy.html')