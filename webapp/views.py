from django.shortcuts import render
from django.http import JsonResponse
from webapp.models import Task
import time
import traceback as tb
from webapp import utils

def index(request):
    return render(request, 'index.html')

def upload(request, ftype: str):
    """Process uploaded files and return appropriate response"""
    time.sleep(2)
    resp_body = {}
    try:
        status = 200
        Task.objects.rm_surplus()
        task = Task.objects.goc_from_form(
            id=request.POST.get('id'),
            ftype=ftype,
            fstream=request.FILES["file"])
        ftypes = task.get_ftypes() 
        resp_body.update({"uploaded": ftypes, "id": task.id})
        if len(ftypes) == 2:
            resp_body.update({"download": task.process().decode()})
    except Exception as e:
        tb.print_exc()
        status = utils.handle_error(e)
    return JsonResponse(resp_body, status=status)      

def upload_adobe(request):
    return upload(request, 'adobe')

def upload_adserver(request):
    return upload(request, 'adserver')