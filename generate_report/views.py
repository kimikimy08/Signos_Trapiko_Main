import datetime
from django.shortcuts import render  
from django.http import HttpResponse 
from django.contrib.auth.models import User
import xlwt
from accounts.models import UserProfile, User
from incidentreport.models import AccidentCausationSub, AccidentCausation,IncidentGeneral
import pytz
from django.db.models import Count, Sum
from django.db.models import Q


# Create your views here.
def generate_report(request):
    return render(request, 'pages/generate_report.html')

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')
    
    alignment = xlwt.Alignment()

    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
 
    # Sheet header, first row
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    header_font = xlwt.Font()

    # Header font preferences
    header_font.name = 'Times New Roman'
    header_font.height = 20 * 15
    header_font.bold = True

    # Header Cells style definition
    header_style = xlwt.XFStyle()
    header_style.font = header_font 


    body_font = xlwt.Font()

    # Body font preferences
    body_font.name = 'Arial'
    body_font.italic = True


    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    header_style.borders = borders
    
    # body cell name style definition
    body_style = xlwt.XFStyle()
    body_style.font = body_font 
    
    
 
    columns = ['Username', 'First name', 'Middle name', 'Last name', 'Email address', 'Mobile Number', 'Birthday', 'Role', 'Status', 'Last Login', 'Created At', 'Updated At']
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], header_style)
        ws.col(col_num).width = 7000

        
 
    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()
 
    rows = UserProfile.objects.all().values_list('user__username', 'user__first_name', "user__middle_name",'user__last_name', 'user__email', 'user__mobile_number', 'birthdate', 'user__role', 'user__status', 'user__last_login', 'created_at', 'updated_at').order_by('-user__last_login')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], body_style)
 
    wb.save(response)
    return response


def export_accidentcausation_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="accident_causation.xls"'
 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Accident Causation')
    
    alignment = xlwt.Alignment()

    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
 
    # Sheet header, first row
    row_num = 0
 
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    header_font = xlwt.Font()

    # Header font preferences
    header_font.name = 'Times New Roman'
    header_font.height = 20 * 15
    header_font.bold = True

    # Header Cells style definition
    header_style = xlwt.XFStyle()
    header_style.font = header_font 


    body_font = xlwt.Font()

    # Body font preferences
    body_font.name = 'Arial'
    body_font.italic = True


    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    header_style.borders = borders
    
    # body cell name style definition
    body_style = xlwt.XFStyle()
    body_style.font = body_font 
    
    
 
    columns = ['Accident Factor', 'Damage to Property', 'Fatal', 'Non-Fatal Injury']
 
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], header_style)
        ws.col(col_num).width = 7000

        
 
    # Sheet body, remaining rows
    # font_style = xlwt.XFStyle()
    # rows1 = AccidentCausation.objects.all()

#     rows = IncidentGeneral.objects.all().values('accident_factor__category')
#     rows = rows.annotate(
#         severity1=Count('severity', only=Q(severity=1)),
#    severity2=Count('severity', only=Q(severity=2)),
#   severity3=Count('severity', only=Q(severity=3))
# #     )
    distinct_articles = AccidentCausation.objects.distinct('category')
    rows = IncidentGeneral.objects.all().values_list('accident_factor__category', 'accident_subcategory')
    rows = rows.annotate(
         severity1=Count('severity', only=Q(1)),
        severity2=Count('severity', only=Q(2)),
        severity3=Count('severity', only=Q(3))
    )
    

    # rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], body_style)
    
    # queryset = IncidentGeneral.objects.all().values('accident_factor')
    # queryset = queryset.annotate(
    #     severity1=Count('severity', only=Q(severity=1)),
    #     severity2=Count('severity', only=Q(severity=2)),
    #     severity3=Count('severity', only=Q(severity=3))
    # )

    # for item in queryset:
    #     print( item.severity1, item.severity2, item.severity3)
 
    wb.save(response)
    return response