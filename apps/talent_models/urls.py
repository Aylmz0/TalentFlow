
from django.urls import path
from . import views

urlpatterns = [
    # Bu satır, kartın ID'sini alıp views içindeki fonksiyona bağlar
    path('update-status/<int:pk>/', views.update_job_status, name='update_job_status'),
]