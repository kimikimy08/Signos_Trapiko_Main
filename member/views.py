from django.shortcuts import render, get_object_or_404
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_member

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def member_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'pages/member_profile.html', context)