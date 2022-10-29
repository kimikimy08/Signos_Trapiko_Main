from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from twilio.rest import Client
import random
from django.core.exceptions import PermissionDenied
from .forms import UserForm, MemberForm
from .utils import send_verfication_email, send_sms, detectUser
from incidentreport.models import IncidentGeneral




def check_role_member(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
# Restrict the customer from accessing the vendor page
def check_role_admin(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_super(user):
    if user.role == 3:
        return True
    else:
        raise PermissionDenied

def check_role_super_admin(user):
    if user.role == 2 or user.role == 3:
        return True
    else:
        raise PermissionDenied
    
    
# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect ('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        m_form = MemberForm(request.POST, request.FILES)
        try:
            if form.is_valid() and m_form.is_valid():
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']
                user = User.objects.create_user(first_name=first_name, middle_name=middle_name, last_name=last_name, username=username, email=email, mobile_number=mobile_number)
                user.set_password(password)
                user.role = User.MEMBER
                user.save()
                member = m_form.save(commit=False)
                member.user = user
                member.save()
                
            
                # send verification email
                mail_subject = 'Please Activate Your Account'
                email_template = 'emails/account_verification_email.html'
                send_verfication_email(request, user, mail_subject, email_template)
                messages.success(request, 'You have signed up successfully! Please check your email to verify your account.')
                print(user.password)
                return redirect('login')
            
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))
                #return redirect('register')
        else:
            print('invalid form')
            print(form.errors)
            print(form.non_field_errors)
    else:
        form = UserForm()
        m_form = MemberForm()
    context = {
        'form' : form,
        'm_form' : m_form,
    }
    return render(request, 'pages/registration.html', context)

def activate(request, uidb64, token):
    # Activate the userr by setting the is_active status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.status = User.ACTIVE
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('login')

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect ('myAccount')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('myAccount')
            #request.session['pk'] = user.pk
            #return redirect('verify_view')
        else:
            messages.error(request, 'Username and Password do not match.')
            return redirect('login')
        
    return render(request, 'pages/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out.")
    return redirect('login')

@login_required(login_url = 'login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def member_dashboard(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(user=request.user).order_by('-created_at')
    incidentReports_top = IncidentGeneral.objects.filter(user=request.user).order_by('-created_at')[:4]
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
        'incidentReports_top': incidentReports_top,
    }
    return render(request, 'pages/member/member_profile.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_dashboard(request):
    return render(request, 'pages/a_Dashboard.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def superadmin_dashboard(request):
    return render(request, 'pages/sa_Dashboard.html')



