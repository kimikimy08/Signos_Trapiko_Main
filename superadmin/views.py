from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_super
from django.contrib import messages
from accounts.forms import UserForm, MemberForm, UserFormAdmin
from accounts.utils import send_verfication_email, send_sms, detectUser
from django.urls import reverse

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
    }
    
    return render(request, 'pages/super_profile.html', context)