
from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [  # type: ignore[var-annotated]
    path('update-status/<int:pk>/', views.update_job_status, name='update_job_status'),  # type: ignore
    path('skill-tree/', views.skill_tree, name='skill_tree'),
    path('kanban/', views.kanban, name='kanban'),
    path('interview/start/<int:job_pk>/', views.start_interview, name='start_interview'),
    path('interview/submit/<int:interview_pk>/', views.submit_interview, name='submit_interview'),
    path('architect/', views.architect, name='architect'),
    path('project-ideas/', views.project_ideas, name='project_ideas'),
    path('cv-improve/', views.cv_improve, name='cv_improve'),
]