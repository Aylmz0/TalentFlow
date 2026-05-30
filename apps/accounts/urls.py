from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('cv-upload/', views.cv_upload, name='cv_upload'),
]
