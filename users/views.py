from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        confirm_password = request.POST.get('confirm_password','')


        if password != confirm_password:
            messages.error(request,"Password do not match")
            return render(request, 'users/signup.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already Exists")
            return redirect('users:signup')
        
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)

            #for remembering, when an error occured
            return render(request, 'users/signup.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            })
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
            )
        user.save()
        auth_login(request,user)
        # messages.success(request,"Account created Successfully!")
        return redirect('web:home')
    
    return render(request,'users/signup.html')




def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,username=email,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('web:index')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('users:login')
        
    return render(request,'users/login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('users:login')





