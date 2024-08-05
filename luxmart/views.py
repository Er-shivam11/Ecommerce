from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect
from .models import Product,CartItem,Order,CustomUser
from .forms import ProductForm,OrderForm,CustomerRegisterForm
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
# C:\Users\User\python_projects\django_projects
from django.http import HttpResponse
from django.db.models import Q

from django.shortcuts import render



@login_required(login_url="login")
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.method == 'POST':
        create_form = CustomerRegisterForm(request.POST, request.FILES)
        if create_form.is_valid():
            user = create_form.save()
           
            # Redirect to the login page or home page as needed
            return redirect('login')
        else:
            print(create_form.errors)
    else:
        create_form = CustomerRegisterForm()
    
    context = {'createform': create_form}
    return render(request, "signup.html", context)


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, "signin.html")


from .forms import ProfileUpdateForm


def view_profile(request):
    user = request.user
    orders = Order.objects.filter(email=user.email)  # Filter orders by the user's email or other identifier

    context = {
        'user': user,
        'orders': orders
    }
    return render(request, 'profile_view.html', context)
@login_required
def profile_view_update(request):
    user = request.user
    orders = Order.objects.filter(email=user.email)  # Filter orders by the user's email or other identifier

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile page after saving
    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        'form': form,
        'orders': orders
    }
    return render(request, 'profile.html', context)

@login_required(login_url="login")
def userlist(request):
    
    user_list = CustomUser.objects.filter(~Q(username=request.user.username) & ~Q(is_superuser=True) & Q(is_active=True))
    # user_list = CustomUser.objects.filter(username=request.user.username)
    # user_list = CustomUser.objects.exclude(Q(username=request.user.username) & Q(request.user.is_superuser))
    if request.user.user_type_id == 1 or request.user.is_superuser:

    
        context = {"userlist": user_list}
    else:
        return HttpResponse('you are not allowed')
    
    return render(request, "userlist.html", context)

@login_required(login_url="login")
def userlist(request):
    
    user_list = CustomUser.objects.filter(~Q(username=request.user.username) & ~Q(is_superuser=True) & Q(is_active=True))
    if request.user.user_type_id == 1 or request.user.is_superuser:

    
        context = {"userlist": user_list}
    else:
        return HttpResponse('you are not allowed')
    
    return render(request, "userlist.html", context)


def det(request):
    empdet = [
        {'Name': 'MATT MONROE ', 'Age': '88', 'Course': 'PYTHON '},
        {'Name': 'JAMES COOPER ', 'Age': '68', 'Course': 'JAVA '},
        {'Name': 'CATE HOLMES ', 'Age': '52', 'Course': 'AUTOMOTIVE '},
    ]
    context = {'empdet': empdet}
    return render(request, "det.html", context)




def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user  # Assuming the user is authenticated
            product.save()
            return redirect('/add-product/')

    else:
        form = ProductForm()

    queryset = Product.objects.all()

    # Search functionality using form instead of direct request.GET
    if request.GET.get('search'):
        form = ProductForm(request.GET)  # Populate the form with GET data
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data['name']
            )

    context = {'prod': queryset, 'form': form}
    return render(request, 'addproduct.html', context)

def men_pro_list(request):
    men_product=Product.objects.all().filter(category=1)
    context={
        'MEN':men_product
    }
    return render(request,'menprod.html',context)


def women_pro_list(request):
    women_product=Product.objects.all().filter(category=2)
    context={
        'WOMEN':women_product
    }
    return render(request,'womenprod.html',context)

def cos_and_access(request):
    cosacc=Product.objects.all().filter(category=3)
    context={
        'cosacc':cosacc
    }
    return render(request,'cosacc.html',context)

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                       user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')
 

def delete_product(request, id):
    queryset = Product.objects.get(id=id)
    queryset.delete()
    return redirect('/add-product/')


def update_product(request, id):
    queryset = Product.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        product_image = request.FILES.get('image')
        product_name = data.get('name')
        product_details = data.get('description')

        queryset.image = product_image
        queryset.name = product_name
        queryset.description = product_details  # Fixed here
        queryset.save()
        return redirect('/add-product/')

    context = {'product': queryset}
    return render(request, 'update.html', context)


def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            
            product = form.save(commit=False)
            product.created_by = request.user  # Assuming the user is authenticated
            product.save()
            return redirect('/add-product/')

    else:
        form = OrderForm()

    queryset = Order.objects.all()    
    context = {'prod': queryset, 'form': form}
    return render(request, 'orderform.html', context)



def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
