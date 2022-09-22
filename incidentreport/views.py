from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member
from incidentreport.models import IncidentReport
from django.contrib import messages

@login_required(login_url = 'login')

@user_passes_test(check_role_super)
def user_reports(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = IncidentReport.objects.all()
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def user_reports_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 1)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def user_reports_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 2)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def user_reports_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 3)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@user_passes_test(check_role_admin)
def user_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = IncidentReport.objects.all()
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def user_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 1)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def user_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 2)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def user_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 3)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 1, user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 2, user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_member)
def my_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentReport.objects.filter(status = 3, user = request.user)
    context = {
        'profile': profile,
        'incidentReports' : incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)

def my_report_delete(request, incident_id=None):
    incidentReports = IncidentReport.objects.get(pk=incident_id)
    incidentReports.delete()
    return redirect('my_report')
    