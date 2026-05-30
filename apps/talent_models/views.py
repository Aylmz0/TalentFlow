
# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from apps.jobs.models import Job
from apps.talent_models.models import UserSkill


def update_job_status(request, pk):
    if request.method == "POST":
        # HTMX tarafından gönderilen yeni durumu (status) alıyoruz
        new_status = request.POST.get('status')
        
        # İlgili iş kaydını ID (pk) üzerinden buluyoruz
        job = get_object_or_404(Job, pk=pk)
        
        # Veritabanında güncelleme yapıp kaydediyoruz
        job.status = new_status
        job.save()
        
        # Sayfanın yenilenmesine gerek olmadığı için "İçerik Yok" (204) dönüyoruz
        return HttpResponse(status=204)




def skill_tree(request):
    user_skills = []
    skill_names_json = json.dumps([])
    skill_levels_json = json.dumps([])
    overall_score = 0
    has_skills = False

    if request.user.is_authenticated:
        user_skills = UserSkill.objects.filter(user=request.user).select_related('skill').order_by('-level')
        if user_skills.exists():
            names = [us.skill.name.upper() for us in user_skills]
            levels = [us.level * 20 for us in user_skills]  # 1-5 seviyeleri → 20-100 aralığına çevrilir
            overall_score = round(sum(levels) / len(levels))
            skill_names_json = json.dumps(names)
            skill_levels_json = json.dumps(levels)
            has_skills = True

    return render(request, 'dashboard/skill_tree.html', {
        'user_skills': user_skills,
        'skill_names_json': skill_names_json,
        'skill_levels_json': skill_levels_json,
        'overall_score': overall_score,
        'has_skills': has_skills
    })

def kanban(request):
    # Eğer veritabanında hiç iş ilanı yoksa, otomatik olarak seed_jobs çalıştır
    if Job.objects.count() == 0:
        from django.core.management import call_command
        try:
            call_command('seed_jobs')
        except Exception as e:
            print("Kanban otomatik veri yükleme hatası:", e)

    jobs = Job.objects.all().order_by('-posted_date')
    context = {
        'basvuruldu': jobs.filter(status='basvuruldu'),
        'mulakat': jobs.filter(status='mulakat'),
        'teklif': jobs.filter(status='teklif'),
        'reddedildi': jobs.filter(status='reddedildi'),
    }
    return render(request, 'dashboard/kanban.html', context)


def start_interview(request, job_pk):
    return HttpResponse("Mock Interview Page Placeholder")


def submit_interview(request, interview_pk):
    return HttpResponse("Submit Interview Placeholder")