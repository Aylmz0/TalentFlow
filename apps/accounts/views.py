from django.shortcuts import redirect
from django.contrib import messages

def index(request):
    return redirect('dashboard:skill_tree')

def cv_upload(request):
    if request.method == 'POST':
        messages.success(request, 'CV başarıyla yapay zeka analizine gönderildi (Simülasyon).')
    return redirect('dashboard:skill_tree')
