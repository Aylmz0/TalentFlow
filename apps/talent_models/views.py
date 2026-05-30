
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

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