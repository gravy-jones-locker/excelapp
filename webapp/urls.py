from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_xls', views.upload_xls, name='upload_xls')
]