import csv
import os
from django.conf import settings
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member, check_role_super_admin
from incidentreport.models import  IncidentGeneral, IncidentRemark, IncidentMedia, IncidentPerson, IncidentVehicle, AccidentCausation, CollisionType, CrashType
from django.contrib import messages

from .forms import IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm, AccidentCausationForm,  CollisionTypeForm, CrashTypeForm
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.forms.models import construct_instance
from datetime import datetime
from .resources import IncidentGeneraltResource, IncidentRemarkResources, IncidentPeopleResources, IncidentVehicleResources
from tablib import Dataset
from django.core.paginator import Paginator
import pandas as pd


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentGeneral = IncidentGeneral.objects.all().order_by('-updated_at')
    paginator = Paginator(incidentGeneral, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentGeneral:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentGeneral': page_obj,
        # 'IncidentGeneral': IncidentGeneral
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    # incidentReports = IncidentGeneral.objects.filter(user_report__status = 1).order_by('-updated_at')
    incidentGeneral = IncidentGeneral.objects.filter(status = 1).order_by('-updated_at')
    paginator = Paginator(incidentGeneral, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentGeneral:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentGeneral': page_obj,
        'IncidentGeneral': IncidentGeneral
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentGeneral = IncidentGeneral.objects.filter(status = 2).order_by('-updated_at')
    paginator = Paginator(incidentGeneral, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentGeneral:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentGeneral': page_obj,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentGeneral = IncidentGeneral.objects.filter(status = 3).order_by('-updated_at')
    paginator = Paginator(incidentGeneral, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentGeneral:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentGeneral': page_obj,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_today(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    today = datetime.today().date()
    incidentReports = IncidentGeneral.objects.filter(created_at__date=today).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.user_report_id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.user_report_id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_report_delete(request, id=None):
    incidentReports = get_object_or_404(IncidentGeneral, id=id)
    #user_report = IncidentGeneral.objects.all()
    incidentReports.delete()
    return redirect('user_reports')



@user_passes_test(check_role_admin)
def user_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = IncidentGeneral.objects.all().order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.user_report_id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.user_report_id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def user_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(user_report__status = 1).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.user_report_id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.user_report_id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def user_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(user_report__status = 2).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.user_report_id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.user_report_id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def user_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(user_report__status = 3).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.user_report_id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.user_report_id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_report_today(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    today = datetime.today().date()
    incidentReports = IncidentGeneral.objects.filter(created_at__date=today).order_by('-updated_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.user_report_id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.user_report_id)
                b.delete()
                messages.success(request, 'User Report successfully deleted')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(incidentReports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in incidentReports:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = IncidentGeneral.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Report details successfully deleted')
        return redirect('my_report')
    context = {
        'profile': profile,
        'incidentReports': page_obj,
    }
    return render(request, 'pages/member/member_myreport.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=1, user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member/member_myreport.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=2, user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member/member_myreport.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=3, user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member/member_myreport.html', context)


# def my_report_delete(request, incident_id=None):
#     incidentReports = IncidentGeneral.objects.get(pk=incident_id)
#     incidentReports.delete()
#     return redirect('my_report')


# @login_required(login_url='login')
# @user_passes_test(check_role_member)
# def my_report_add(request):

#     form = IncidentGeneralForm(request.POST, request.FILES)
#     profile = get_object_or_404(UserProfile, user=request.user)

#     if request.method == 'POST':
#         User.objects.get(pk=request.user.pk)
#         if form.is_valid():
#             date = request.POST['date']
#             time = request.POST['time']
#             address = request.POST['address']
#             description = request.POST['description']
            
            

#             upload_photovideo = request.FILES.get('upload_photovideo')
#             status = 1
#             # user_report = form.save(commit=False)
#             # user_report.user = get_user(request)
#             # user_report.save()
#             obj = IncidentGeneral.objects.create(user_id=request.user.pk, date=date, time=time, address=address,
#                                             description=description, upload_photovideo=upload_photovideo, status=status)
#             obj.save()
#             messages.success(request, 'User Report added successfully!')
#             return redirect('my_report')

#         else:
#             print(form.errors)

#     else:
#         form = IncidentGeneralForm()
#     context = {
#         'form': form,
#         'profile': profile,

#     }
#     return render(request, 'pages/member_myreport_add.html', context)


def my_report_view(request, id):
    user_report = get_object_or_404(IncidentGeneral, pk=id)
    context = {
        'user_report': user_report,
    }

    return render(request, 'pages/member/member_myreport_view.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_edit(request, id):
    user_report = get_object_or_404(IncidentGeneral, pk=id)
    if request.method == 'POST':
        form = IncidentGeneralForm1(request.POST or None,
                              request.FILES or None, instance=user_report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report details successfully updated')
            return redirect('my_report')
        
    else:
        form = IncidentGeneralForm1(instance=user_report)
        # messages.error(request, 'Report details unsuccessfully updated')
    context = {
        'form': form,
        'user_report': user_report,
    }
    return render(request, 'pages/member/member_myreport_edit.html', context)




@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_delete(request, id):
    user_report = get_object_or_404(IncidentGeneral, pk=id)
    incident_general = get_object_or_404(IncidentGeneral, pk=id)
    incident_remark = get_object_or_404(IncidentRemark, pk=id)
    incident_remark.delete()
    incident_general.delete()
    user_report.delete()
    messages.success(request, 'Report details successfully deleted')
    return redirect('my_report')


def incident_report_general(request):
    if request.method == 'POST':
        user_report_form = IncidentGeneralForm(request.POST, request.FILES)
        inc_gen_form = IncidentGeneralForm(request.POST, request.FILES)

    else:
        user_report_form = IncidentGeneralForm()
        inc_gen_form = IncidentGeneralForm()
    context = {
        'user_report_form': user_report_form,
        'inc_gen_form': inc_gen_form,
    }
    return render(request, 'pages/incident_report_general.html', context)

def incident_report_people(request):
    if request.method == 'POST':
        user_report_form = IncidentGeneralForm(request.POST, request.FILES)
        person_instance = IncidentPersonForm(request.POST, request.FILES)
        obj = get_object_or_404(UserProfile, pk=request.id)
        try:
            if person_instance.is_valid():
                incident_first_name = person_instance.cleaned_data['incident_first_name']
                incident_middle_name = person_instance.cleaned_data['incident_middle_name']
                incident_last_name = person_instance.cleaned_data['incident_last_name']
                incident_age = person_instance.cleaned_data['incident_age']
                incident_gender = person_instance.cleaned_data['incident_gender']
                incident_address = person_instance.cleaned_data['incident_address']
                incident_id_presented = person_instance.cleaned_data['incident_id_presented']
                incident_id_number = person_instance.cleaned_data['incident_id_number']
                incident_injury = person_instance.cleaned_data['incident_injury']
                incident_driver_error = person_instance.cleaned_data['incident_driver_error']
                incident_alcohol_drugs = person_instance.cleaned_data['incident_alcohol_drugs']
                incident_seatbelt_helmet = person_instance.cleaned_data['incident_seatbelt_helmet']
            
            else:
                model = IncidentPerson(incident_general=obj, incident_first_name=incident_first_name,
                                                    incident_middle_name=incident_middle_name,
                                                    incident_last_name=incident_last_name,
                                                    incident_age=incident_age,
                                                    incident_gender=incident_gender,
                                                    incident_address=incident_address,
                                                    incident_id_presented=incident_id_presented,
                                                    incident_id_number=incident_id_number,
                                                    incident_injury=incident_injury,
                                                    incident_driver_error=incident_driver_error,
                                                    incident_alcohol_drugs=incident_alcohol_drugs,
                                                    incident_seatbelt_helmet=incident_seatbelt_helmet)
                model.save()
                messages.success(request, 'Accident Factor Added')
                return redirect('attributes_builder_accident')
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))
            
    else:
        user_report_form = IncidentGeneralForm()
        person_instance = IncidentPersonForm()
        print(user_report_form.errors)
        print(person_instance.errors)
        
    context = {
        'user_report_form': user_report_form,
        'person_instance': person_instance,
        
    }
    return render(request, 'pages/super/incident_report_people.html', context)

   
    
def incident_report_vehicle(request):
    if request.method == 'POST':
        user_report_form = IncidentGeneralForm(request.POST, request.FILES)
        inc_veh_form = IncidentVehicleForm(request.POST, request.FILES)

    else:
        user_report_form = IncidentGeneralForm()
        inc_veh_form = IncidentVehicleForm()
        print(user_report_form.errors)
        print(inc_veh_form.errors)
        
    context = {
        'user_report_form': user_report_form,
        'inc_veh_form': inc_veh_form,
    }
    return render(request, 'pages/incident_report_vehicle.html', context)

def incident_report_media(request):
    if request.method == 'POST':
        user_report_form = IncidentGeneralForm(request.POST, request.FILES)
        inc_med_form = IncidentMediaForm(request.POST, request.FILES)

    else:
        user_report_form = IncidentGeneralForm()
        inc_med_form = IncidentMediaForm()
        print(user_report_form.errors)
        print(inc_med_form.errors)
        
    context = {
        'user_report_form': user_report_form,
        'inc_med_form': inc_med_form,
    }
    return render(request, 'pages/incident_report_media.html', context)

def incident_report_remarks(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
       
        inc_rem_form = IncidentRemarksForm(request.POST, request.FILES)

    else:
        inc_rem_form = IncidentRemarksForm()
        print(inc_rem_form.errors)
        
    context = {
        'profile': profile,
        'inc_rem_form': inc_rem_form,
    }
    return render(request, 'pages/incident_report_remarks.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_report_delete(request, id=None):
    incidentReports = get_object_or_404(IncidentGeneral, id=id)
    #user_report = IncidentGeneral.objects.all()
    incidentReports.delete()
    return redirect('user_reports')


# AJAX
# def load_accident(request):
#     accident_factor_id = request.GET.get('id_accident_factor')
#     collision_type_id = request.GET.get('id_collision_type')
#     context = {
#         'acc_subcat': acc_subcat,
#         'col_subcat': col_subcat
#     }
#     return render(request, 'incident/acc_sub_dropdown_list_options.html', context)
#     #return JsonResponse(list(acc_subcat.values('id', 'sub_category')), safe=False)

# def load_collision(request):
#     collision_type_id = request.GET.get('collision_type_id')
#     col_subcat = CollisionTypeSub.objects.filter(collision_type_id=collision_type_id).all()
#     #return render(request, 'incident/acc_sub_dropdown_list_options.html', {'acc_subcat': acc_subcat})
#     return JsonResponse(list(col_subcat.values('id', 'sub_category')), safe=False)


# FORMS = [("information", IncidentGeneralForm),
#         ("general", IncidentGeneralForm),
#         #  ("people", IncidentPersonForm),
#         #  ("vehicle",IncidentVehicleForm),
#         #  ("media", IncidentMediaForm),
#          ("remarks", IncidentRemarksForm)]

FORMS1 = [("information", IncidentGeneralForm)]

# TEMPLATES = {"information": "pages/super/incident_report_user.html",
#                 "general": "pages/super/incident_report_general.html",
#                 # "people": "pages/super/incident_report_people.html",
#                 # "vehicle": "pages/super/incident_report_vehicle.html",
#                 # "media": "pages/super/incident_report_media.html",
#                 "remarks": "pages/super/incident_report_remarks.html"}


# TEMPLATES1 = {"information": "pages/admin/incident_report_user.html",
#                 "general": "pages/admin/incident_report_general.html",
#                 # "people": "pages/admin/incident_report_people.html",
#                 # "vehicle": "pages/admin/incident_report_vehicle.html",
#                 # "media": "pages/admin/incident_report_media.html",
#                 "remarks": "pages/admin/incident_report_remarks.html"}

TEMPLATES2 = {"information": "pages/member/member_myreport_add.html"}


# class multistepformsubmission(SessionWizardView):


#     # template_name = 'pages/incident_report.html'
#     # form_list = [IncidentGeneralForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
#     file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    
#     def get_template_names(self):
#         return [TEMPLATES[self.steps.current]]
    
#     def done(self, form_list, **kwargs):
#         # IncidentGeneral, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
#         profile = get_object_or_404(UserProfile, user=self.request.user)
#         cleaned_data = [form.cleaned_data for form in form_list]
#         user_instance = IncidentGeneral()
#         general_instance = IncidentGeneral()
#         # person_instance  = IncidentPerson()
#         # vehicle_instance = IncidentVehicle()
#         # media_instance = IncidentMedia()
#         remarks_instance = IncidentRemark()
#         #listing_instance.created_by = self.request.user
#         #listing_instance.listing_owner = self.request.user
#         #listing_instance.listing_type = 'P'
#         for form in form_list:
#             user_instance = construct_instance(form, user_instance, form._meta.fields, form._meta.exclude)
#             general_instance = construct_instance(form, general_instance, form._meta.fields, form._meta.exclude)
#             # person_instance = construct_instance(form, person_instance, form._meta.fields, form._meta.exclude)
#             # vehicle_instance = construct_instance(form, vehicle_instance, form._meta.fields, form._meta.exclude)
#             # media_instance = construct_instance(form, media_instance, form._meta.fields, form._meta.exclude)
#             remarks_instance = construct_instance(form, remarks_instance, form._meta.fields, form._meta.exclude)
#         user_instance.user = self.request.user
#         user_instance.status = 2
#         user_instance.save()
#         general_instance.user_report = user_instance
#         general_instance.save()
#         # for form in cleaned_data[2]:
#             # incident_first_name = form.get('incident_first_name')
#             # incident_middle_name = form.get('incident_middle_name')
#             # incident_last_name = form.get('incident_last_name')
#             # incident_age = form.get('incident_age')
#             # incident_gender = form.get('incident_gender')
#             # incident_address = form.get('incident_address')
#             # incident_involvement = form.get('incident_involvement')
#             # incident_id_presented = form.get('incident_id_presented')
#             # incident_id_number = form.get('incident_id_number')
#             # incident_injury = form.get('incident_injury')
#             # incident_driver_error = form.get('incident_driver_error')
#             # incident_alcohol_drugs = form.get('incident_alcohol_drugs')
#             # incident_seatbelt_helmet = form.get('incident_seatbelt_helmet')
            
#             # data = IncidentPerson.objects.create(incident_first_name = incident_first_name,
#             #                                             incident_middle_name = incident_middle_name,
#             #                                             incident_last_name = incident_last_name,
#             #                                             incident_age = incident_age,
#             #                                             incident_gender = incident_gender,
#             #                                             incident_address = incident_address,
#             #                                             incident_involvement = incident_involvement,
#             #                                             incident_id_presented = incident_id_presented,
#             #                                             incident_id_number = incident_id_number,
#             #                                             incident_injury = incident_injury,
#             #                                             incident_driver_error = incident_driver_error,
#             #                                             incident_alcohol_drugs = incident_alcohol_drugs,
#             #                                             incident_seatbelt_helmet = incident_seatbelt_helmet,
#             #                                   )
#             # person_instance, created = data
#             # person_instance.clean()
#         # person_instance.incident_general = general_instance
#         # person_instance.save()
#         # vehicle_instance.incident_general = general_instance
#         # vehicle_instance.save()
#         # media_instance.incident_general = general_instance
#         # media_instance.save()
#         remarks_instance.incident_general = general_instance
#         remarks_instance.save()
#         context = {
#             'profile': profile
#         }
#         # return redirect('/incidentReport/people', context)
#         return redirect('/IncidentGenerals', context)

# class multistepformsubmission_admin(SessionWizardView):
    

#     # template_name = 'pages/incident_report.html'
#     # form_list = [IncidentGeneralForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
#     file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    
#     def get_template_names(self):
#         return [TEMPLATES1[self.steps.current]]
    
#     def done(self, form_list, **kwargs):
#         # IncidentGeneral, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
#         profile = get_object_or_404(UserProfile, user=self.request.user)
#         user_instance = IncidentGeneral()
#         general_instance = IncidentGeneral()
#         person_instance  = IncidentPerson()
#         vehicle_instance = IncidentVehicle()
#         media_instance = IncidentMedia()
#         remarks_instance = IncidentRemark()
#         #listing_instance.created_by = self.request.user
#         #listing_instance.listing_owner = self.request.user
#         #listing_instance.listing_type = 'P'
#         for form in form_list:
#             user_instance = construct_instance(form, user_instance, form._meta.fields, form._meta.exclude)
#             general_instance = construct_instance(form, general_instance, form._meta.fields, form._meta.exclude)
#             person_instance = construct_instance(form, person_instance, form._meta.fields, form._meta.exclude)
#             vehicle_instance = construct_instance(form, vehicle_instance, form._meta.fields, form._meta.exclude)
#             media_instance = construct_instance(form, media_instance, form._meta.fields, form._meta.exclude)
#             remarks_instance = construct_instance(form, remarks_instance, form._meta.fields, form._meta.exclude)
#         user_instance.user = self.request.user
#         user_instance.status = 2
#         user_instance.save()
#         general_instance.user_report = user_instance
#         general_instance.save()
        
#         person_instance.incident_general = general_instance
#         person_instance.save()
#         vehicle_instance.incident_general = general_instance
#         vehicle_instance.save()
#         media_instance.incident_general = general_instance
#         media_instance.save()
#         remarks_instance.incident_general = general_instance
#         remarks_instance.save()
#         context = {
#             'profile': profile
#         }
#         return redirect('/IncidentGenerals', context)
    
class multistepformsubmission_member(SessionWizardView):
    

    # template_name = 'pages/incident_report.html'
    # form_list = [IncidentGeneralForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'incident_report/image'))
    
    def get_template_names(self):
        return [TEMPLATES2[self.steps.current]]
    
    def form_valid(self, form):
        try:
            form.execute()
            # messages.add_message(self.request, messages.SUCCESS, ('Report details successfully added'))
            
            # messages.add_message(self.request, messages.SUCCESS)
        except Exception as err:
            messages.add_message(self.request, messages.ERROR, err.message)
        else:
            messages.add_message(self.request, messages.INFO, ('It worked'))
    
    def done(self, form_list, **kwargs):
        # IncidentGeneral, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
        profile = get_object_or_404(UserProfile, user=self.request.user)

        user_instance = IncidentGeneral()
        general_instance = IncidentGeneral()
        person_instance  = IncidentPerson()
        vehicle_instance = IncidentVehicle()
        media_instance = IncidentMedia()
        remarks_instance = IncidentRemark()
        #listing_instance.created_by = self.request.user
        #listing_instance.listing_owner = self.request.user
        #listing_instance.listing_type = 'P'
        for form in form_list:
            user_instance = construct_instance(form, user_instance, form._meta.fields, form._meta.exclude)
            general_instance = construct_instance(form, general_instance, form._meta.fields, form._meta.exclude)
            person_instance = construct_instance(form, person_instance, form._meta.fields, form._meta.exclude)
            vehicle_instance = construct_instance(form, vehicle_instance, form._meta.fields, form._meta.exclude)
            media_instance = construct_instance(form, media_instance, form._meta.fields, form._meta.exclude)
            remarks_instance = construct_instance(form, remarks_instance, form._meta.fields, form._meta.exclude)
        user_instance.user = self.request.user
        user_instance.status = 1
        user_instance.save()
        general_instance.user_report = user_instance
        general_instance.save()
        person_instance.incident_general = general_instance
        person_instance.save()
        vehicle_instance.incident_general = general_instance
        vehicle_instance.save()
        media_instance.incident_general = general_instance
        media_instance.save()
        remarks_instance.incident_general = general_instance
        remarks_instance.save()
        
        # Notification.objects.create(to_user=self.request, IncidentGeneral=self.user_report, notification_type='application', created_by=self.user, extra_id=general_instance.id)
        
        messages.success(self.request, 'Report details successfully added')
        context = {
            'profile': profile,
        
        }
        return redirect('/myReport', context)

@login_required(login_url='login')
@user_passes_test(check_role_member)
def incident_form_member(request):
    attWizardView = multistepformsubmission_member.as_view(FORMS1)
    return attWizardView(request)


# def incident_report_people_view(request, id):
#     general_instance = get_object_or_404(IncidentGeneral, pk=id)
#     #user_instance = IncidentGeneral.objects.all()
#     user_report = IncidentGeneral.objects.all()
#     person_instance  = IncidentPerson.objects.all()
#     vehicle_instance = IncidentVehicle.objects.all()
#     media_instance = IncidentMedia.objects.all()
#     remarks_instance = IncidentRemark.objects.all()
#     context = {
#         'user_report': user_report,
#         'general_instance': general_instance,
#         'person_instance': person_instance,
#         'vehicle_instance': vehicle_instance,
#         'media_instance': media_instance,
#         'remarks_instance': remarks_instance,
#     }

#     return render(request, 'pages/incident_report_people_view.html', context)

# def incident_report_vehicle_view(request, id):
#     general_instance = get_object_or_404(IncidentGeneral, pk=id)
#     #user_instance = IncidentGeneral.objects.all()
#     user_report = IncidentGeneral.objects.all()
#     person_instance  = IncidentPerson.objects.all()
#     vehicle_instance = IncidentVehicle.objects.all()
#     media_instance = IncidentMedia.objects.all()
#     remarks_instance = IncidentRemark.objects.all()
#     context = {
#         'user_report': user_report,
#         'general_instance': general_instance,
#         'person_instance': person_instance,
#         'vehicle_instance': vehicle_instance,
#         'media_instance': media_instance,
#         'remarks_instance': remarks_instance,
#     }

#     return render(request, 'pages/incident_report_vehicle_view.html', context)

# def incident_report_media_view(request, id):
#     general_instance = get_object_or_404(IncidentGeneral, pk=id)
#     #user_instance = IncidentGeneral.objects.all()
#     user_report = IncidentGeneral.objects.all()
#     person_instance  = IncidentPerson.objects.all()
#     vehicle_instance = IncidentVehicle.objects.all()
#     media_instance = IncidentMedia.objects.all()
#     remarks_instance = IncidentRemark.objects.all()
#     context = {
#         'user_report': user_report,
#         'general_instance': general_instance,
#         'person_instance': person_instance,
#         'vehicle_instance': vehicle_instance,
#         'media_instance': media_instance,
#         'remarks_instance': remarks_instance,
#     }

#     return render(request, 'pages/incident_report_media_view.html', context)

# def incident_report_remarks_view(request, id):
#     general_instance = get_object_or_404(IncidentGeneral, pk=id)
#     #user_instance = IncidentGeneral.objects.all()
#     user_report = IncidentGeneral.objects.all()
#     person_instance  = IncidentPerson.objects.all()
#     vehicle_instance = IncidentVehicle.objects.all()
#     media_instance = IncidentMedia.objects.all()
#     remarks_instance = IncidentRemark.objects.all()
#     context = {
#         'user_report': user_report,
#         'general_instance': general_instance,
#         'person_instance': person_instance,
#         'vehicle_instance': vehicle_instance,
#         'media_instance': media_instance,
#         'remarks_instance': remarks_instance,
#     }

#     return render(request, 'pages/incident_report_remarks_view.html', context)





# FORMS = [("information", IncidentGeneralForm),
#         ("general", IncidentGeneralForm),
#          ("people", IncidentPersonForm),
#          ("vehicle",IncidentVehicleForm),
#          ("media", IncidentMediaForm),
#          ("remarks", IncidentRemarksForm)]

# 'user_report': user_report,
#         'general_instance': general_instance,
#         'person_instance': person_instance,
#         'vehicle_instance': vehicle_instance,
#         'media_instance': media_instance,
#         'remarks_instance': remarks_instance,

# def incident_report_people_edit(request, id=None):
#     IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
#     general = get_object_or_404(IncidentGeneral, pk=id)
#     person = get_object_or_404(IncidentPerson, pk=id)
#     if request.method == 'POST':
#         person_instance = IncidentPersonForm(request.POST  or None, request.FILES  or None, instance=person)
#         if person_instance.is_valid():
#             person_instance.save()
#             messages.success(request, 'Profile updated')
#             return redirect('user_reports')
#         else:
#             print(person_instance.errors)

#     else:
#         person_instance = IncidentPersonForm(instance=person)
#     context = {
#         'general': general,
#         'person_instance' : person_instance,
#         'IncidentGeneral': IncidentGeneral,
#         'person': person
#     }
    
#     return render(request, 'pages/incident_report_people_edit.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    accident_factor = AccidentCausation.objects.all()
    paginator = Paginator(accident_factor, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in accident_factor:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = AccidentCausation.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Accident Factor successfully deleted')
        return redirect('attributes_builder_accident')
    context = {
        'accident_factor': page_obj,
        'profile':profile
    }
    return render(request, 'pages/super/accident_factor.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_sub(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    accident_factor_sub = AccidentCausationSub.objects.filter(accident_factor=accident_factor)
    paginator = Paginator(accident_factor_sub, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in accident_factor_sub:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = AccidentCausationSub.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Accident Facor Sub-category successfully deleted')
        return redirect('attributes_builder_accident')
    context = {
        'accident_factor': accident_factor,
        'accident_factor_sub': page_obj,
    }
    return render(request, 'pages/super/accident_factor_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_crash(request):
    crash_type = CrashType.objects.all()
    paginator = Paginator(crash_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in crash_type:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = CrashType.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Crash Type successfully deleted')
        return redirect('attributes_builder_crash')
    context = {
        'crash_type': page_obj,
    }
    return render(request, 'pages/super/crash.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision(request):
    collision_type = CollisionType.objects.all()
    paginator = Paginator(collision_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in collision_type:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = CollisionType.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Collision Type successfully deleted')
    context = {
        'collision_type': page_obj,
    }
    return render(request, 'pages/super/collision_type.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_sub(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    collision_type_sub = CollisionTypeSub.objects.filter(collision_type=collision_type)
    paginator = Paginator(collision_type_sub, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in collision_type_sub:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = CollisionTypeSub.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Collision Type Sub-category successfully deleted')
    context = {
        'collision_type': collision_type,
        'collision_type_sub': page_obj,
    }
    return render(request, 'pages/super/collision_type_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_add(request):
    if request.method == 'POST':
        form = AccidentCausationForm(request.POST)
        try:
            if form.is_valid():
                
                category = form.cleaned_data['category']
                
                matching_courses = AccidentCausation.objects.filter(category=category)
                if matching_courses.exists():
                    messages.error(request, 'You already entered the same accident factor subcategory')
                    return redirect('attributes_builder_accident')
                else:
                    accident_factor = AccidentCausation(category=category)
                    accident_factor.save()
                    messages.success(request, 'Accident Factor Added')
                    return redirect('attributes_builder_accident')
                
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = AccidentCausationForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super/accident_factor_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_edit(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    if request.method == 'POST':
        form = AccidentCausationForm(request.POST or None,
                              request.FILES or None, instance=accident_factor)
        if form.is_valid():
            category = form.cleaned_data['category']
            matching_courses = AccidentCausation.objects.filter(category=category)
            if matching_courses:
                messages.error(request, 'You already entered the same accident factor subcategory')
                return redirect('attributes_builder_accident')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same accident factor subcategory')
                return redirect('attributes_builder_accident')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_accident')
    else:
        form = AccidentCausationForm(instance=accident_factor)
    context = {
        'form': form,
        'accident_factor': accident_factor,
    }
    return render(request, 'pages/super/accident_factor_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_delete(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    #user_report = IncidentGeneral.objects.all()
    accident_factor.delete()
    return redirect('attributes_builder_accident')

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_add_sub(request):
    if request.method == 'POST':
        form = AccidentCausationSubForm(request.POST)
        try:
            if form.is_valid():
                accident_factor = form.cleaned_data['accident_factor']
                sub_category = form.cleaned_data['sub_category']
                matching_courses = AccidentCausationSub.objects.filter(accident_factor=accident_factor,sub_category=sub_category)
                if matching_courses:
                    messages.error(request, 'You already entered the same accident factor subcategory')
                    return redirect('attributes_builder_accident_add_sub')
                    
                elif matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
                    messages.error(request, 'You already entered the same accident factor subcategory')
                else:
                    accident_factor = AccidentCausationSub(accident_factor=accident_factor, sub_category=sub_category)
                    accident_factor.save()
                    messages.success(request, 'Accident Factor Subcategory Added')
                    return redirect('attributes_builder_accident')
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = AccidentCausationSubForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super/accident_factor_add_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_edit_sub(request, id):
    accident_factor_sub = get_object_or_404(AccidentCausationSub, pk=id)
    if request.method == 'POST':
        form = AccidentCausationSubForm(request.POST or None,
                              request.FILES or None, instance=accident_factor_sub)
        if form.is_valid():
            accident_factor = form.cleaned_data['accident_factor']
            sub_category = form.cleaned_data['sub_category']
            matching_courses = AccidentCausationSub.objects.filter(accident_factor=accident_factor,sub_category=sub_category)
            if matching_courses:
                messages.error(request, 'You already entered the same accident factor subcategory')
                return redirect('attributes_builder_accident')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same accident factor subcategory')
                return redirect('attributes_builder_accident')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_accident')
    else:
        form = AccidentCausationSubForm(instance=accident_factor_sub)
    context = {
        'form': form,
        'accident_factor_sub': accident_factor_sub,
    }
    return render(request, 'pages/super/accident_factor_edit_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_delete_sub(request, id):
    accident_factor_sub = get_object_or_404(AccidentCausationSub, pk=id)
    #user_report = IncidentGeneral.objects.all()
    accident_factor_sub.delete()
    messages.error(request, 'Accident Factor Sub-category has been successfully deleted')
    return redirect('attributes_builder_accident')

# COLLISION
@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_add(request):
    if request.method == 'POST':
        form = CollisionTypeForm(request.POST)
        try:
            if form.is_valid():
                
                category = form.cleaned_data['category']
                
                matching_courses = CollisionType.objects.filter(category=category)
                if matching_courses.exists():
                    messages.error(request, 'You already entered the same collision type')
                    return redirect('attributes_builder_collision')
                else:
                    accident_factor = CollisionType(category=category)
                    accident_factor.save()
                    messages.success(request, 'Collision Type Added')
                    return redirect('attributes_builder_collision')
                
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = CollisionTypeForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super/collision_type_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_edit(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    if request.method == 'POST':
        form = CollisionTypeForm(request.POST or None,
                              request.FILES or None, instance=collision_type)
        if form.is_valid():
            category = form.cleaned_data['category']
            matching_courses = CollisionType.objects.filter(category=category)
            if matching_courses:
                messages.error(request, 'You already entered the same collision type')
                return redirect('attributes_builder_collision')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same collision type')
                return redirect('attributes_builder_collision')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_collision')
    else:
        form = CollisionTypeForm(instance=collision_type)
    context = {
        'form': form,
        'collision_type': collision_type,
    }
    return render(request, 'pages/super/collision_type_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_delete(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    #user_report = IncidentGeneral.objects.all()
    collision_type.delete()
    return redirect('attributes_builder_collision')

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_add_sub(request):
    if request.method == 'POST':
        form = CollisionTypeSubForm(request.POST)
        try:
            if form.is_valid():
                collision_type = form.cleaned_data['collision_type']
                sub_category = form.cleaned_data['sub_category']
                matching_courses = CollisionTypeSub.objects.filter(collision_type=collision_type, sub_category=sub_category)
                if matching_courses:
                    messages.error(request, 'You already entered the same collision type sub-category')
                    return redirect('attributes_builder_collision')
                    
                elif matching_courses.exists():
                    messages.error(request, 'You already entered the same collision type sub-category')
                    return redirect('attributes_builder_collision')
                else:
                    accident_factor = CollisionTypeSub(collision_type=collision_type, sub_category=sub_category)
                    accident_factor.save()
                    messages.success(request, 'Collision Type Subcategory Added')
                    return redirect('attributes_builder_collision')
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = CollisionTypeSubForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super/collision_type_add_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_edit_sub(request, id):
    collision_type_sub = get_object_or_404(CollisionTypeSub, pk=id)
    if request.method == 'POST':
        form = CollisionTypeSubForm(request.POST or None,
                              request.FILES or None, instance=collision_type_sub)
        if form.is_valid():
            collision_type = form.cleaned_data['collision_type']
            sub_category = form.cleaned_data['sub_category']
            matching_courses = CollisionTypeSub.objects.filter(collision_type=collision_type,sub_category=sub_category)
            if matching_courses:
                messages.error(request, 'You already entered the same collision type sub-category')
                return redirect('attributes_builder_collision')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same collision type sub-category')
                return redirect('attributes_builder_collision')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_collision')
    else:
        form = CollisionTypeSubForm(instance=collision_type_sub)
    context = {
        'form': form,
        'collision_type_sub': collision_type_sub,
    }
    return render(request, 'pages/super/collision_type_edit_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_delete_sub(request, id):
    collision_type_sub = get_object_or_404(CollisionTypeSub, pk=id)
    #user_report = IncidentGeneral.objects.all()
    collision_type_sub.delete()
    return redirect('attributes_builder_collision')

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_crash_add(request):
    if request.method == 'POST':
        form = CrashTypeForm(request.POST)
        try:
            if form.is_valid():
                
                crash_type = form.cleaned_data['crash_type']
                
                matching_courses = CrashType.objects.filter(crash_type=crash_type)
                if matching_courses.exists():
                    messages.error(request, 'You already entered the same crash type')
                    return redirect('attributes_builder_crash')
                else:
                    accident_factor = CrashType(crash_type=crash_type)
                    accident_factor.save()
                    messages.success(request, 'Collision Type Added')
                    return redirect('attributes_builder_crash')
                
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = CrashTypeForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/super/crash_type_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_crash_edit(request, id):
    crash_type = get_object_or_404(CrashType, pk=id)
    if request.method == 'POST':
        form = CrashTypeForm(request.POST or None,
                              request.FILES or None, instance=crash_type)
        if form.is_valid():
            crash_types = form.cleaned_data['crash_type']
            matching_courses = CrashType.objects.filter(crash_type=crash_types)
            if matching_courses:
                messages.error(request, 'You already entered the same crash type')
                return redirect('attributes_builder_crash')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same crash type')
                return redirect('attributes_builder_crash')
            else:
                form.save()
                messages.success(request, 'Crash Type Updated')
                return redirect('attributes_builder_crash')
    else:
        form = CrashTypeForm(instance=crash_type)
    context = {
        'form': form,
        'crash_type': crash_type,
    }
    return render(request, 'pages/super/crash_type_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_crash_delete(request, id):
    crash_type = get_object_or_404(CrashType, pk=id)
    #user_report = IncidentGeneral.objects.all()
    crash_type.delete()
    return redirect('attributes_builder_crash')



@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_admin(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    accident_factor = AccidentCausation.objects.all()
    paginator = Paginator(accident_factor, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in accident_factor:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = AccidentCausation.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Accident Factor successfully deleted')
        return redirect('attributes_builder_accident_admin')
    context = {
        'accident_factor': page_obj,
        'profile':profile
    }
    return render(request, 'pages/admin/accident_factor.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_sub_admin(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    accident_factor_sub = AccidentCausationSub.objects.filter(accident_factor=accident_factor)
    paginator = Paginator(accident_factor_sub, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in accident_factor_sub:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = AccidentCausationSub.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Accident Facor Sub-category successfully deleted')
        return redirect('attributes_builder_accident_admin')
    context = {
        'accident_factor': accident_factor,
        'accident_factor_sub': page_obj,
    }
    return render(request, 'pages/admin/accident_factor_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_crash_admin(request):
    crash_type = CrashType.objects.all()
    paginator = Paginator(crash_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in crash_type:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = CrashType.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Crash Type successfully deleted')
        return redirect('attributes_builder_crash_admin')
    context = {
        'crash_type': page_obj,
    }
    return render(request, 'pages/admin/crash.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_admin(request):
    collision_type = CollisionType.objects.all()
    paginator = Paginator(collision_type, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in collision_type:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = CollisionType.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Collision Type successfully deleted')
            return redirect('attributes_builder_collision_admin')
    context = {
        'collision_type': page_obj,
    }
    return render(request, 'pages/admin/collision_type.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_sub_admin(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    collision_type_sub = CollisionTypeSub.objects.filter(collision_type=collision_type)
    paginator = Paginator(collision_type_sub, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        for i in collision_type_sub:
            x = request.POST.get(str(i.id))
            print(x)
            if str(x) == 'on':
                b = CollisionTypeSub.objects.get(id=i.id)
                b.delete()
            messages.success(request, 'Collision Type Sub-category successfully deleted')
            return redirect('attributes_builder_collision_admin')
    context = {
        'collision_type': collision_type,
        'collision_type_sub': page_obj,
    }
    return render(request, 'pages/admin/collision_type_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_add_admin(request):
    if request.method == 'POST':
        form = AccidentCausationForm(request.POST)
        try:
            if form.is_valid():
                
                category = form.cleaned_data['category']
                
                matching_courses = AccidentCausation.objects.filter(category=category)
                if matching_courses.exists():
                    messages.error(request, 'You already entered the same accident factor')
                    return redirect('attributes_builder_accident_admin')
                else:
                    accident_factor = AccidentCausation(category=category)
                    accident_factor.save()
                    messages.success(request, 'Accident Factor Added')
                    return redirect('attributes_builder_accident_admin')
                
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = AccidentCausationForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/admin/accident_factor_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_edit_admin(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    if request.method == 'POST':
        form = AccidentCausationForm(request.POST or None,
                              request.FILES or None, instance=accident_factor)
        if form.is_valid():
            category = form.cleaned_data['category']
            matching_courses = AccidentCausation.objects.filter(category=category)
            if matching_courses:
                messages.error(request, 'You already entered the same accident factor')
                return redirect('attributes_builder_accident_admin')
                
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same accident factor')
                return redirect('attributes_builder_accident_admin')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_accident_admin')
    else:
        form = AccidentCausationForm(instance=accident_factor)
    context = {
        'form': form,
        'accident_factor': accident_factor,
    }
    return render(request, 'pages/admin/accident_factor_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_delete_admin(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    #user_report = IncidentGeneral.objects.all()
    accident_factor.delete()
    return redirect('attributes_builder_accident_admin')

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_add_sub_admin(request):
    if request.method == 'POST':
        form = AccidentCausationSubForm(request.POST)
        try:
            if form.is_valid():
                accident_factor = form.cleaned_data['accident_factor']
                sub_category = form.cleaned_data['sub_category']
                matching_courses = AccidentCausationSub.objects.filter(accident_factor=accident_factor,sub_category=sub_category)
                if matching_courses:
                    messages.error(request, 'You already entered the same accident factor sub-category')
                    return redirect('attributes_builder_accident_admin')
                    
                elif matching_courses.exists():
                    messages.error(request, 'You already entered the same accident factor sub-category')
                    return redirect('attributes_builder_accident_admin')
                else:
                    accident_factor = AccidentCausationSub(accident_factor=accident_factor, sub_category=sub_category)
                    accident_factor.save()
                    messages.success(request, 'Accident Factor Subcategory Added')
                    return redirect('attributes_builder_accident_admin')
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = AccidentCausationSubForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/admin/accident_factor_add_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_edit_sub_admin(request, id):
    accident_factor_sub = get_object_or_404(AccidentCausationSub, pk=id)
    if request.method == 'POST':
        form = AccidentCausationSubForm(request.POST or None,
                              request.FILES or None, instance=accident_factor_sub)
        if form.is_valid():
            accident_factor = form.cleaned_data['accident_factor']
            sub_category = form.cleaned_data['sub_category']
            matching_courses = AccidentCausationSub.objects.filter(accident_factor=accident_factor,sub_category=sub_category)
            if matching_courses:
                messages.error(request, 'You already entered the same accident factor sub-category')
                return redirect('attributes_builder_accident_admin')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same accident factor sub-category')
                return redirect('attributes_builder_accident_admin')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_accident_admin')
    else:
        form = AccidentCausationSubForm(instance=accident_factor_sub)
    context = {
        'form': form,
        'accident_factor_sub': accident_factor_sub,
    }
    return render(request, 'pages/admin/accident_factor_edit_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_accident_delete_sub_admin(request, id):
    accident_factor_sub = get_object_or_404(AccidentCausationSub, pk=id)
    #user_report = IncidentGeneral.objects.all()
    accident_factor_sub.delete()
    return redirect('attributes_builder_accident_admin')

# COLLISION
@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_add_admin(request):
    if request.method == 'POST':
        form = CollisionTypeForm(request.POST)
        try:
            if form.is_valid():
                
                category = form.cleaned_data['category']
                
                matching_courses = CollisionType.objects.filter(category=category)
                if matching_courses.exists():
                    messages.error(request, 'You already entered the same collision type')
                    return redirect('attributes_builder_collision_admin')
                else:
                    accident_factor = CollisionType(category=category)
                    accident_factor.save()
                    messages.success(request, 'Collision Type Added')
                    return redirect('attributes_builder_collision_admin')
                
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = CollisionTypeForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/admin/collision_type_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_edit_admin(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    if request.method == 'POST':
        form = CollisionTypeForm(request.POST or None,
                              request.FILES or None, instance=collision_type)
        if form.is_valid():
            category = form.cleaned_data['category']
            matching_courses = CollisionType.objects.filter(category=category)
            if matching_courses:
                messages.error(request, 'You already entered the same collision type')
                return redirect('attributes_builder_collision_admin')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same collision type')
                return redirect('attributes_builder_collision_admin')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_collision_admin')
    else:
        form = CollisionTypeForm(instance=collision_type)
    context = {
        'form': form,
        'collision_type': collision_type,
    }
    return render(request, 'pages/admin/collision_type_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_delete_admin(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    #user_report = IncidentGeneral.objects.all()
    collision_type.delete()
    return redirect('attributes_builder_collision_admin')

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_add_sub_admin(request):
    if request.method == 'POST':
        form = CollisionTypeSubForm(request.POST)
        try:
            if form.is_valid():
                collision_type = form.cleaned_data['collision_type']
                sub_category = form.cleaned_data['sub_category']
                matching_courses = CollisionTypeSub.objects.filter(collision_type=collision_type, sub_category=sub_category)
                if matching_courses:
                    messages.error(request, 'You already entered the same collision type sub-category')
                    return redirect('attributes_builder_collision_admin')
                    
                elif matching_courses.exists():
                    messages.error(request, 'You already entered the same collision type sub-category')
                    return redirect('attributes_builder_collision_admin')
                else:
                    accident_factor = CollisionTypeSub(collision_type=collision_type, sub_category=sub_category)
                    accident_factor.save()
                    messages.success(request, 'Collision Type Subcategory Added')
                    return redirect('attributes_builder_collision_admin')
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = CollisionTypeSubForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/admin/collision_type_add_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_edit_sub_admin(request, id):
    collision_type_sub = get_object_or_404(CollisionTypeSub, pk=id)
    if request.method == 'POST':
        form = CollisionTypeSubForm(request.POST or None,
                              request.FILES or None, instance=collision_type_sub)
        if form.is_valid():
            collision_type = form.cleaned_data['collision_type']
            sub_category = form.cleaned_data['sub_category']
            matching_courses = CollisionTypeSub.objects.filter(collision_type=collision_type,sub_category=sub_category)
            if matching_courses:
                messages.error(request, 'You already entered the same collision type sub-category')
                return redirect('attributes_builder_collision_admin')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same collision type sub-category')
                return redirect('attributes_builder_collision_admin')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_collision_admin')
    else:
        form = CollisionTypeSubForm(instance=collision_type_sub)
    context = {
        'form': form,
        'collision_type_sub': collision_type_sub,
    }
    return render(request, 'pages/admin/collision_type_edit_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_collision_delete_sub_admin(request, id):
    collision_type_sub = get_object_or_404(CollisionTypeSub, pk=id)
    #user_report = IncidentGeneral.objects.all()
    collision_type_sub.delete()
    return redirect('attributes_builder_collision_admin')

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_crash_add_admin(request):
    if request.method == 'POST':
        form = CrashTypeForm(request.POST)
        try:
            if form.is_valid():
                
                crash_type = form.cleaned_data['crash_type']
                
                matching_courses = CrashType.objects.filter(crash_type=crash_type)
                if matching_courses.exists():
                    messages.error(request, 'You already entered the same crash type')
                    return redirect('attributes_builder_collision_admin')
                else:
                    accident_factor = CrashType(crash_type=crash_type)
                    accident_factor.save()
                    messages.success(request, 'Collision Type Added')
                    return redirect('attributes_builder_crash_admin')
                
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


    else:
        form = CrashTypeForm()
    context = {
        'form' : form,
    }
    return render(request, 'pages/admin/crash_type_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_crash_edit_admin(request, id):
    crash_type = get_object_or_404(CrashType, pk=id)
    if request.method == 'POST':
        form = CrashTypeForm(request.POST or None,
                              request.FILES or None, instance=crash_type)
        if form.is_valid():
            crash_types = form.cleaned_data['crash_type']
            matching_courses = CrashType.objects.filter(crash_type=crash_types)
            if matching_courses:
                messages.error(request, 'You already entered the same crash type')
                return redirect('attributes_builder_collision_admin')
                
            elif matching_courses.exists():
                messages.error(request, 'You already entered the same crash type')
                return redirect('attributes_builder_collision_admin')
            else:
                form.save()
                messages.success(request, 'Crash Type Updated')
                return redirect('attributes_builder_crash_admin')
    else:
        form = CrashTypeForm(instance=crash_type)
    context = {
        'form': form,
        'crash_type': crash_type,
    }
    return render(request, 'pages/admin/crash_type_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def attributes_builder_crash_delete_admin(request, id):
    crash_type = get_object_or_404(CrashType, pk=id)
    #user_report = IncidentGeneral.objects.all()
    crash_type.delete()
    return redirect('attributes_builder_crash_admin')

@login_required(login_url='login')
@user_passes_test(check_role_super)
def sa_incidentreports(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form =  IncidentGeneralForm(request.POST or None, request.FILES or None)
        form_general = IncidentGeneralForm(request.POST or None, request.FILES or None)
        # form_people = IncidentRemarksForm(request.POST or None, request.FILES or None)
        form_media = IncidentRemarksForm(request.POST or None, request.FILES or None)
        form_remarks = IncidentRemarksForm(request.POST or None, request.FILES or None)
        try:
            if form.is_valid() and form_general.is_valid() and form_remarks.is_valid():
                date=request.POST.get("date")
                time=request.POST.get("time")
                address=request.POST.get("address")
                city=request.POST.get("city")
                pin_code=request.POST.get("pin_code")
                latitude=request.POST.get("latitude")
                longitude=request.POST.get("longitude")
                description=request.POST.get("description")
                
    
                accident_factor1 = request.POST.get("accident_factor")
                accident_factor = AccidentCausation.objects.get(pk=accident_factor1)

                collision_type1 = request.POST.get("collision_type")
                collision_type = CollisionType.objects.get(pk=collision_type1)

                
                crash_type1 = request.POST.get("crash_type")
                crash_type = CrashType.objects.get(pk=crash_type1)
                
                weather = request.POST.get("weather")
                light = request.POST.get("light")
                severity = request.POST.get("severity")
                movement_code = request.POST.get("movement_code")
                
                
                desc=request.POST.getlist("desc[]")
                images=request.FILES.getlist("file[]")
                
                responder = request.POST.get("responder")
                action_taken = request.POST.get("action_taken")
                form.user = request.user
                # user_report=IncidentGeneral(user=request.user,date=date,time=time,address=address,city=city,pin_code=pin_code,latitude=latitude,longitude=longitude,description=description)
                # user_report.status = 2
                # user_report.save()
                
                user_instance =  IncidentGeneral.objects.filter(date = date)
                
                # if user_instance.exists():
                #     user_report.duplicate = "Possible Duplicate"
                #     user_report.save()
                # else:
                #     user_report.save()
                
                incident_general=IncidentGeneral(user=request.user,date=date,time=time,address=address,city=city,pin_code=pin_code,latitude=latitude,longitude=longitude,description=description,
                                                 accident_factor=accident_factor,
                                                collision_type=collision_type,
                                                crash_type=crash_type,
                                                weather=weather,light=light,severity=severity,movement_code=movement_code)
                incident_general.status = 2
                incident_general.save()
                
                incident_remarks = IncidentRemark(incident_general=incident_general,responder=responder,action_taken=action_taken)
                incident_remarks.save()
                
                
                
                messages.success(request,"Data Save Successfully")
                request.session['latest__id'] = incident_general.id
                return redirect('sa_incidentreports_additional')
            
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))


        else:
            print('invalid formd')
            print(form.errors)
            print(form_general.errors)
            print(form_remarks.errors)
    else:
        form = IncidentGeneralForm()
        form_general = IncidentGeneralForm()
        form_remarks = IncidentRemarksForm()        
    context = {
        'form': form,
        'form_general': form_general,
        'form_remarks': form_remarks,
        'profile':profile
    }
    return render(request,"pages/super/sa_incident_report.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def sa_incidentreports_additional(request):
    # if request.method!="POST":
    general_id = request.session.get('latest__id', None)
    # incident_general = IncidentGeneral.objects.get(pk = id)
    # incident_general = IncidentGeneral.objects.filter(id=general_id).first()
    profile = get_object_or_404(UserProfile, user=request.user)
    incident_general = get_object_or_404(IncidentGeneral, pk=general_id )
    if request.method == 'POST':
        form =  IncidentGeneralForm(request.POST or None, request.FILES or None)
        form_general = IncidentGeneralForm(request.POST or None, request.FILES or None)
        form_people = IncidentPersonForm(request.POST or None, request.FILES or None)
        form_vehicle = IncidentVehicleForm(request.POST or None, request.FILES or None)
        form_media = IncidentMediaForm(request.POST or None, request.FILES or None)
        form_remarks = IncidentRemarksForm(request.POST or None, request.FILES or None)
        try:
            if form_people.is_valid() and form_vehicle.is_valid() and form_media.is_valid():
                incident_first_name=request.POST.get("incident_first_name")
                incident_middle_name=request.POST.get("incident_middle_name")
                incident_last_name=request.POST.get("incident_last_name")
                incident_age=request.POST.get("incident_age")
                incident_gender=request.POST.get("incident_gender")
                incident_address=request.POST.get("incident_address")
                incident_involvement=request.POST.get("incident_involvement")
                incident_id_presented=request.POST.get("incident_id_presented")
                incident_id_number=request.POST.get("incident_id_number")
                incident_injury=request.POST.get("incident_injury")
                incident_driver_error=request.POST.get("incident_driver_error")
                incident_alcohol_drugs=request.POST.get("incident_alcohol_drugs")
                incident_seatbelt_helmet=request.POST.get("incident_seatbelt_helmet")
                
               
                incident_person=IncidentPerson(incident_general=incident_general, incident_first_name=incident_first_name,incident_middle_name=incident_middle_name,
                                       incident_last_name=incident_last_name,incident_age=incident_age,
                                       incident_gender=incident_gender,incident_address=incident_address,
                                       incident_involvement=incident_involvement,incident_id_presented=incident_id_presented,
                                       incident_id_number=incident_id_number, incident_injury=incident_injury,
                                       incident_driver_error=incident_driver_error, incident_alcohol_drugs=incident_alcohol_drugs,
                                      incident_seatbelt_helmet=incident_seatbelt_helmet)
                incident_person.save()
                
                classification=request.POST.get("classification")
                vehicle_type=request.POST.get("vehicle_type")
                brand=request.POST.get("brand")
                plate_number=request.POST.get("plate_number")
                engine_number=request.POST.get("engine_number")
                chassis_number=request.POST.get("chassis_number")
                insurance_details=request.POST.get("insurance_details")
                maneuver=request.POST.get("maneuver")
                damage=request.POST.get("damage")
                defect=request.POST.get("defect")
                loading=request.POST.get("loading")

                incident_upload_photovideo=request.POST.get("incident_upload_photovideo")
                media_description=request.POST.get("incident_upload_photovideo")
               
                incident_vehicle=IncidentVehicle(incident_general=incident_general, classification=classification,vehicle_type=vehicle_type,
                                       brand=brand,plate_number=plate_number,
                                       engine_number=engine_number,chassis_number=chassis_number,
                                       insurance_details=insurance_details, maneuver=maneuver,
                                       damage=damage, defect=defect,
                                      loading=loading)
                incident_vehicle.save()
                
                incident_media=IncidentMedia(incident_general=incident_general, media_description=media_description, incident_upload_photovideo=incident_upload_photovideo)
                incident_media.save()
               
                messages.success(request,"Data Save Successfully 1")
                return redirect('sa_incidentreports_additional')
            
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))

            messages.error(request,"Error in Saving Data")
            # return redirect ('user_reports')
        else:
            print('invalid formd')
            print(form.errors)
            print(form_people.errors)
            print(form_vehicle.errors)
            print(form_media.errors)
    else:
        form = IncidentGeneralForm()
        form_general = IncidentGeneralForm()
        form_people = IncidentPersonForm()
        form_vehicle = IncidentVehicleForm()
        form_media = IncidentMediaForm()
        form_remarks = IncidentRemarksForm()        
    context = {
        'form': form,
        'form_general': form_general,
        'form_people': form_people,
        'form_vehicle': form_vehicle,
        'form_media': form_media,
        'form_remarks': form_remarks,
        'profile':profile,
        'incident_general':incident_general
    }
    return render(request,"pages/super/sa_incident_report_additional.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def a_incidentreports(request):
    # if request.method!="POST":
    #     return redirect ('user_reports')
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form =  IncidentGeneralForm(request.POST or None, request.FILES or None)
        form_general = IncidentGeneralForm(request.POST or None, request.FILES or None)
        # form_people = IncidentRemarksForm(request.POST or None, request.FILES or None)
        form_media = IncidentRemarksForm(request.POST or None, request.FILES or None)
        form_remarks = IncidentRemarksForm(request.POST or None, request.FILES or None)
        try:
            if form.is_valid() and form_general.is_valid() and form_remarks.is_valid():
                date=request.POST.get("date")
                time=request.POST.get("time")
                address=request.POST.get("address")
                city=request.POST.get("city")
                pin_code=request.POST.get("pin_code")
                latitude=request.POST.get("latitude")
                longitude=request.POST.get("longitude")
                description=request.POST.get("description")
                
                
                # accident_factor = AccidentCausation.objects.get(pk=request.id)
                # accident_subcategory = AccidentCausationSub.objects.get(pk=request.id)
                # collision_type = CollisionType.objects.get(pk=request.id)
                # collision_subcategory = CollisionTypeSub.objects.get(pk=request.id)
                # crash_type = CrashType.objects.get(pk=request.id)
                accident_factor1 = request.POST.get("accident_factor")
                accident_factor = AccidentCausation.objects.get(pk=accident_factor1)
                
                # accident_subcategory1 = request.POST.get("accident_subcategory")
                # accident_subcategory = AccidentCausationSub.objects.get(pk=accident_subcategory1)
                collision_type1 = request.POST.get("collision_type")
                collision_type = CollisionType.objects.get(pk=collision_type1)
                
                
                
                # collision_subcategory1 = request.POST.get("collision_subcategory")
                # collision_subcategory = CollisionTypeSub.objects.get(pk=collision_subcategory1)
                
                crash_type1 = request.POST.get("crash_type")
                crash_type = CrashType.objects.get(pk=crash_type1)
                
                weather = request.POST.get("weather")
                light = request.POST.get("light")
                severity = request.POST.get("severity")
                movement_code = request.POST.get("movement_code")
                
                
                desc=request.POST.getlist("desc[]")
                images=request.FILES.getlist("file[]")
                
                responder = request.POST.get("responder")
                action_taken = request.POST.get("action_taken")
                form.user = request.user
                user_report=IncidentGeneral(user=request.user,date=date,time=time,address=address,city=city,pin_code=pin_code,latitude=latitude,longitude=longitude,description=description)
                user_report.status = 2
                user_report.save()
                incident_general=IncidentGeneral(user_report=user_report,accident_factor=accident_factor,
                                                collision_type=collision_type,
                                                crash_type=crash_type,
                                                weather=weather,light=light,severity=severity,movement_code=movement_code)
                incident_general.save()
                
                incident_remarks = IncidentRemark(incident_general=incident_general,responder=responder,action_taken=action_taken)
                incident_remarks.save()
                
                messages.success(request,"Data Save Successfully")
                request.session['latest__id'] = incident_general.id
                return redirect('a_incidentreports_additional')
            
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))

            messages.error(request,"Error in Saving Data")
            # return redirect ('user_reports')
        else:
            print('invalid formd')
            print(form.errors)
            print(form_general.errors)
            print(form_remarks.errors)
    else:
        form = IncidentGeneralForm()
        form_general = IncidentGeneralForm()
        form_remarks = IncidentRemarksForm()        
    context = {
        'form': form,
        'form_general': form_general,
        'form_remarks': form_remarks,
        'profile':profile
    }
    return render(request,"pages/admin/a_incident_report.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def a_incidentreports_additional(request):
    # if request.method!="POST":
    general_id = request.session.get('latest__id', None)
    # incident_general = IncidentGeneral.objects.get(pk = id)
    # incident_general = IncidentGeneral.objects.filter(id=general_id).first()
    profile = get_object_or_404(UserProfile, user=request.user)
    incident_general = get_object_or_404(IncidentGeneral, pk=general_id )
    if request.method == 'POST':
        form =  IncidentGeneralForm(request.POST or None, request.FILES or None)
        form_general = IncidentGeneralForm(request.POST or None, request.FILES or None)
        form_people = IncidentPersonForm(request.POST or None, request.FILES or None)
        form_vehicle = IncidentVehicleForm(request.POST or None, request.FILES or None)
        form_media = IncidentMediaForm(request.POST or None, request.FILES or None)
        form_remarks = IncidentRemarksForm(request.POST or None, request.FILES or None)
        try:
            if form_people.is_valid() and form_vehicle.is_valid() and form_media.is_valid():
                incident_first_name=request.POST.get("incident_first_name")
                incident_middle_name=request.POST.get("incident_middle_name")
                incident_last_name=request.POST.get("incident_last_name")
                incident_age=request.POST.get("incident_age")
                incident_gender=request.POST.get("incident_gender")
                incident_address=request.POST.get("incident_address")
                incident_involvement=request.POST.get("incident_involvement")
                incident_id_presented=request.POST.get("incident_id_presented")
                incident_id_number=request.POST.get("incident_id_number")
                incident_injury=request.POST.get("incident_injury")
                incident_driver_error=request.POST.get("incident_driver_error")
                incident_alcohol_drugs=request.POST.get("incident_alcohol_drugs")
                incident_seatbelt_helmet=request.POST.get("incident_seatbelt_helmet")
                
               
                incident_person=IncidentPerson(incident_general=incident_general, incident_first_name=incident_first_name,incident_middle_name=incident_middle_name,
                                       incident_last_name=incident_last_name,incident_age=incident_age,
                                       incident_gender=incident_gender,incident_address=incident_address,
                                       incident_involvement=incident_involvement,incident_id_presented=incident_id_presented,
                                       incident_id_number=incident_id_number, incident_injury=incident_injury,
                                       incident_driver_error=incident_driver_error, incident_alcohol_drugs=incident_alcohol_drugs,
                                      incident_seatbelt_helmet=incident_seatbelt_helmet)
                incident_person.save()
                
                classification=request.POST.get("classification")
                vehicle_type=request.POST.get("vehicle_type")
                brand=request.POST.get("brand")
                plate_number=request.POST.get("plate_number")
                engine_number=request.POST.get("engine_number")
                chassis_number=request.POST.get("chassis_number")
                insurance_details=request.POST.get("insurance_details")
                maneuver=request.POST.get("maneuver")
                damage=request.POST.get("damage")
                defect=request.POST.get("defect")
                loading=request.POST.get("loading")

                incident_upload_photovideo=request.POST.get("incident_upload_photovideo")
                media_description=request.POST.get("incident_upload_photovideo")
               
                incident_vehicle=IncidentVehicle(incident_general=incident_general, classification=classification,vehicle_type=vehicle_type,
                                       brand=brand,plate_number=plate_number,
                                       engine_number=engine_number,chassis_number=chassis_number,
                                       insurance_details=insurance_details, maneuver=maneuver,
                                       damage=damage, defect=defect,
                                      loading=loading)
                incident_vehicle.save()
                
                incident_media=IncidentMedia(incident_general=incident_general, media_description=media_description, incident_upload_photovideo=incident_upload_photovideo)
                incident_media.save()
               
                messages.success(request,"Data Save Successfully 1")
                return redirect('a_incidentreports_additional')
            
        except Exception as e:
            print('invalid form')
            messages.error(request, str(e))

            messages.error(request,"Error in Saving Data")
            # return redirect ('user_reports')
        else:
            print('invalid formd')
            print(form.errors)
            print(form_people.errors)
            print(form_vehicle.errors)
            print(form_media.errors)
    else:
        form = IncidentGeneralForm()
        form_general = IncidentGeneralForm()
        form_people = IncidentPersonForm()
        form_vehicle = IncidentVehicleForm()
        form_media = IncidentMediaForm()
        form_remarks = IncidentRemarksForm()        
    context = {
        'form': form,
        'form_general': form_general,
        'form_people': form_people,
        'form_vehicle': form_vehicle,
        'form_media': form_media,
        'form_remarks': form_remarks,
        'profile':profile,
        'incident_general':incident_general
    }
    return render(request,"pages/admin/a_incident_report_additional.html", context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_general_view(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    
    #user_instance = IncidentGeneral.objects.all()
    user_report = IncidentGeneral.objects.all()
    person_instance  = IncidentPerson.objects.all()
    vehicle_instance = IncidentVehicle.objects.all()
    media_instance = IncidentMedia.objects.all()
    remarks_instance = IncidentRemark.objects.all()
    context = {
        'user_report': user_report,
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'media_instance': media_instance,
        'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_general_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_general_edit(request, id=None):
    # IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    IncidentGeneral = IncidentGeneral.objects.filter(__incident_general =general)
    if request.method == 'POST':
        general_instance = IncidentGeneralForm(request.POST  or None, request.FILES  or None, instance=general)
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        if general_instance.is_valid() and user_report.is_valid():
            user_report.instance.username = request.user
            general_instance.save()
            user_report.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(general_instance.errors)
            print(user_report.errors)

    else:
        general_instance = IncidentGeneralForm(instance=general)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'general_instance': general_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral
    }
    
    return render(request, 'pages/incident_report_general_edit.html', context)

def incident_report_remarks_view(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    remarks_instance = get_object_or_404(IncidentRemark, pk=id)
    #user_instance = IncidentGeneral.objects.all()
    user_report = IncidentGeneral.objects.all()
    person_instance  = IncidentPerson.objects.all()
    vehicle_instance = IncidentVehicle.objects.all()
    media_instance = IncidentMedia.objects.all()
    # remarks_instance = IncidentRemark.objects.all()
    context = {
        'user_report': user_report,
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'media_instance': media_instance,
        'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_remarks_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_remarks_view(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    remarks_instance = get_object_or_404(IncidentRemark, pk=id)
    #user_instance = IncidentGeneral.objects.all()
    user_report = IncidentGeneral.objects.all()
    person_instance  = IncidentPerson.objects.all()
    vehicle_instance = IncidentVehicle.objects.all()
    media_instance = IncidentMedia.objects.all()
    # remarks_instance = IncidentRemark.objects.all()
    context = {
        'user_report': user_report,
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'media_instance': media_instance,
        'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_remarks_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_people_vehicle_main(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    people_instance = IncidentPerson.objects.filter(incident_general =general_instance )
    vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
    #     'user_report': user_report,
        'general_instance': general_instance,
        'people_instance': people_instance,
        'vehicle_instance': vehicle_instance,
    #     'media_instance': media_instance,
    #     'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_people_vehicle_main.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_people_vehicle_view(request, id, people_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    person_instance = get_object_or_404(IncidentPerson, pk=people_id)
    vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_people_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_vehicle_main(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    vehicle_instance = IncidentVehicle.objects.filter(incident_general =general_instance )
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
    #     'user_report': user_report,
        'general_instance': general_instance,
        'vehicle_instance': vehicle_instance,
        
    #     'media_instance': media_instance,
    #     'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_vehicle_main.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_media_main(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    media_instance = IncidentMedia.objects.filter(incident_general =general_instance )
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
    #     'user_report': user_report,
        'general_instance': general_instance,
        'media_instance': media_instance,
        
    #     'media_instance': media_instance,
    #     'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_media_main.html', context)

def incident_report_vehicle_view(request, id, vehicle_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    vehicle_instance = get_object_or_404(IncidentVehicle, pk=vehicle_id)
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
        'general_instance': general_instance,
        # 'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_vehicle_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_media_view(request, id, media_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    media_instance = get_object_or_404(IncidentMedia, pk=media_id)
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
        'general_instance': general_instance,
        # 'person_instance': person_instance,
        'media_instance': media_instance,
        'profile':profile
    }

    return render(request, 'pages/incident_report_media_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_general_edit(request, id=None):
    # incidentGeneral1 =  get_object_or_404(IncidentGeneral, pk=id)
    incidentGeneral = get_object_or_404(IncidentGeneral, pk=id)
    if request.method == 'POST':
        general_instance = IncidentGeneralForm(request.POST  or None, request.FILES  or None, instance=incidentGeneral)
        # user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        if general_instance.is_valid():
            general_instance.instance.username = request.user
            general_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(general_instance.errors)
            # print(user_report.errors)

    else:
        general_instance = IncidentGeneralForm(instance=incidentGeneral)
        # user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'general_instance': general_instance,
        # 'user_report' : user_report,
        'general': incidentGeneral,
        'IncidentGeneral': IncidentGeneral
    }
    
    return render(request, 'pages/incident_report_general_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_remarks_edit(request, id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    remarks = get_object_or_404(IncidentRemark, pk=id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        remarks_instance = IncidentRemarksForm(request.POST  or None, request.FILES  or None, instance=remarks)
        if remarks_instance.is_valid():
            user_report.instance.username = request.user
            remarks_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(remarks_instance.errors)
            print(user_report.errors)

    else:
        remarks_instance = IncidentRemarksForm(instance=remarks)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'remarks_instance': remarks_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral
    }
    
    return render(request, 'pages/incident_report_remarks_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_people_edit(request, id=None, people_id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    people = get_object_or_404(IncidentPerson, pk=people_id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        person_instance = IncidentPersonForm(request.POST  or None, request.FILES  or None, instance=people)
        if person_instance.is_valid():
            user_report.instance.username = request.user
            person_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(person_instance.errors)
            print(user_report.errors)

    else:
        person_instance = IncidentPersonForm(instance=people)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'person_instance': person_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral,
        'people': people
    }
    
    return render(request, 'pages/incident_report_people_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_vehicle_edit(request, id=None, vehicle_id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    vehicle = get_object_or_404(IncidentVehicle, pk=vehicle_id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        vehicle_instance = IncidentVehicleForm(request.POST  or None, request.FILES  or None, instance=vehicle)
        if vehicle_instance.is_valid():
            user_report.instance.username = request.user
            vehicle_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(vehicle_instance.errors)
            print(user_report.errors)

    else:
        vehicle_instance = IncidentVehicleForm(instance=vehicle)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'vehicle_instance': vehicle_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral,
        'vehicle': vehicle
    }
    
    return render(request, 'pages/incident_report_vehicle_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def incident_report_media_edit(request, id=None, media_id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    media = get_object_or_404(IncidentMedia, pk=media_id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        media_instance = IncidentMediaForm(request.POST  or None, request.FILES  or None, instance=media)
        if media_instance.is_valid():
            user_report.instance.username = request.user
            media_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(media_instance.errors)
            print(user_report.errors)

    else:
        media_instance = IncidentMediaForm(instance=media)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'media_instance': media_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral,
        'media': media
    }
    
    return render(request, 'pages/incident_report_media_edit.html', context)




@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_general_view(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    #user_instance = IncidentGeneral.objects.all()
    user_report = IncidentGeneral.objects.all()
    person_instance  = IncidentPerson.objects.all()
    vehicle_instance = IncidentVehicle.objects.all()
    media_instance = IncidentMedia.objects.all()
    remarks_instance = IncidentRemark.objects.all()
    print(general_instance)
    context = {
        'user_report': user_report,
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'media_instance': media_instance,
        'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_general_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_general_edit(request, id):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    print(general)
    if request.method == 'POST':
        general_instance = IncidentGeneralForm(request.POST  or None, request.FILES  or None, instance=general)
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        if general_instance.is_valid() and user_report.is_valid():
            user_report.instance.username = request.user
            general_instance.save()
            user_report.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(general_instance.errors)
            print(user_report.errors)

    else:
        general_instance = IncidentGeneralForm(instance=general)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    print(general)
    context = {
        'general_instance': general_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral
    }
    
    return render(request, 'pages/a_incident_report_general_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_remarks_view(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    remarks_instance = get_object_or_404(IncidentRemark, pk=id)
    #user_instance = IncidentGeneral.objects.all()
    user_report = IncidentGeneral.objects.all()
    person_instance  = IncidentPerson.objects.all()
    vehicle_instance = IncidentVehicle.objects.all()
    media_instance = IncidentMedia.objects.all()
    # remarks_instance = IncidentRemark.objects.all()
    context = {
        'user_report': user_report,
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'media_instance': media_instance,
        'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_remarks_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_remarks_view(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    remarks_instance = get_object_or_404(IncidentRemark, pk=id)
    #user_instance = IncidentGeneral.objects.all()
    user_report = IncidentGeneral.objects.all()
    person_instance  = IncidentPerson.objects.all()
    vehicle_instance = IncidentVehicle.objects.all()
    media_instance = IncidentMedia.objects.all()
    # remarks_instance = IncidentRemark.objects.all()
    context = {
        'user_report': user_report,
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'media_instance': media_instance,
        'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_remarks_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_people_vehicle_main(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    people_instance = IncidentPerson.objects.filter(incident_general =general_instance )
    vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
    #     'user_report': user_report,
        'general_instance': general_instance,
        'people_instance': people_instance,
        'vehicle_instance': vehicle_instance,
    #     'media_instance': media_instance,
    #     'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_people_vehicle_main.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_people_vehicle_view(request, id, people_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    person_instance = get_object_or_404(IncidentPerson, pk=people_id)
    vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
        'general_instance': general_instance,
        'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_people_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_vehicle_main(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    vehicle_instance = IncidentVehicle.objects.filter(incident_general =general_instance )
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
    #     'user_report': user_report,
        'general_instance': general_instance,
        'vehicle_instance': vehicle_instance,
        
    #     'media_instance': media_instance,
    #     'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_vehicle_main.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_media_main(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    media_instance = IncidentMedia.objects.filter(incident_general =general_instance )
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
    #     'user_report': user_report,
        'general_instance': general_instance,
        'media_instance': media_instance,
        
    #     'media_instance': media_instance,
    #     'remarks_instance': remarks_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_media_main.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_vehicle_view(request, id, vehicle_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    vehicle_instance = get_object_or_404(IncidentVehicle, pk=vehicle_id)
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
        'general_instance': general_instance,
        # 'person_instance': person_instance,
        'vehicle_instance': vehicle_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_vehicle_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_media_view(request, id, media_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    media_instance = get_object_or_404(IncidentMedia, pk=media_id)
    # vehicle_instance = IncidentVehicle.objects.all()
    # #user_instance = IncidentGeneral.objects.all()
    # user_report = IncidentGeneral.objects.all()
    # person_instance  = IncidentPerson.objects.all()
    # vehicle_instance = IncidentVehicle.objects.all()
    # media_instance = IncidentMedia.objects.all()
    # # remarks_instance = IncidentRemark.objects.all()
    context = {
        'general_instance': general_instance,
        # 'person_instance': person_instance,
        'media_instance': media_instance,
        'profile':profile
    }

    return render(request, 'pages/a_incident_report_media_view.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_general_edit(request, id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    if request.method == 'POST':
        general_instance = IncidentGeneralForm(request.POST  or None, request.FILES  or None, instance=general)
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        if general_instance.is_valid() and user_report.is_valid():
            user_report.instance.username = request.user
            general_instance.save()
            user_report.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(general_instance.errors)
            print(user_report.errors)

    else:
        general_instance = IncidentGeneralForm(instance=general)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'general_instance': general_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral
    }
    
    return render(request, 'pages/a_incident_report_general_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_remarks_edit(request, id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    remarks = get_object_or_404(IncidentRemark, pk=id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        remarks_instance = IncidentRemarksForm(request.POST  or None, request.FILES  or None, instance=remarks)
        if remarks_instance.is_valid():
            user_report.instance.username = request.user
            remarks_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(remarks_instance.errors)
            print(user_report.errors)

    else:
        remarks_instance = IncidentRemarksForm(instance=remarks)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'remarks_instance': remarks_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral
    }
    
    return render(request, 'pages/a_incident_report_remarks_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_people_edit(request, id=None, people_id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    people = get_object_or_404(IncidentPerson, pk=people_id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        person_instance = IncidentPersonForm(request.POST  or None, request.FILES  or None, instance=people)
        if person_instance.is_valid():
            user_report.instance.username = request.user
            person_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(person_instance.errors)
            print(user_report.errors)

    else:
        person_instance = IncidentPersonForm(instance=people)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'person_instance': person_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral,
        'people': people
    }
    
    return render(request, 'pages/a_incident_report_people_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_vehicle_edit(request, id=None, vehicle_id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    vehicle = get_object_or_404(IncidentVehicle, pk=vehicle_id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        vehicle_instance = IncidentVehicleForm(request.POST  or None, request.FILES  or None, instance=vehicle)
        if vehicle_instance.is_valid():
            user_report.instance.username = request.user
            vehicle_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(vehicle_instance.errors)
            print(user_report.errors)

    else:
        vehicle_instance = IncidentVehicleForm(instance=vehicle)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'vehicle_instance': vehicle_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral,
        'vehicle': vehicle
    }
    
    return render(request, 'pages/a_incident_report_vehicle_edit.html', context)

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_incident_report_media_edit(request, id=None, media_id=None):
    IncidentGeneral =  get_object_or_404(IncidentGeneral, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    media = get_object_or_404(IncidentMedia, pk=media_id)
    if request.method == 'POST':
        user_report = IncidentGeneralForm(request.POST  or None, request.FILES  or None,  instance=IncidentGeneral)
        media_instance = IncidentMediaForm(request.POST  or None, request.FILES  or None, instance=media)
        if media_instance.is_valid():
            user_report.instance.username = request.user
            media_instance.save()
            messages.success(request, 'Profile updated')

            return redirect('user_reports')
        else:
            print(media_instance.errors)
            print(user_report.errors)

    else:
        media_instance = IncidentMediaForm(instance=media)
        user_report = IncidentGeneralForm(instance=IncidentGeneral)
    context = {
        'media_instance': media_instance,
        'user_report' : user_report,
        'general': general,
        'IncidentGeneral': IncidentGeneral,
        'media': media
    }
    
    return render(request, 'pages/a_incident_report_media_edit.html', context)



@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_report_people_delete(request, id):
    user_report = get_object_or_404(IncidentPerson, pk=id)
    user_report.delete()
    return redirect('user_reports')

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_report_vehicle_delete(request, id):
    user_report = get_object_or_404(IncidentVehicle, pk=id)
    user_report.delete()
    return redirect('user_reports')

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def super_user_report_media_delete(request, id):
    user_report = get_object_or_404(IncidentMedia, pk=id)
    user_report.delete()
    return redirect('user_reports')

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_report_people_delete(request, id):
    user_report = get_object_or_404(IncidentPerson, pk=id)
    user_report.delete()
    return redirect('user_reports')

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_report_vehicle_delete(request, id):
    user_report = get_object_or_404(IncidentVehicle, pk=id)
    user_report.delete()
    return redirect('user_reports')

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def admin_user_report_media_delete(request, id):
    user_report = get_object_or_404(IncidentMedia, pk=id)
    user_report.delete()
    return redirect('user_reports')

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def simple_upload(request):
    data = None
    
    try:
        if request.method == 'POST':
            data = request.FILES['myfile']
            
            if not data.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return redirect('user_reports')
            else: 
                data = pd.read_csv(data, header=0, encoding="UTF-8", na_values=[' '])
                data = data.astype(object).where(pd.notnull(data), None)
            try:
                for index, rows in data.iterrows():
                    
                        userid = rows["User ID"] 
                        generalid = rows["User ID"]
                        date = rows["Date"] if rows["Date"] else datetime.date.today()
                        time = rows["Time"]
                        description = rows["Description"] if rows["Description"] else " "
                        address = rows["Address"] if rows["Address"] else " "
                        latitude = rows["Latitude"] if rows["Latitude"] else " "
                        longitude = rows["Longitude"] if rows["Longitude"] else " "
                        status = rows["Status"] if rows["Status"] else " "
                        weather = rows["Weather"] if rows["Weather"] else " "
                        light = rows["Light"] if rows["Light"] else " "
                        accident_factor = rows["Accident Factor"] if rows["Accident Factor"] else " "
                        collision_type = rows["Collision Type"] if rows["Collision Type"] else " "
                        crash_type = rows["Crash"] if rows["Crash"] else " "
                        severity = rows["Severity"] if rows["Severity"] else " "
                        movement_code = rows["Movement Code"] if rows["Movement Code"] else " "
                        responder = rows["Responder"] if rows["Responder"] else " "
                        action_taken = rows["Action Taken"] if rows["Action Taken"] else " "
                    
                        # user_report_instance = IncidentGeneral.objects.get(userid=userid)
                        # general_instance = IncidentGeneral.objects.get(generalid=generalid)
                        
                        # get_or_create is used to eliminate forming or any duplicate record 
                        IncidentGeneral, created = IncidentGeneral.objects.get_or_create(
                            user=request.user,
                            userid=userid,
                            date=date,
                            time=time,
                            description=description,
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
                            status=status
                        )
                        
                        usergeneral, created = IncidentGeneral.objects.get_or_create(
                            user=request.user,
                            user_report=IncidentGeneral.objects.get(userid=userid),
                            generalid = generalid,
                            weather=weather,
                            light=light,
                            accident_factor=AccidentCausation.objects.get(category=accident_factor),
                            collision_type=CollisionType.objects.get(category=collision_type),
                            crash_type=CrashType.objects.get(crash_type=crash_type),
                            severity=severity,
                            movement_code=movement_code
                        )
                        
                        userremarks, created = IncidentRemark.objects.get_or_create(
                            incident_general = IncidentGeneral.objects.get(generalid=generalid),
                            responder=responder,
                            action_taken=action_taken
                        )
                        
                        
                        
                        if created:
                            IncidentGeneral.save()
                            usergeneral.save()
                            userremarks.save()
                messages.success(request, "The files has been uploaded to the database")
                            # return redirect('simple_upload')
                        
                        # else:
                        #     messages.error(request, "The files not uploaded to the database")
                        
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('simple_upload')
                    
            except IntegrityError as e:
                messages.error(request, str(e))
                return redirect('simple_upload')
                   
                
    except csv.Error as e:
        print(e)
        return redirect('simple_upload')
    

    return render(request, 'pages/super/input.html')
    
    # if request.method == 'POST':
    #     user_resource = IncidentGeneralResource()
    #     incident_general = IncidentGeneraltResource()
    #     incident_remark = IncidentRemarkResources()
        
        
    #     dataset = Dataset()
    #     new_IncidentGeneral = request.FILES['myfile']

    #     imported_data = dataset.load(new_IncidentGeneral.read(),format='xls')
    #     #print(imported_data)
    #     for data in imported_data:
    #         user_report_instance = IncidentGeneral.objects.get(userid=data[0])
    #         general_instance = IncidentGeneral.objects.get(generalid=data[0])
    #         value = IncidentGeneral(user=request.user, userid= data[0], date=data[1], description=data[2], address=data[3], latitude=data[4], longitude=data[5], status=data[6])
    #         value1= IncidentGeneral(user=request.user, user_report__userid=user_report_instance, generalid=data[0], weather=data[6],
    #                                 light=data[7], severity=data[8], movement_code=data[9])
    #         value2 = IncidentRemark(incident_general__generalid=general_instance, responder=data[10], action_taken=data[11])
    #         value.save()
    #         value1.save()
    #         value2.save()
    #         print(data[1])
    # return render(request, 'input.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_super)
def simple_upload_additional(request):
    data = None
    
    try:
        if request.method == 'POST':
            data = request.FILES['myfile']
            
            if not data.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return redirect('user_reports')
            
            else: 
                data = pd.read_csv(data, header=0, encoding="UTF-8", na_values=[' '])
                data = data.astype(object).where(pd.notnull(data), None)
                
            
            try:
                for index, rows in data.iterrows():
                
                    generalid = rows["User ID"]
                    incident_first_name = rows["First Name"]
                    incident_middle_name = rows["Middle Name"]
                    incident_last_name = rows["Last Name"]
                    incident_age = rows["Age"]
                    incident_gender = rows["Gender"]
                    incident_address = rows["Address"]
                    incident_involvement = rows["Involvement"]
                    incident_id_presented = rows["ID Presented"]
                    incident_id_number = rows["ID Number"]
                    incident_injury = rows["Injury"]
                    incident_driver_error = rows["Driver Error"]
                    incident_alcohol_drugs = rows["Alcohol/Drugs"]
                    incident_seatbelt_helmet = rows["Seatbelt/Helmet"]
                    classification = rows["Vehicle Classification"]
                    vehicle_type = rows["Vehicle Type"]
                    brand = rows["Brand"]
                    plate_number = rows["Plate Number"]
                    engine_number = rows["Engine Number"]
                    chassis_number = rows["Chassis Number"]
                    insurance_details = rows["Insurance Details"]
                    maneuver = rows["Maneuver"]
                    damage = rows["Damage"]
                    defect = rows["Defect"]
                    loading = rows["Loading"]
                    
                    rows.fillna(" ", inplace=True)
                
                    userperson, created = IncidentPerson.objects.get_or_create(
                        incident_general = IncidentGeneral.objects.get(generalid=generalid),
                        incident_first_name=incident_first_name,
                        incident_middle_name=incident_middle_name,
                        incident_last_name=incident_last_name,
                        incident_age=incident_age,
                        incident_gender=incident_gender,
                        incident_address=incident_address,
                        incident_involvement=incident_involvement,
                        incident_id_presented=incident_id_presented,
                        incident_id_number=incident_id_number,
                        incident_injury=incident_injury,
                        incident_driver_error=incident_driver_error,
                        incident_alcohol_drugs=incident_alcohol_drugs,
                        incident_seatbelt_helmet=incident_seatbelt_helmet,
                    )
                    

                    
                    uservehicle, created = IncidentVehicle.objects.get_or_create(
                        incident_general = IncidentGeneral.objects.get(generalid=generalid),
                        classification = classification,
                        vehicle_type=vehicle_type,
                        brand=brand,
                        plate_number=plate_number,
                        engine_number=engine_number,
                        chassis_number=chassis_number,
                        insurance_details=insurance_details,
                        maneuver=maneuver,
                        damage=damage,
                        defect=defect,
                        loading=loading,
                    )
                    
                    
                    
                    
                    if created:
                        userperson.save()
                        uservehicle.save()
                messages.success(request, "The files has been uploaded to the database")
                        
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('simple_upload_additional')
                    
            except IntegrityError as e:
                messages.error(request, str(e))
                return redirect('simple_upload_additional')
                    

    except csv.Error as e:
        print(e)
        return redirect('simple_upload_additional')


    return render(request, 'pages/super/input_additional.html')
    # if request.method == 'POST':
    #     incident_people = IncidentPeopleResources()
    #     incident_vehicle = IncidentVehicleResources()
    #     dataset = Dataset()
    #     new_IncidentGeneral = request.FILES['myfile']

    #     imported_data = dataset.load(new_IncidentGeneral.read(),format='xls')
    #     #print(imported_data)
    #     for data in imported_data:
    #         value = IncidentPerson(incident_first_name=data[0],
    #                                 incident_middle_name=data[1], incident_last_name=data[2], incident_age=data[3], incident_gender=data[4],
    #                                 incident_address=data[5], incident_involvement=data[6], incident_id_presented=data[7], incident_id_number=data[8],
    #                                 incident_injury=data[9], incident_driver_error=data[10], incident_alcohol_drugs=data[11], incident_seatbelt_helmet=data[12])
    #         value1 = IncidentVehicle(classification=data[13],
    #                                 vehicle_type=data[14], brand=data[15], plate_number=data[16],
    #                                 engine_number=data[17], chassis_number=data[18], insurance_details=data[19], maneuver=data[20],
    #                                 damage=data[21], defect=data[22], loading=data[23])
                                    
    #         value.save()
    #         value1.save()
    #         print(data[1])
    # return render(request, 'input_additional.html')
    
@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_simple_upload(request):
    data = None
    
    try:
        if request.method == 'POST':
            data = request.FILES['myfile']
            
            if not data.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return redirect('user_report')
            else: 
                data = pd.read_csv(data, header=0, encoding="UTF-8", na_values=[' '])
                data = data.astype(object).where(pd.notnull(data), None)
            try:
                for index, rows in data.iterrows():
                    
                        userid = rows["User ID"] 
                        generalid = rows["User ID"]
                        date = rows["Date"] if rows["Date"] else datetime.date.today()
                        time = rows["Time"]
                        description = rows["Description"] if rows["Description"] else " "
                        address = rows["Address"] if rows["Address"] else " "
                        latitude = rows["Latitude"] if rows["Latitude"] else " "
                        longitude = rows["Longitude"] if rows["Longitude"] else " "
                        status = rows["Status"] if rows["Status"] else " "
                        weather = rows["Weather"] if rows["Weather"] else " "
                        light = rows["Light"] if rows["Light"] else " "
                        accident_factor = rows["Accident Factor"] if rows["Accident Factor"] else " "
                        collision_type = rows["Collision Type"] if rows["Collision Type"] else " "
                        crash_type = rows["Crash"] if rows["Crash"] else " "
                        severity = rows["Severity"] if rows["Severity"] else " "
                        movement_code = rows["Movement Code"] if rows["Movement Code"] else " "
                        responder = rows["Responder"] if rows["Responder"] else " "
                        action_taken = rows["Action Taken"] if rows["Action Taken"] else " "
                    
                        # user_report_instance = IncidentGeneral.objects.get(userid=userid)
                        # general_instance = IncidentGeneral.objects.get(generalid=generalid)
                        
                        # get_or_create is used to eliminate forming or any duplicate record 
                        IncidentGeneral, created = IncidentGeneral.objects.get_or_create(
                            user=request.user,
                            userid=userid,
                            date=date,
                            time=time,
                            description=description,
                            address=address,
                            latitude=latitude,
                            longitude=longitude,
                            status=status
                        )
                        
                        usergeneral, created = IncidentGeneral.objects.get_or_create(
                            user=request.user,
                            user_report=IncidentGeneral.objects.get(userid=userid),
                            generalid = generalid,
                            weather=weather,
                            light=light,
                            accident_factor=AccidentCausation.objects.get(category=accident_factor),
                            collision_type=CollisionType.objects.get(category=collision_type),
                            crash_type=CrashType.objects.get(crash_type=crash_type),
                            severity=severity,
                            movement_code=movement_code
                        )
                        
                        userremarks, created = IncidentRemark.objects.get_or_create(
                            incident_general = IncidentGeneral.objects.get(generalid=generalid),
                            responder=responder,
                            action_taken=action_taken
                        )
                        
                        
                        
                        if created:
                            IncidentGeneral.save()
                            usergeneral.save()
                            userremarks.save()
                messages.success(request, "The files has been uploaded to the database")
                            # return redirect('simple_upload')
                        
                        # else:
                        #     messages.error(request, "The files not uploaded to the database")
                        
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('a_simple_upload')
                    
            except IntegrityError as e:
                messages.error(request, str(e))
                return redirect('a_simple_upload')
                   
                
    except csv.Error as e:
        print(e)
        return redirect('a_simple_upload')
    

    return render(request, 'pages/admin/a_input.html')
    
    # if request.method == 'POST':
    #     user_resource = IncidentGeneralResource()
    #     incident_general = IncidentGeneraltResource()
    #     incident_remark = IncidentRemarkResources()
        
        
    #     dataset = Dataset()
    #     new_IncidentGeneral = request.FILES['myfile']

    #     imported_data = dataset.load(new_IncidentGeneral.read(),format='xls')
    #     #print(imported_data)
    #     for data in imported_data:
    #         user_report_instance = IncidentGeneral.objects.get(userid=data[0])
    #         general_instance = IncidentGeneral.objects.get(generalid=data[0])
    #         value = IncidentGeneral(user=request.user, userid= data[0], date=data[1], description=data[2], address=data[3], latitude=data[4], longitude=data[5], status=data[6])
    #         value1= IncidentGeneral(user=request.user, user_report__userid=user_report_instance, generalid=data[0], weather=data[6],
    #                                 light=data[7], severity=data[8], movement_code=data[9])
    #         value2 = IncidentRemark(incident_general__generalid=general_instance, responder=data[10], action_taken=data[11])
    #         value.save()
    #         value1.save()
    #         value2.save()
    #         print(data[1])
    # return render(request, 'input.html')

@login_required(login_url = 'login')
@user_passes_test(check_role_admin)
def a_simple_upload_additional(request):
    data = None
    
    try:
        if request.method == 'POST':
            data = request.FILES['myfile']
            
            if not data.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return redirect('user_reports')
            
            else: 
                data = pd.read_csv(data, header=0, encoding="UTF-8", na_values=[' '])
                data = data.astype(object).where(pd.notnull(data), None)
                
            
            try:
                for index, rows in data.iterrows():
                
                    generalid = rows["User ID"]
                    incident_first_name = rows["First Name"]
                    incident_middle_name = rows["Middle Name"]
                    incident_last_name = rows["Last Name"]
                    incident_age = rows["Age"]
                    incident_gender = rows["Gender"]
                    incident_address = rows["Address"]
                    incident_involvement = rows["Involvement"]
                    incident_id_presented = rows["ID Presented"]
                    incident_id_number = rows["ID Number"]
                    incident_injury = rows["Injury"]
                    incident_driver_error = rows["Driver Error"]
                    incident_alcohol_drugs = rows["Alcohol/Drugs"]
                    incident_seatbelt_helmet = rows["Seatbelt/Helmet"]
                    classification = rows["Vehicle Classification"]
                    vehicle_type = rows["Vehicle Type"]
                    brand = rows["Brand"]
                    plate_number = rows["Plate Number"]
                    engine_number = rows["Engine Number"]
                    chassis_number = rows["Chassis Number"]
                    insurance_details = rows["Insurance Details"]
                    maneuver = rows["Maneuver"]
                    damage = rows["Damage"]
                    defect = rows["Defect"]
                    loading = rows["Loading"]
                    
                    rows.fillna(" ", inplace=True)
                
                    userperson, created = IncidentPerson.objects.get_or_create(
                        incident_general = IncidentGeneral.objects.get(generalid=generalid),
                        incident_first_name=incident_first_name,
                        incident_middle_name=incident_middle_name,
                        incident_last_name=incident_last_name,
                        incident_age=incident_age,
                        incident_gender=incident_gender,
                        incident_address=incident_address,
                        incident_involvement=incident_involvement,
                        incident_id_presented=incident_id_presented,
                        incident_id_number=incident_id_number,
                        incident_injury=incident_injury,
                        incident_driver_error=incident_driver_error,
                        incident_alcohol_drugs=incident_alcohol_drugs,
                        incident_seatbelt_helmet=incident_seatbelt_helmet,
                    )
                    

                    
                    uservehicle, created = IncidentVehicle.objects.get_or_create(
                        incident_general = IncidentGeneral.objects.get(generalid=generalid),
                        classification = classification,
                        vehicle_type=vehicle_type,
                        brand=brand,
                        plate_number=plate_number,
                        engine_number=engine_number,
                        chassis_number=chassis_number,
                        insurance_details=insurance_details,
                        maneuver=maneuver,
                        damage=damage,
                        defect=defect,
                        loading=loading,
                    )
                    
                    
                    
                    
                    if created:
                        userperson.save()
                        uservehicle.save()
                messages.success(request, "The files has been uploaded to the database")
                        
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('a_simple_upload_additional')
                    
            except IntegrityError as e:
                messages.error(request, str(e))
                return redirect('a_simple_upload_additional')
                    

    except csv.Error as e:
        print(e)
        return redirect('a_simple_upload_additional')


    return render(request, 'pages/admin/a_input_additional.html')
    # if request.method == 'POST':
    #     incident_people = IncidentPeopleResources()
    #     incident_vehicle = IncidentVehicleResources()
    #     dataset = Dataset()
    #     new_IncidentGeneral = request.FILES['myfile']

    #     imported_data = dataset.load(new_IncidentGeneral.read(),format='xls')
    #     #print(imported_data)
    #     for data in imported_data:
    #         value = IncidentPerson(incident_first_name=data[0],
    #                                 incident_middle_name=data[1], incident_last_name=data[2], incident_age=data[3], incident_gender=data[4],
    #                                 incident_address=data[5], incident_involvement=data[6], incident_id_presented=data[7], incident_id_number=data[8],
    #                                 incident_injury=data[9], incident_driver_error=data[10], incident_alcohol_drugs=data[11], incident_seatbelt_helmet=data[12])
    #         value1 = IncidentVehicle(classification=data[13],
    #                                 vehicle_type=data[14], brand=data[15], plate_number=data[16],
    #                                 engine_number=data[17], chassis_number=data[18], insurance_details=data[19], maneuver=data[20],
    #                                 damage=data[21], defect=data[22], loading=data[23])
                                    
    #         value.save()
    #         value1.save()
    #         print(data[1])
    # return render(request, 'input_additional.html')


