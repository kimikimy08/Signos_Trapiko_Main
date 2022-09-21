from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin
from django.contrib import messages

# Create your views here.
@login_required(login_url = 'signin')
@user_passes_test(check_role_admin)
def admin_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'pages/admin_profile.html', context)