from django.shortcuts import redirect, render

from inbox.models import Notification

# Create your views here.

def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)
    extra_id = request.GET.get('extra_id', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('user_reports', application_id=notification.extra_id)
        elif notification.notification_type == Notification.APPLICATION:
            return redirect('user_reports', application_id=notification.extra_id)
    
    return render(request, 'notification/notifications.html')
