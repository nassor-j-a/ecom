from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout

# This is for messages in the login_user function
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms

# Create your views here.


def home(request):
    products = Product.objects.all()

    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})

def search(request):
    return render(request, 'search.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in...Welcome"))
            return redirect('home')
        else:
            messages.error(request, ("Invalid username or password"))
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(
        request, ("You have been logged out...Thanks for stopping by"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form, cleaned_data['username']
            password = form, cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ("Username created - Please Fill Out Your User Info Below..."))
            return redirect('update_info')
        else:
            messages.success(
                request, ("There wa aproblem registering, please try again!!!"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        # Did they fill out the form
        if request.method == 'POST':
            # Do stuff
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request,  'Your Password Has Been Updated...')
                login(request, current_user)
                return redirect('update_password')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
            
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form' : form})
    else:
        messages.success(request, "You must be must be logged In to access that page !!!")
        return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Has Been Updated!!!")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form' : user_form})
    else:
        messages.success(request, "You must be must be logged In to access that page !!!")
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()

            messages.success(request, "Your Info Has Been Updated!!!")
            return redirect('home')
        return render(request, 'update_info.html', {'form' : form})
    else:
        messages.success(request, "You must be must be logged In to access that page !!!")
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, foo):
    # Replace hyphens with spaces
    foo = foo.replace('-', ' ')
    # Grab the category from the url
    try:
        # look up the category
        category = Category.objects.get(name=foo)
        # get all the products in that category
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'foo': foo, 'products': products, 'category': category})
    except:
        messages.success(
                request, ("That Category doesn't exist!!!"))
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})