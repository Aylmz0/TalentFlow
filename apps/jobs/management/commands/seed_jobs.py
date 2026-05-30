import random
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.jobs.models import Job
from core.services.ingestion_service import IngestionService


class Command(BaseCommand):
    help = "Veritabanını SerpAPI veya yerel premium yedek ilanlarla doldurur."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("İş ilanları yükleme işlemi başlatılıyor..."))

        # 1. SerpAPI anahtarını kontrol et
        serpapi_key = getattr(settings, "SERPAPI_API_KEY", "")
        jobs_added = 0

        if serpapi_key:
            self.stdout.write(self.style.NOTICE("SerpAPI anahtarı algılandı, canlı ilanlar çekiliyor..."))
            ingestion = IngestionService(api_key=serpapi_key)
            # Python ve Software Developer ile ilgili ilanları çekiyoruz
            raw_jobs = ingestion.fetch_jobs(query="software developer")
            
            for item in raw_jobs:
                title = item.get("title", "Başlıksız İlan")
                company = item.get("company_name", "Bilinmeyen Şirket")
                description = item.get("description", "Detay bulunamadı.")
                
                # Durumu rastgele dağıtarak Kanban panosunda şık bir dağılım elde edelim
                random_status = random.choice(["basvuruldu", "mulakat", "teklif", "reddedildi"])
                
                _, created = Job.objects.get_or_create(
                    title=title,
                    company=company,
                    defaults={
                        "description": description,
                        "source": "LIVE_SERPAPI",
                        "status": random_status
                    }
                )
                if created:
                    jobs_added += 1
            
            if jobs_added > 0:
                self.stdout.write(self.style.SUCCESS(f"SerpAPI üzerinden {jobs_added} canlı iş ilanı başarıyla yüklendi!"))
                return

        # 2. API anahtarı yoksa veya SerpAPI'den ilan dönmediyse premium yerel ilanları yükle
        self.stdout.write(self.style.NOTICE("Statik premium yerel iş ilanları yükleniyor (Fallback)..."))
        
        static_jobs = [
            {
                "title": "Senior Python Backend Developer",
                "company": "TechFlow Solutions",
                "description": "Python, Django, PostgreSQL ve Redis teknolojileriyle yüksek ölçeklenebilir backend servisleri geliştirecek, REST API tasarımı ve mikroservis mimarisine hakim çalışma arkadaşı arıyoruz.",
                "status": "basvuruldu"
            },
            {
                "title": "React Frontend Engineer",
                "company": "Aura Digital",
                "description": "TypeScript, React, Next.js ve Tailwind CSS kullanarak modern, responsive ve premium kullanıcı arayüzleri geliştirecek yetenekli frontend geliştirici arıyoruz.",
                "status": "basvuruldu"
            },
            {
                "title": "Full Stack Software Developer",
                "company": "Initech Yazılım",
                "description": "Node.js (Express), React, MongoDB ve Docker teknolojilerini kullanarak uçtan uca modern web uygulamaları geliştirecek Full Stack çalışma arkadaşı arıyoruz.",
                "status": "mulakat"
            },
            {
                "title": "DevOps & Infrastructure Specialist",
                "company": "CloudSphere",
                "description": "Docker, Kubernetes, AWS bulut altyapısı, Terraform (IaC) ve GitHub Actions CI/CD süreçlerini yönetecek ve optimize edecek DevOps Mühendisi arıyoruz.",
                "status": "mulakat"
            },
            {
                "title": "Data Scientist & AI Engineer",
                "company": "Cyberdyne Intelligence",
                "description": "Python, TensorFlow, PyTorch ve Pandas kütüphaneleriyle yapay zeka modelleri eğitecek, LLM (Büyük Dil Modeli) entegrasyonları kuracak Data Scientist arıyoruz.",
                "status": "teklif"
            },
            {
                "title": "Mobile App Developer (Flutter)",
                "company": "Pixel Labs",
                "description": "Flutter ve Dart kullanarak hem iOS hem Android platformlarında premium tasarımlı ve akıcı mobil uygulamalar geliştirecek çalışma arkadaşları arıyoruz.",
                "status": "teklif"
            },
            {
                "title": "Go Backend & Systems Engineer",
                "company": "StreamGate",
                "description": "Go (Golang), gRPC, Apache Kafka ve Redis kullanarak yüksek performanslı gerçek zamanlı veri akış kuyrukları ve sistem backendleri geliştirecek mühendis arıyoruz.",
                "status": "reddedildi"
            },
            {
                "title": "Frontend Architect",
                "company": "Stark Industries",
                "description": "Next.js, TypeScript ve premium CSS mimarileriyle kurumsal web portalları geliştirecek ve frontend mimari standartlarını belirleyecek lider geliştirici arıyoruz.",
                "status": "reddedildi"
            },
            {
                "title": "QA Test Automation Engineer",
                "company": "Wayne Enterprises",
                "description": "Python, Selenium, Pytest ve Git kullanarak web uygulamalarının uçtan uca test otomasyon süreçlerini tasarlayacak ve sürdürecek QA Mühendisi arıyoruz.",
                "status": "basvuruldu"
            },
            {
                "title": "Java Spring Boot Developer",
                "company": "Massive Dynamic",
                "description": "Java, Spring Boot, Spring Security ve Hibernate/MySQL kullanarak mikroservis ekosisteminde güvenli ve ölçeklenebilir kurumsal backend uygulamaları geliştirecek mühendisler arıyoruz.",
                "status": "basvuruldu"
            }
        ]

        for item in static_jobs:
            _, created = Job.objects.get_or_create(
                title=item["title"],
                company=item["company"],
                defaults={
                    "description": item["description"],
                    "source": "KAGGLE",
                    "status": item["status"]
                }
            )
            if created:
                jobs_added += 1

        self.stdout.write(self.style.SUCCESS(f"Toplam {jobs_added} premium yerel iş ilanı başarıyla veritabanına yüklendi!"))
