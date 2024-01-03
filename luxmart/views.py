from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
# C:\Users\User\python_projects\django_projects
from django.http import HttpResponse

from django.shortcuts import render


def compare_lists(request):
    li1 = ['(GSTIN(O1) : 1890107200253)', '(EXP(17) : Aug 15, 2015)',
           '(Batch No(10) : RNBXY0614)', '(S.No(21) : 15892152002)']
    li2 = [
        'ORO\n\nGSTIN(O1) : 1890107200253\nEXP(17) : Aug 15, 2017\n\nBatch No(10) : RNBXY0614\nS.No(21) : 15892152002\n']
    li3 = [
        'ORO\n\nGSTIN(O1) : 1890107200253\nEXP(17) : Aug 15, 2015\n\nBatch No(10) : RNBXY0614\nS.No(21) : 15892152002\n']
    li4 = [
        'OROqugs\n\nGSTIN(O1) : 1890107200253\nEXP(17) : Aug 15, 2017\n\nBatch No(10) : RNBXY0614\nS.No(21) : 15892002\n']
    lists_to_compare = [li2, li3, li4]

    result = 'Success'
    for li in lists_to_compare:
        # Extract column names and values from the inspection list
        column_values_ins = {}
        for entry in li:
            columns = entry.split(':')
            column_name = columns[0].strip()
            column_value = columns[1].strip()
            column_values_ins[column_name] = column_value

        # Filter data in the database list based on column names
        filter_data = [entry for entry in li1 if entry.split(
            ':')[0].strip() in column_values_ins]

        # Compare the filtered data with the inspection list
        if filter_data != li:
            result = 'Unsuccessful'
            break

    return render(request, 'compare.html', {'result': result})


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


def car(request):
    if request.method == 'POST':
        data = request.POST
        car_image = request.FILES.get('car_image')
        car_name = data.get('car_name')
        car_details = data.get('car_details')

        Car.objects.create(
            car_image=car_image,
            car_name=car_name,
            car_details=car_details,
        )
        return redirect('/card/')

    queryset = Car.objects.all()
    # for search cars

    if request.GET.get('search'):
        queryset = queryset.filter(
            car_name__icontains=request.GET.get('search'))
    # done search funtion

    context = {'cardeta': queryset}

    return render(request, 'car.html', context)


def delete_car(request, id):
    queryset = Car.objects.get(id=id)
    queryset.delete()
    return redirect('/card/')


def update_car(request, id):
    queryset = Car.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        car_image = request.FILES.get('car_image')
        car_name = data.get('car_name')
        car_details = data.get('car_details')

        queryset.car_image = car_image
        queryset.car_name = car_name
        if car_image:
            queryset.car_details = car_details
        queryset.save()
        return redirect('/card/')

    context = {'cars': queryset}
    return render(request, 'update.html', context)
