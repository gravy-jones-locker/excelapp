from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_adobe', views.upload_adobe, name='upload_adobe'),
    path('upload_adserver', views.upload_adserver, name='upload adserver')
]