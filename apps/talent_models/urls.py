
from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    # Bu satır, kartın ID'sini alıp views içindeki fonksiyona bağlar
    path('update-status/<int:pk>/', views.update_job_status, name='update_job_status'),
    path('skill-tree/', views.skill_tree, name='skill_tree'),
    path('kanban/', views.kanban, name='kanban'),
]