from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_member
from accounts.forms import MemberForm, UserUpdateForm
from django.contrib import messages

# Create your views here.
@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def member_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
    }
    return render(request, 'pages/member_profile.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def member_profile_edit(request):
    user = User.objects.get(username = request.user.username)
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile_form = MemberForm(request.POST  or None, request.FILES  or None, instance=profile)
        user_form = UserUpdateForm(request.POST  or None, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.instance.username = request.user
            # user.first_name = user_form.cleaned_data['first_name']
            # user.middle_name = user_form.cleaned_data['middle_name']
            # user.last_name = user_form.cleaned_data['last_name']
            # user.username = user_form.cleaned_data['username']
            # user.email = user_form.cleaned_data['email']
            # user.mobile_number = user_form.cleaned_data['mobile_number']
            # my_form = user_form.save(commit=False)
            # my_form.username = request.user.username
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile updated')
            return redirect('member_profile')
        else:
            print(profile_form.errors)
            print(user_form.errors)

    else:
        profile_form = MemberForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user, initial={"email": user.email, 
                                                        "username": user.username})
    context = {
        'profile_form': profile_form,
        'user_form' : user_form,
        'profile': profile,
    }
    
    return render(request, 'pages/member_profile_edit.html', context)