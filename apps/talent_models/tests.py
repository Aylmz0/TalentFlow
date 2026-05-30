
from django.test import Client, TestCase
from django.urls import reverse

from apps.jobs.models import Job  # Senin Job modelin buradan geliyor


class KanbanDBTest(TestCase):
    def setUp(self):
        # Test için geçici bir veri oluşturuyoruz
        self.job = Job.objects.create(
            company="Test Firması",
            title="Yazılım Stajyeri",
            status="basvuruldu"
        )
        self.client = Client()

    def test_status_update_works(self):
        # 1. Adım: views.py'da tanımladığımız adresi (URL) oluştur
        url = reverse('update_job_status', args=[self.job.id])
        
        # 2. Adım: HTMX'in atacağı POST isteğini simüle et
        response = self.client.post(url, {'status': 'mulakat'})
        
        # 3. Adım: Veritabanını tazele ve durumu kontrol et
        self.job.refresh_from_db()
        
        # 204 (No Content) yanıtı geldi mi ve statü değişti mi?
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.job.status, 'mulakat')