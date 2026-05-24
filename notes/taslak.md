# 📄 TalentFlow Intelligence

### Proje Vizyonu

Sadece iş arama motoru değil; kullanıcının yeteneklerini analiz eden, eksiklerini
görselleştiren (Skill Tree), başvurularını bir Kanban panosunda yöneten, yapay zeka
ile mülakata hazırlayan ve **kullanıcının proje fikirlerine uygun teknoloji mimarisi
çizen** Bütünleşik Kariyer İşletim Sistemi.

## 1. Teknoloji Yığını (Tech Stack)

_Bu seçimler Python'ın veri gücünü, Django'nun ORM yeteneklerini, FOSS (Özgür Yazılım)
felsefesini ve dersin "Bonus" şartlarını maksimize eder._

- **Dil:** Python 3.10+
- **Web Framework:** Django 4+ (Zorunlu ORM, Admin Paneli ve Güvenlik için).
- **Veritabanı:** PostgreSQL (JSONB desteği, İlişkisel Yapı ve Render uyumu).
- **Arka Plan İşlemleri:** Django-Q2 (veya Celery) (SerpApi sorgularını kullanıcıyı
    bekletmeden yapmak için - Kritik Mühendislik).
- **AI & Logic:** LiteLLM Entegrasyonu (Model Agnostic yapı, CV Analizi, AI Mülakat, Tech Stack Önerisi).
    Mülakat Simülasyonu, Tech Stack Önerisi).
- **PDF Okuma:** opendataloader-pdf (CV dosyasından text çıkarma)
- **Frontend:** Django Templates + Bootstrap 5 (Hızlı UI) + Chart.js (Yetenek Ağacı Grafikleri) + HTMX & Alpine.js (SPA hissi veren etkileşimler) + **Sortable.js** (Kanban etkileşimleri).
- **DevOps:** Docker + GitHub Actions (CI/CD) + Render.com.

## 2. Veritabanı Mimarisi (Hibrit & İlişkisel)

_Dersin "N-N İlişki" ve "ORM Modelleme" şartlarına tam uyumlu, hibrit yapıyı koruyan
şema._


1. **Users (Kullanıcılar):** ID, Username, Email, TargetRole (örn: Backend Dev),
    CV_File (Yüklenen PDF).
**2.Jobs (İş İlanları) - HİBRİT YAPI:**
    - Alanlar: ID, Title, Company, Description, Source ('KAGGLE' |
       'LIVE_SERPAPI'), Posted Date.
    - _Strateji:_ Statik ve Canlı veri bu tabloda birleşir. Source kolonu ile
       ayrıştırılır.
3. **Skills (Yetenek Havuzu):** ID, Name (Python, Docker), Category.
    - **JobSkills (N-N):** Hangi ilan hangi yeteneği istiyor?
    - **UserSkills (N-N):** Kullanıcı hangi yeteneğe sahip? (+ Level 1-5).
**4.Applications (Başvuru Takip - Kritik N-N Tablosu):**
    - _Amaç:_ Kullanıcı ile İlanı bağlar, sürecin durumunu tutar.
    - Alanlar: ID, UserID (FK), JobID (FK), Status (Applied, Interview, Offer,
       Rejected), Notes.
**5.MockInterviews (Yapay Mülakat - AI Kaydı):**
    - _Amaç:_ AI mülakat geçmişini JSON olarak saklar.
    - Alanlar: ID, UserID (FK), JobID (FK), Questions (JSON), UserAnswers
       (JSON), Score (0-100).
6. **UserProjects (AI Portföy Mimarı - YENİ):**
    - _Amaç:_ Kullanıcının proje fikirlerini ve AI'ın önerdiği teknoloji yığınını
       saklar.
    - Alanlar: ID, UserID (FK), Idea (Text - Örn: "E-Ticaret Sitesi"),
       RecommendedStack (JSON - Önerilen Araçlar), Roadmap (JSON - Adım
       adım plan), CreatedAt.

## 3. Proje Klasör Yapısı (Django Clean Architecture)

_Django'nun standart yapısını, Business Logic (İş Mantığı) ile UI (Arayüz) birbirinden
ayrılacak şekilde düzenledik._


TalentFlow/
├── apps/ # (Public) Web ve API Katmanı (Views & URLs)
│ ├── accounts/ # Giriş, Kayıt, Profil Yönetimi
│ ├── jobs/ # İlan Listeleme, Detay Sayfası
│ ├── talent_models/ # Skill, Application, UserProject modelleri (Hibrit DB yapısı)
│ ├── dashboard/ # Skill Tree, Kanban Panosu ve **Proje Mimarı UI**
│ └── interviews/ # AI Mülakat Ekranı
│
├── core/ # (Private) İş Mantığı & Servisler (Framework Bağımsız)
│ ├── services/
│ │ ├── ingestion_service.py # SerpApi/Kaggle Veri Çekme Motoru
│ │ ├── matchmaking_service.py # Eşleştirme ve Gap Analysis Algoritması
│ │ ├── resume_parser.py # CV Okuma (PDF -> Text -> Skills)
│ │ └── ai_coach.py # LiteLLM Mülakat, Puanlama ve **Tech Stack Önerisi**
│ └── interfaces/
│
├── infrastructure/ # (Private) Dış Kaynaklar ve Veritabanı
│ ├── repositories/ # Django ORM Sorguları (Örn: JobRepository)
│ ├── serp_api/ # Google Jobs Client
│ └── ai_client/ # AI Client Wrapper (LiteLLM)
│
├── static/ # CSS, JS (Chart.js, HTMX, Alpine.js), Images
├── media/ # Kullanıcıların yüklediği CV dosyaları
├── templates/ # HTML Dosyaları
│ ├── dashboard/ # skill_tree.html, kanban.html, **architect.html**
│ ├── interviews/ # active_session.html
│ └── partials/ # Navbar, Footer, JobCard
├── config/ # Proje Ayarları (settings.py, urls.py, wsgi.py)
├── manage.py
├── requirements.txt
├── Dockerfile
└── .env # Gizli Anahtarlar (API Key)

## 4. Fonksiyonel Özellikler (Kayıpsız & Geliştirilmiş)

**A. Veri Motoru (Ingestion Engine)**

- **Statik:** Kaggle verisi temel eğitimi sağlar.
- **Canlı (Background Task):** Django-Q2, her gece SerpApi'den yeni ilanları çeker
    ve veritabanına LIVE etiketiyle ekler. Kullanıcı beklemez, veriler her sabah
    tazedir.
**B. Görsel Yetenek Analizi (Skill Tree)**
- **Resume Parsing:** Kullanıcı PDF CV yükler, sistem yetenekleri otomatik çeker
(UserSkills tablosuna yazar).


- **Gap Analysis:** "Senior Developer olmak için Python tamam ama Kubernetes
    eksik" analizi yapılır.
- **Görselleştirme:** Eksikler Chart.js ile bir "Radar Grafiği" (Skill Tree) olarak
    dashboard'da sunulur.
**C. Başvuru Takip Sistemi (ATS - Kanban)**
- **İşleyiş:** Kullanıcı ilanları "Başvurulacak", "Görüşüldü", "Reddedildi" sütunları
arasında sürükler.
- **Teknik:** Bu işlem HTMX ile arkada Applications tablosundaki Status alanını
günceller. Sayfa yenilenmez.
- **Değer:** Jüriye "Süreç Yönetimi" ve N-N ilişki kullanımını gösterir.
**D. AI Kariyer Koçu (Mock Interview)**
- **Senaryo:** Kullanıcı bir ilana özel "Mülakat Başlat" der.
- **AI İşlemi:** LiteLLM, ilanın açıklamasını okur ve o pozisyona uygun 3 teknik soru
üretir.
- **Simülasyon:** Kullanıcı cevapları yazar, AI cevapları puanlar (0-100) ve geri
bildirim yapar. Sonuç MockInterviews tablosuna kaydedilir.
**E. AI Portföy Mimarı (Portfolio Architect) - YENİ ÖZELLİK**
- **Senaryo:** Kullanıcı, aklındaki proje fikrini (örn: "E-Ticaret Sitesi") sisteme girer.
- **AI İşlemi:** Sistem, ai_coach.py servisi üzerinden kullanıcının hedefine en uygun
teknoloji yığınını (Tech Stack) oluşturur.
- **Hibrit Kural:** Sistem sektör standardını önerir (örn: AWS S3). Ancak eğer
önerilen araç FOSS değilse, yanına mutlaka FOSS alternatifini (örn: MinIO)
yazar.
- **Çıktı:** JSON formatında teknoloji listesi ve adım adım uygulama planı
kullanıcıya sunulur ve UserProjects tablosuna kaydedilir.

## 5. Geliştirme Yol Haritası (Sprint Planı)


- **1. Hafta:** Django kurulumu, PostgreSQL bağlantısı. User, Job, Skill, Application
    ve **UserProjects** modellerinin kodlanması.


- **2. Hafta:** Veri Motoru. Kaggle verisinin yüklenmesi ve Django-Q2 kurulumu
    (SerpApi arka plan görevi).
- **3. Hafta:** CV Yükleme ve Skill Tree. resume_parser servisinin yazımı ve Chart.js
    entegrasyonu.
- **4. Hafta:** ATS (Kanban) ve AI Entegrasyonu. Sürükle-bırak sistemi, Mülakat
    Simülasyonu ve **AI Portföy Mimarı (Architect)** özelliğinin ai_coach.py içine
    eklenmesi.
- **5. Hafta:** DevOps. Dockerize etme, GitHub Actions CI/CD yazımı ve Render
    deploy.

## 6. Kritik Kontrol Listesi (Checklist)

- [ ] **ORM Kuralı:** SQL yasak. Job.objects.filter(...) gibi Django ORM kullanılacak.
- [ ] **Repository Pattern:** View'lar (views.py) içinde veritabanı kodu olmayacak.
    Servis ve Repo katmanı kullanılacak.
- [ ] **Canlılık:** SerpApi entegrasyonu "Background Task" olarak çalışacak, kullanıcı
    arama yaparken API'ye gitmeyecek (Kota koruması).
- [ ] **Git Flow:** Her özellik için (örn: feature/portfolio-architect) yeni branch
    açılacak.
- [ ] **Gizlilik:** .env dosyası kullanılacak, API keyler repoya atılmayacak.
- [ ] **FOSS Hassasiyeti:** Önerilen araçlarda açık kaynak alternatifler daima
    belirtilecek.


