import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member, check_role_super_admin
from incidentreport.models import UserReport, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle, AccidentCausation, CollisionType, CrashType
from django.contrib import messages
from .forms import UserReportForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm, AccidentCausationForm, AccidentCausationSubForm, CollisionTypeForm, CollisionTypeSubForm, CrashTypeForm
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.forms.models import construct_instance


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = IncidentGeneral.objects.all()
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=1)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=2)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_reports_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = IncidentGeneral.objects.filter(status=3)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super_admin)
def user_report_delete(request, id=None):
    incidentReports = get_object_or_404(IncidentGeneral, id=id)
    #user_report = UserReport.objects.all()
    incidentReports.delete()
    return redirect('user_reports')



@user_passes_test(check_role_admin)
def user_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    incidentReports = IncidentGeneral.objects.all()
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def user_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=1)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def user_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=2)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def user_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=3)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/user_report.html', context)




@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_pending(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=1, user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_approved(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=2, user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_rejected(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    incidentReports = UserReport.objects.filter(status=3, user=request.user)
    context = {
        'profile': profile,
        'incidentReports': incidentReports,
    }
    return render(request, 'pages/member_myreport.html', context)


def my_report_delete(request, incident_id=None):
    incidentReports = UserReport.objects.get(pk=incident_id)
    incidentReports.delete()
    return redirect('my_report')


# @login_required(login_url='login')
# @user_passes_test(check_role_member)
# def my_report_add(request):

#     form = UserReportForm(request.POST, request.FILES)
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
#             obj = UserReport.objects.create(user_id=request.user.pk, date=date, time=time, address=address,
#                                             description=description, upload_photovideo=upload_photovideo, status=status)
#             obj.save()
#             messages.success(request, 'User Report added successfully!')
#             return redirect('my_report')

#         else:
#             print(form.errors)

#     else:
#         form = UserReportForm()
#     context = {
#         'form': form,
#         'profile': profile,

#     }
#     return render(request, 'pages/member_myreport_add.html', context)


def my_report_view(request, id):
    user_report = get_object_or_404(UserReport, pk=id)
    context = {
        'user_report': user_report,
    }

    return render(request, 'pages/member_myreport_view.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_edit(request, id):
    user_report = get_object_or_404(UserReport, pk=id)
    if request.method == 'POST':
        form = UserReportForm(request.POST or None,
                              request.FILES or None, instance=user_report)
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


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_delete(request, id):
    user_report = get_object_or_404(UserReport, pk=id)
    incident_general = get_object_or_404(IncidentGeneral, pk=id)
    incident_remark = get_object_or_404(IncidentRemark, pk=id)
    incident_remark.delete()
    incident_general.delete()
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
    return render(request, 'pages/incident_report_general.html', context)

def incident_report_people(request):
    if request.method == 'POST':
        user_report_form = UserReportForm(request.POST, request.FILES)
        inc_per_form = IncidentPersonForm(request.POST, request.FILES)
    else:
        user_report_form = UserReportForm()
        inc_per_form = IncidentPersonForm()
        print(user_report_form.errors)
        print(inc_per_form.errors)
        
    context = {
        'user_report_form': user_report_form,
        'inc_per_form': inc_per_form,
    }
    return render(request, 'pages/incident_report_people.html', context)

def incident_report_vehicle(request):
    if request.method == 'POST':
        user_report_form = UserReportForm(request.POST, request.FILES)
        inc_veh_form = IncidentVehicleForm(request.POST, request.FILES)

    else:
        user_report_form = UserReportForm()
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
        user_report_form = UserReportForm(request.POST, request.FILES)
        inc_med_form = IncidentMediaForm(request.POST, request.FILES)

    else:
        user_report_form = UserReportForm()
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
    #user_report = UserReport.objects.all()
    incidentReports.delete()
    return redirect('user_reports')


# AJAX
def load_accident(request):
    accident_factor_id = request.GET.get('accident_factor_id')
    collision_type_id = request.GET.get('collision_type_id')
    acc_subcat = AccidentCausationSub.objects.filter(accident_factor_id=accident_factor_id).all()
    col_subcat = CollisionTypeSub.objects.filter(collision_type_id=collision_type_id).all()
    context = {
        'acc_subcat': acc_subcat,
        'col_subcat': col_subcat
    }
    return render(request, 'incident/acc_sub_dropdown_list_options.html', context)
    #return JsonResponse(list(acc_subcat.values('id', 'sub_category')), safe=False)

def load_collision(request):
    collision_type_id = request.GET.get('collision_type_id')
    col_subcat = CollisionTypeSub.objects.filter(collision_type_id=collision_type_id).all()
    #return render(request, 'incident/acc_sub_dropdown_list_options.html', {'acc_subcat': acc_subcat})
    return JsonResponse(list(col_subcat.values('id', 'sub_category')), safe=False)


FORMS = [("information", UserReportForm),
        ("general", IncidentGeneralForm),
         ("people", IncidentPersonForm),
         ("vehicle",IncidentVehicleForm),
         ("media", IncidentMediaForm),
         ("remarks", IncidentRemarksForm)]

FORMS1 = [("information", UserReportForm)]

TEMPLATES = {"information": "pages/super/incident_report_user.html",
                "general": "pages/super/incident_report_general.html",
                "people": "pages/super/incident_report_people.html",
                "vehicle": "pages/super/incident_report_vehicle.html",
                "media": "pages/super/incident_report_media.html",
                "remarks": "pages/super/incident_report_remarks.html"}


TEMPLATES1 = {"information": "pages/admin/incident_report_user.html",
                "general": "pages/admin/incident_report_general.html",
                "people": "pages/admin/incident_report_people.html",
                "vehicle": "pages/admin/incident_report_vehicle.html",
                "media": "pages/admin/incident_report_media.html",
                "remarks": "pages/admin/incident_report_remarks.html"}

TEMPLATES2 = {"information": "pages/member/member_myreport_add.html"}


class multistepformsubmission(SessionWizardView):


    # template_name = 'pages/incident_report.html'
    # form_list = [UserReportForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        # UserReport, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
        profile = get_object_or_404(UserProfile, user=self.request.user)
        user_instance = UserReport()
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
        user_instance.status = 2
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
        context = {
            'profile': profile
        }
        return redirect('/userReports', context)

class multistepformsubmission_admin(SessionWizardView):
    

    # template_name = 'pages/incident_report.html'
    # form_list = [UserReportForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    
    def get_template_names(self):
        return [TEMPLATES1[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        # UserReport, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
        profile = get_object_or_404(UserProfile, user=self.request.user)
        user_instance = UserReport()
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
        user_instance.status = 2
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
        context = {
            'profile': profile
        }
        return redirect('/userReports', context)
    
class multistepformsubmission_member(SessionWizardView):
    

    # template_name = 'pages/incident_report.html'
    # form_list = [UserReportForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    
    def get_template_names(self):
        return [TEMPLATES2[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        # UserReport, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
        profile = get_object_or_404(UserProfile, user=self.request.user)
        user_instance = UserReport()
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
        context = {
            'profile': profile
        }
        return redirect('/incidentReport/incident', context)


def incident_report_general_view(request, id):
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    #user_instance = UserReport.objects.all()
    user_report = UserReport.objects.all()
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
    }

    return render(request, 'pages/incident_report_general_view.html', context)

def incident_report_people_view(request, id):
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    #user_instance = UserReport.objects.all()
    user_report = UserReport.objects.all()
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
    }

    return render(request, 'pages/incident_report_people_view.html', context)

def incident_report_vehicle_view(request, id):
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    #user_instance = UserReport.objects.all()
    user_report = UserReport.objects.all()
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
    }

    return render(request, 'pages/incident_report_vehicle_view.html', context)

def incident_report_media_view(request, id):
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    #user_instance = UserReport.objects.all()
    user_report = UserReport.objects.all()
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
    }

    return render(request, 'pages/incident_report_media_view.html', context)

def incident_report_remarks_view(request, id):
    general_instance = get_object_or_404(IncidentGeneral, pk=id)
    #user_instance = UserReport.objects.all()
    user_report = UserReport.objects.all()
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
    }

    return render(request, 'pages/incident_report_remarks_view.html', context)

def incident_report_general_edit(request, id=None):
    userreport =  get_object_or_404(UserReport, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    if request.method == 'POST':
        general_instance = IncidentGeneralForm(request.POST  or None, request.FILES  or None, instance=general)
        user_report = UserReportForm(request.POST  or None, request.FILES  or None,  instance=userreport)
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
        user_report = UserReportForm(instance=userreport)
    context = {
        'general_instance': general_instance,
        'user_report' : user_report,
        'general': general,
        'userreport': userreport
    }
    
    return render(request, 'pages/incident_report_general_edit.html', context)

# FORMS = [("information", UserReportForm),
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

def incident_report_people_edit(request, id=None):
    userreport =  get_object_or_404(UserReport, pk=id)
    general = get_object_or_404(IncidentGeneral, pk=id)
    person = get_object_or_404(IncidentPerson, pk=id)
    if request.method == 'POST':
        person_instance = IncidentPersonForm(request.POST  or None, request.FILES  or None, instance=person)
        if person_instance.is_valid():
            person_instance.save()
            messages.success(request, 'Profile updated')
            return redirect('user_reports')
        else:
            print(person_instance.errors)

    else:
        person_instance = IncidentPersonForm(instance=person)
    context = {
        'general': general,
        'person_instance' : person_instance,
        'userreport': userreport,
        'person': person
    }
    
    return render(request, 'pages/incident_report_people_edit.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def incident_form_super(request):
    attWizardView = multistepformsubmission.as_view(FORMS)
    return attWizardView(request)

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def incident_form_admin(request):
    attWizardView = multistepformsubmission_admin.as_view(FORMS)
    return attWizardView(request)

@login_required(login_url='login')
@user_passes_test(check_role_member)
def incident_form_member(request):
    attWizardView = multistepformsubmission_member.as_view(FORMS1)
    return attWizardView(request)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    accident_factor = AccidentCausation.objects.all()
    context = {
        'accident_factor': accident_factor,
        'profile':profile
    }
    return render(request, 'pages/super/accident_factor.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_accident_sub(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    accident_factor_sub = AccidentCausationSub.objects.filter(accident_factor=accident_factor)
    context = {
        'accident_factor': accident_factor,
        'accident_factor_sub': accident_factor_sub,
    }
    return render(request, 'pages/super/accident_factor_sub.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_crash(request):
    crash_type = CrashType.objects.all()
    context = {
        'crash_type': crash_type,
    }
    return render(request, 'pages/super/crash.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision(request):
    collision_type = CollisionType.objects.all()
    context = {
        'collision_type': collision_type,
    }
    return render(request, 'pages/super/collision_type.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_super)
def attributes_builder_collision_sub(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    collision_type_sub = CollisionTypeSub.objects.filter(collision_type=collision_type)
    context = {
        'collision_type': collision_type,
        'collision_type_sub': collision_type_sub,
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
                    messages.error(request, 'Duplicate Entries')
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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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
    #user_report = UserReport.objects.all()
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
                    messages.warning(request, 'Same Entries')
                    
                elif matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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
    #user_report = UserReport.objects.all()
    accident_factor_sub.delete()
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
                    messages.error(request, 'Duplicate Entries')
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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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
    #user_report = UserReport.objects.all()
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
                    messages.warning(request, 'Same Entries')
                    
                elif matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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
    return render(request, 'pages/admin/collision_type_add_sub.html', context)

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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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
    #user_report = UserReport.objects.all()
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
                    messages.error(request, 'Duplicate Entries')
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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
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
    #user_report = UserReport.objects.all()
    crash_type.delete()
    return redirect('attributes_builder_crash')




def attributes_builder_accident_admin(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    accident_factor = AccidentCausation.objects.all()
    context = {
        'accident_factor': accident_factor,
        'profile':profile
    }
    return render(request, 'pages/admin/accident_factor.html', context)

def attributes_builder_accident_sub_admin(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    accident_factor_sub = AccidentCausationSub.objects.filter(accident_factor=accident_factor)
    context = {
        'accident_factor': accident_factor,
        'accident_factor_sub': accident_factor_sub,
    }
    return render(request, 'pages/admin/accident_factor_sub.html', context)

def attributes_builder_crash_admin(request):
    crash_type = CrashType.objects.all()
    context = {
        'crash_type': crash_type,
    }
    return render(request, 'pages/admin/crash.html', context)

def attributes_builder_collision_admin(request):
    collision_type = CollisionType.objects.all()
    context = {
        'collision_type': collision_type,
    }
    return render(request, 'pages/admin/collision_type.html', context)

def attributes_builder_collision_sub_admin(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    collision_type_sub = CollisionTypeSub.objects.filter(collision_type=collision_type)
    context = {
        'collision_type': collision_type,
        'collision_type_sub': collision_type_sub,
    }
    return render(request, 'pages/admin/collision_type_sub.html', context)

def attributes_builder_accident_add_admin(request):
    if request.method == 'POST':
        form = AccidentCausationForm(request.POST)
        try:
            if form.is_valid():
                
                category = form.cleaned_data['category']
                
                matching_courses = AccidentCausation.objects.filter(category=category)
                if matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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

def attributes_builder_accident_edit_admin(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    if request.method == 'POST':
        form = AccidentCausationForm(request.POST or None,
                              request.FILES or None, instance=accident_factor)
        if form.is_valid():
            category = form.cleaned_data['category']
            matching_courses = AccidentCausation.objects.filter(category=category)
            if matching_courses:
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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

def attributes_builder_accident_delete_admin(request, id):
    accident_factor = get_object_or_404(AccidentCausation, pk=id)
    #user_report = UserReport.objects.all()
    accident_factor.delete()
    return redirect('attributes_builder_accident_admin')

def attributes_builder_accident_add_sub_admin(request):
    if request.method == 'POST':
        form = AccidentCausationSubForm(request.POST)
        try:
            if form.is_valid():
                accident_factor = form.cleaned_data['accident_factor']
                sub_category = form.cleaned_data['sub_category']
                matching_courses = AccidentCausationSub.objects.filter(accident_factor=accident_factor,sub_category=sub_category)
                if matching_courses:
                    messages.warning(request, 'Same Entries')
                    
                elif matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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

def attributes_builder_accident_delete_sub_admin(request, id):
    accident_factor_sub = get_object_or_404(AccidentCausationSub, pk=id)
    #user_report = UserReport.objects.all()
    accident_factor_sub.delete()
    return redirect('attributes_builder_accident_admin')

# COLLISION

def attributes_builder_collision_add_admin(request):
    if request.method == 'POST':
        form = CollisionTypeForm(request.POST)
        try:
            if form.is_valid():
                
                category = form.cleaned_data['category']
                
                matching_courses = CollisionType.objects.filter(category=category)
                if matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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

def attributes_builder_collision_edit_admin(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    if request.method == 'POST':
        form = CollisionTypeForm(request.POST or None,
                              request.FILES or None, instance=collision_type)
        if form.is_valid():
            category = form.cleaned_data['category']
            matching_courses = CollisionType.objects.filter(category=category)
            if matching_courses:
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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

def attributes_builder_collision_delete_admin(request, id):
    collision_type = get_object_or_404(CollisionType, pk=id)
    #user_report = UserReport.objects.all()
    collision_type.delete()
    return redirect('attributes_builder_collision_admin')

def attributes_builder_collision_add_sub_admin(request):
    if request.method == 'POST':
        form = CollisionTypeSubForm(request.POST)
        try:
            if form.is_valid():
                collision_type = form.cleaned_data['collision_type']
                sub_category = form.cleaned_data['sub_category']
                matching_courses = CollisionTypeSub.objects.filter(collision_type=collision_type, sub_category=sub_category)
                if matching_courses:
                    messages.warning(request, 'Same Entries')
                    
                elif matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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
    return render(request, 'pages/admin/collision_type_add_sub_admin.html', context)

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
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
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

def attributes_builder_collision_delete_sub_admin(request, id):
    collision_type_sub = get_object_or_404(CollisionTypeSub, pk=id)
    #user_report = UserReport.objects.all()
    collision_type_sub.delete()
    return redirect('attributes_builder_collision_admin')

def attributes_builder_crash_add_admin(request):
    if request.method == 'POST':
        form = CrashTypeForm(request.POST)
        try:
            if form.is_valid():
                
                crash_type = form.cleaned_data['crash_type']
                
                matching_courses = CrashType.objects.filter(crash_type=crash_type)
                if matching_courses.exists():
                    messages.error(request, 'Duplicate Entries')
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

def attributes_builder_crash_edit_admin(request, id):
    crash_type = get_object_or_404(CrashType, pk=id)
    if request.method == 'POST':
        form = CrashTypeForm(request.POST or None,
                              request.FILES or None, instance=crash_type)
        if form.is_valid():
            crash_types = form.cleaned_data['crash_type']
            matching_courses = CrashType.objects.filter(crash_type=crash_types)
            if matching_courses:
                messages.warning(request, 'Same Entries')
                
            elif matching_courses.exists():
                messages.error(request, 'Duplicate Entries')
            else:
                form.save()
                messages.success(request, 'Accident Factor Updated')
                return redirect('attributes_builder_crash_admin')
    else:
        form = CrashTypeForm(instance=crash_type)
    context = {
        'form': form,
        'crash_type': crash_type,
    }
    return render(request, 'pages/admin/crash_type_edit.html', context)

def attributes_builder_crash_delete_admin(request, id):
    crash_type = get_object_or_404(CrashType, pk=id)
    #user_report = UserReport.objects.all()
    crash_type.delete()
    return redirect('attributes_builder_crash_admin')

