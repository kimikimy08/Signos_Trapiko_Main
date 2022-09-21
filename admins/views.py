from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.forms import UserForm, MemberForm, UserManagementForm

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'pages/admin_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_account(request):
    form = UserManagementForm(request.POST)
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
    return render(request, 'pages/admin_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_account_member(request):
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
    return render(request, 'pages/admin_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_account_admin(request):
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
    return render(request, 'pages/admin_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_account_superadmin(request):
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
    return render(request, 'pages/admin_user_account.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_account_delete(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.role == 1 or user.role == 2:
        user.delete()
        return redirect('admin_user_account')
    else:
        messages.error(request, 'Unable to Delete Super Admin')
        return redirect('admin_user_account')