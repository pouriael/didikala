from django.shortcuts import(
    redirect,
    render ,
    get_object_or_404,render
    ) 
from django.db.models import Q,Max,Min,Sum
from django.core.paginator import Paginator

from .models import *
from .filters import *
from home.models import *
from cart.models import *

# this function for all blog.
def blog(request):
    cart = Cart.objects.filter(user_id = request.user.id)
    total = 0
 
    for p in cart:
        if p.product.status != "None":
            total += p.variants.total_price * p.quantity
        else:
            total += p.quantity * p.product.total_price 
    nums = Cart.objects.filter(user_id =request.user.id ).aggregate(sum=Sum('quantity'))['sum']
    blog = Blog.objects.all()
    create = Blog.objects.all().order_by('-create')[:5]
    tag = Blog.tags.all()
    paginator = Paginator(blog,6)
    page_num = request.GET.get('page')
    data = request.GET.copy()
    if 'page' in data:
        del data['page']
    page_obj = paginator.get_page(page_num)
    category = Category.objects.filter(sub_cat = False)
    return render(request,"blog/blog.html",{'blog':blog ,'nums':nums,'total':total,'create':create,'tag':tag,'data':data,'blogs':page_obj,'page_num':page_num,'category':category})

# this function for detail blog
def detail(request,id):
    blog = get_object_or_404(Blog,id = id)
    blog_all = Blog.objects.all()
    filter = BlogFilter(request.GET,queryset=blog_all)
    blog_all = filter.qs
    create = Blog.objects.all().order_by('-create')[:5]
    bazdid = sorted(blog_all,key= lambda t: t.total_asli(),reverse=True)
    tag = Blog.tags.all()
    similar = blog.tags.similar_objects()
    if request.user.is_authenticated:
        blog.views.add(request.user)
    else :
        blog.total += 1
        blog.save()
    views = blog.total_asli()
    return render(request,"blog/detail.html",{'blog':blog,'views':views,'filter':filter,'blog_all':blog_all,'create':create,'bazdid':bazdid,'similar':similar,'tag':tag})

# this function for category blog
def dastebandi(request,id):
    tag =  Blog.tags.get(id =id)
    blog = Blog.objects.filter(tags =tag)
    
    return render(request,'blog/dastebandi.html',{'tag':tag,'blog':blog})
