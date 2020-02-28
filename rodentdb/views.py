from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rodentdb.admin import RodentResource
import csv
from django.http import HttpResponse

# Create your views here.
@login_required
def get_rodent_template(request):
    rodent_resource = RodentResource()
    dataset = rodent_resource.export()
    
    # prepare response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rodent_template.csv"'

    csv_list = dataset.csv.rstrip().split(',')

    writer = csv.writer(response)
    writer.writerow(csv_list)

    return response