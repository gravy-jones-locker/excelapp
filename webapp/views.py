from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import time
from webapp.models import UploadFile

# Create your views here.

def index(request):

    """Render homepage in applicable state"""

    return render(request, 'index.html', {'status': 'processed'})

def upload_xls(request):

    """Upload file and create record"""

    time.sleep(2)  # Hacky way to allow animation to complete

    try:
        # Stop the stored files/records from breaching the limit
        UploadFile.objects.rm_surplus()
        
        xls = request.FILES['file']
        xls_db = UploadFile.objects.create(content=xls).process()

        return JsonResponse({'fname': xls_db.fname}, status=200)

    except:
        return HttpResponse(status=201)