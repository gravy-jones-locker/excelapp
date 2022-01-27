from django.shortcuts import render
from django.http import JsonResponse
from webapp.models import Task
import time
from webapp import utils

def index(request):
    return render(request, 'index.html')

def upload(request, ftype: str):
    """Process uploaded files and return appropriate response"""
    time.sleep(5)
    return index(request)
    resp_body = {}
    try:
        status = 200
        Task.objects.rm_surplus()
        task = Task.objects.goc_from_form(
            id=request.POST.get('id'),
            ftype=ftype,
            fstream=request.FILES["file"])
        resp_body.update({"uploaded": task.get_ftypes(), "id": task.id})
        if task._is_ready():
            resp_body.update({"download": task.process()})
    except Exception as e:
        status = 201 #utils.handle_error(e)
    return JsonResponse(resp_body, status=status)      

def upload_adobe(request):
    return upload(request, 'adobe')

def upload_adserver(request):
    return upload(request, 'adserver')