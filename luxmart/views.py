from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect
from .models import Product,CartItem,Order
from .forms import ProductForm,OrderForm

# Create your views here.
# C:\Users\User\python_projects\django_projects
from django.http import HttpResponse

from django.shortcuts import render




@login_required(login_url="login")
def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            my_user = User.objects.create_user(username, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, "signup.html")


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
    return render(request,'womenprod.html')

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
        if product_image:
            queryset.description = product_details
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