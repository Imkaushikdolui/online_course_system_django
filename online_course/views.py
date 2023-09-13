from django.shortcuts import render,redirect
from online_course.forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.http import Http404 
from django.shortcuts import get_object_or_404

from django.core.mail import send_mail
from online_course.settings import EMAIL_HOST_USER
from accounts.models import Account , Profile

import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.models import Student,Teacher
from django.contrib.auth.views import PasswordResetView , PasswordResetConfirmView

# from .forms import CustomPasswordResetForm
from django.urls import reverse_lazy
from django.contrib import messages
import uuid
from django.contrib.auth import get_user_model
from online_course.tasks import send_mail_celery

#  user registration -->
@csrf_exempt
def Otpverify(request):
    if request.method == 'POST':
        userotp = request.POST.get('otp')
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print("OTP:",userotp)
        if password1 == password2:
            form  = Account.objects.create_user(
                name = name,
                email = email,
                username = username,
                role = role,
                password = password1
            )
            if role == 'teacher':
                teacher = Teacher.objects.create(
                    teacher_id=form,
                    name = name
                )
                teacher.save()
            elif role == 'student':
                student = Student.objects.create(
                    student_id=form,
                    name = name
                )
                student.save()
            form.save()
    return JsonResponse({'otp' : 'otp'}, status=200 )

def Signup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if form.is_valid():
            otp = random.randint(1000,9999)
            print("form is saved successfully")
            # send_mail("TWO FACTOR AUTHENTICATION: ",f"VERIFY YOUR MAIL USING THIS OTP: {otp}",EMAIL_HOST_USER,[email],fail_silently=True)
            send_mail_celery.delay("TWO FACTOR AUTHENTICATION: ",f"VERIFY YOUR MAIL USING THIS OTP: {otp}",EMAIL_HOST_USER,[email],fail_silently=True)
            print("email sended successfully")
            context = {
                'name' : name,
                'email' : email,
                'username' : username,
                'role': role,
                'password1' : password1,
                'password2' : password2,
                'otp' : otp
            }
            return render(request, 'template/OTPverify.html' ,context)
        else:
            print("some error has occured")
    context= {
            'form': form
    }
    return render(request, 'signup.html', context)


# user login -->
@csrf_exempt
def LoginOtpVerify(request):
    
    if request.method == 'POST':
        userotp = request.POST.get('otp')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = authenticate(request,email=email, password=password)
        print("OTP:",userotp)
        print(user)
        if user is not None:
            login(request,user)
            print("login done")
            return redirect("base:welcome")
        else:
            print("login failed")

    return JsonResponse({'otp' : 'otp'}, status=200 )


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)
            email = user.email
            role = user.role
            print(f'{password} {email} {role}')
        except Account.DoesNotExist:
            print("user does not exist")

        user = authenticate(request,email=email, password=password)
        print(user)
        if user is not None:
            otp = random.randint(1000,9999)
            print("form is saved successfully")
            # send_mail("TWO FACTOR AUTHENTICATION: ",f"LOGIN USING THIS OTP: {otp}",EMAIL_HOST_USER,[email],fail_silently=True)
            send_mail_celery.delay("TWO FACTOR AUTHENTICATION: ",f"LOGIN USING THIS OTP: {otp}",EMAIL_HOST_USER,[email])
            print("email sended successfully")
            context = {
                    'otp' : otp,
                    'email' : email,
                    'password' : password,
                    'role': role
                }
            return render(request,'template/LoginOtpVerify.html' ,context)
        else:
            print("Invalid Entry")
    
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    print("logout done")
    return redirect('/login')


def ChangePassword(request, token):
    context = {}
    try:
        # Attempt to retrieve the profile associated with the token
        profile_obj = get_object_or_404(Profile, forget_password_token=token)

        if request.method == "POST":
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            user_id = request.POST.get("user_id")

            if user_id is None:
                messages.error(request, "No user id found")
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.error(request, "Both passwords do not match")
                return redirect(f'/change-password/{token}/')

            user_obj = profile_obj.user
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

        context = {
            'user_id': profile_obj.user.id
        }

    except Http404:
        messages.error(request, "Profile not found. Please request a new password reset.")
        return redirect('/forget-password/')  # Redirect to the password reset page

    except Exception as e:
        print(e)
        messages.error(request, "An error occurred while processing your request. Please try again.")
    
    return render(request, 'change-password.html', context)

def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Click on the link to reset your password: http://127.0.0.1:8000/change-password/{token}/'
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail_celery.delay(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(e)
        return False
    
def ForgetPassword(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email') 
            print(email)
            
            user_obj = Account.objects.filter(email=email).first()
            
            if not user_obj:
                messages.error(request, 'No user found with this email address')
                return redirect('/forget-password/') 
            
            # Generate a new token for each password reset request
            token = str(uuid.uuid4())
            
            try:
                # Check if the user already has a profile
                profile_obj = user_obj.profile
                profile_obj.forget_password_token = token  # Update the existing profile with the new token
            except Profile.DoesNotExist:
                # If the user doesn't have a profile, create a new one
                profile_obj = Profile(user=user_obj, forget_password_token=token)
            profile_obj.save()
                
            # Print the token for debugging purposes
            print(f"Token generated for {user_obj.username}: {token}")
                
            if send_forget_password_mail(email, token):
                messages.success(request, 'An email has been sent with a link to reset your password')
                print('Email has been sent')
            else:
                messages.error(request, 'Failed to send the email. Please try again later.')
                print('Failed to send the email')
            
            return redirect('/forget-password/') 
        except Exception as e:
            print(e)
            
    return render(request, 'forget-password.html')