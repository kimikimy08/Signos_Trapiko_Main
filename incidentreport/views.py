from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member
from incidentreport.models import UserReport, IncidentGeneral
from django.contrib import messages
from .forms import UserReportForm, IncidentGeneralForm

@login_required(login_url = 'login')

@user_passes_test(check_role_super)
def user_reports(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = UserReport.objects.all()
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def user_reports_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 1)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def user_reports_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 2)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def user_reports_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 3)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@user_passes_test(check_role_admin)
def user_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = UserReport.objects.all()
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def user_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 1)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def user_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 2)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def user_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 3)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 1, user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 2, user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status = 3, user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

def my_report_delete(request, incident_id=None):
    incidentReports = UserReport.objects.get(pk=incident_id)
    incidentReports.delete()
    return redirect('my_report')

@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_add(request):
    
    form = UserReportForm(request.POST, request.FILES)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        User.objects.get(pk=request.user.pk)
        if form.is_valid():
            date=request.POST['date']
            time=request.POST['time']
            location=request.POST['location']
            description=request.POST['description']
            
            
            upload_photovideo=request.FILES.get('upload_photovideo')
            status = 1
            # user_report = form.save(commit=False)
            # user_report.user = get_user(request)
            # user_report.save()
            obj=UserReport.objects.create(user_id=request.user.pk, date=date, time=time, location=location,description=description,upload_photovideo=upload_photovideo, status=status)
            obj.save()
            messages.success(request, 'User Report added successfully!')
            return redirect('my_report')
        
        else:
            print(form.errors)

    else:
        form = UserReportForm()
    context = {
        'form': form,
        'profile': profile,

    }
    return render(request, 'pages/member_myreport_add.html', context)

def my_report_view(request, id):
    user_report = get_object_or_404(UserReport, pk=id)
    context = {
        'user_report': user_report,
    }

    return render(request, 'pages/member_myreport_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_edit(request, id):
    user_report = get_object_or_404(UserReport, pk=id)
    if request.method == 'POST':
        form = UserReportForm(request.POST or None, request.FILES or None, instance=user_report)
        if form.is_valid():
            form.save()
            return redirect('my_report')
    else:
        form = UserReportForm(instance=user_report)
    context = {
        'form': form,
        'user_report': user_report,
    }
    return render(request, 'pages/member_myreport_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_delete(request, id):
    user_report = get_object_or_404(UserReport, pk=id)
    user_report.delete()
    return redirect('my_report')

def incident_report_general(request):
    if request.method == 'POST':
        user_report_form = UserReportForm(request.POST, request.FILES)
        inc_gen_form = IncidentGeneralForm(request.POST, request.FILES)
        
    else:
        user_report_form = UserReportForm()
        inc_gen_form = IncidentGeneralForm()
    context = {
        'user_report_form': user_report_form,
        'inc_gen_form': inc_gen_form,
    }
    return render(request, 'pages/incident_report.html', context)


