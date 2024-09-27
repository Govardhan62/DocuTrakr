from django.shortcuts import render, redirect
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Sign-up view
@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
            return redirect('signup')
        
        # Create a new user if the username is available
        user = User.objects.create_user(username=username, password=password, first_name=first_name)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')

# Login view
@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('process_document')  # Redirect to your home page or dashboard
        else:
            messages.error(request, "You are not authorized. Check your credentials.")
            return redirect('login')
    
    return render(request, 'login.html')

# Logout view (optional for a complete flow)
from django.contrib.auth import logout

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')  # Redirect to the login page
