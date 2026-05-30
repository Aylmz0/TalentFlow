
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.jobs.models import Job  # Modelin bulunduğu doğru yol


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
    return render(request, 'dashboard/skill_tree.html')

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