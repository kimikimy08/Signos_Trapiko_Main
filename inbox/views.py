from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_member, check_role_super
from accounts.models import UserProfile, User 
from .forms import SentMessage
from django.contrib import messages
from .models import Sent
from accounts.utils import send_verfication_email, send_sms, detectUser
from django.views.decorators.cache import cache_control

# Create your views here.
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sent_message(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = SentMessage(request.POST or None, request.FILES or None)
        try:
            if form.is_valid():
                form.user = request.user
                to_email = request.POST.get('to_email')
                subject = request.POST.get('subject')
                message = request.POST.get('message')
                
                if User.objects.filter(email = to_email).exists():
                    user_from = User.objects.get(email__exact=request.user.email)
                    user = User.objects.get(email__exact=to_email)
                    
                # to_email = form.cleaned_data['to_email']
                # subject = form.cleaned_data['subject']
                # message = form.cleaned_data['message']

                    sent_email_message = Sent(user=request.user, to_email=to_email, subject=subject, message=message)
                    sent_email_message.save()
                    
                    mail_subject = str(request.user) + ' just sent you a message in Signos Trapiko'
                    email_template = 'emails/notification_receive.html'
                    send_verfication_email(request, user, mail_subject, email_template, user_from)
                    
                    messages.success(request, 'Message sent successfully')
                    
                
                else:
                    messages.warning(request, 'Email does not exists in the system')
            
                # # send verification email
                # mail_subject = 'Please Activate Your Account'
                # email_template = 'emails/account_verification_email.html'
                # send_verfication_email(request, user, mail_subject, email_template)
                # messages.success(request, 'You have signed up successfully! Please check your email to verify your account.')
                # print(user.password)
                return redirect('sent_message')
            else:
                print(form.errors)
                print(form.non_field_errors)
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = SentMessage()
    context = {
        'form' : form,
    }
    return render(request, 'pages/inbox/sent_message.html', context)

