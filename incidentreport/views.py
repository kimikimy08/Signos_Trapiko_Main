import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile, User
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_admin, check_role_super, check_role_member, check_role_super_admin
from incidentreport.models import UserReport, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
from django.contrib import messages
from .forms import UserReportForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm
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


@login_required(login_url='login')
@user_passes_test(check_role_member)
def my_report_add(request):

    form = UserReportForm(request.POST, request.FILES)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        User.objects.get(pk=request.user.pk)
        if form.is_valid():
            date = request.POST['date']
            time = request.POST['time']
            address = request.POST['address']
            description = request.POST['description']
            
            

            upload_photovideo = request.FILES.get('upload_photovideo')
            status = 1
            # user_report = form.save(commit=False)
            # user_report.user = get_user(request)
            # user_report.save()
            obj = UserReport.objects.create(user_id=request.user.pk, date=date, time=time, address=address,
                                            description=description, upload_photovideo=upload_photovideo, status=status)
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

TEMPLATES = {"information": "pages/incident_report_user.html",
                "general": "pages/incident_report_general1.html",
                "people": "pages/incident_report_people1.html",
                "vehicle": "pages/incident_report_vehicle1.html",
                "media": "pages/incident_report_media1.html",
                "remarks": "pages/incident_report_remarks1.html"}
class multistepformsubmission(SessionWizardView):


    # template_name = 'pages/incident_report.html'
    # form_list = [UserReportForm, IncidentGeneralForm, IncidentPersonForm, IncidentVehicleForm, IncidentMediaForm, IncidentRemarksForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media'))
    
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def done(self, form_list, **kwargs):
        # UserReport, IncidentGeneral, IncidentRemark, AccidentCausationSub, CollisionTypeSub, IncidentMedia, IncidentPerson, IncidentVehicle
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
        return HttpResponse('data saved successfully')

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
