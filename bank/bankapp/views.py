from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "index.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dataform')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid credentials")  # Use messages.error for clarity
            return redirect('login')
    return render(request, 'login.html')  # Use a separate login template


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('register')
    return render(request, "register.html")


@login_required  # Require login to access this view
def logout(request):
    auth.logout(request)
    return redirect('home')  # Redirect to the home page after logout


def dataform(request):
    return render(request, 'dataform.html')


def test(request):
    return render(request, 'test.html')
