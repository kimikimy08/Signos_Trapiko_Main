from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_super
from django.contrib import messages
from accounts.forms import UserForm, MemberForm, UserManagementForm
from accounts.utils import send_verfication_email, send_sms, detectUser
from django.urls import reverse
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
    }
    
    return render(request, 'pages/super_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account(request):
    form = UserManagementForm(request.POST)
    m_form = MemberForm(request.POST, request.FILES)
    user = User.objects.all()
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    print(context)
    return render(request, 'pages/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_member(request):
    user = User.objects.filter(role = 1)
    form = UserManagementForm(request.POST)
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    print(context)
    return render(request, 'pages/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_admin(request):
    user = User.objects.filter(role = 2)
    form = UserManagementForm(request.POST)
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    print(context)
    return render(request, 'pages/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_superadmin(request):
    user = User.objects.filter(role = 3)
    form = UserManagementForm(request.POST)
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'form': form,
        'user': user,
        'page_obj':page_obj
    }
    return render(request, 'pages/super_user_account.html', context)

def super_user_account_add(request):
    if request.method == 'POST':
        form = UserManagementForm(request.POST)
        try:
            if form.is_valid():
                
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                mobile_number = form.cleaned_data['mobile_number']
                password = form.cleaned_data['password']
                role = request.POST['role']

                user = User(first_name=first_name, middle_name=middle_name, last_name=last_name, username=username, email=email, mobile_number=mobile_number, password=password, role=role)
                user.save()
            
                # send verification email
                mail_subject = 'Please Activate Your Account'
                email_template = 'emails/account_verification_email.html'
                send_verfication_email(request, user, mail_subject, email_template)
                messages.success(request, 'You have signed up successfully! Please check your email to verify your account.')
                print(user.password)
                return redirect('super_user_account')
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_account_delete(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.role == 1 or user.role == 2:
        user.delete()
        return redirect('super_user_account')
    else:
        messages.error(request, 'Unable to Delete Super Admin')
        return redirect('super_user_account')