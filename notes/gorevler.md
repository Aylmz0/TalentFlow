# TalentFlow - Gorev Listesi

Bu dosya, Jira'da verilecek gorevleri ve ekip sorumluluklarini tutar.

## **Epic Listesi ve Sorumlular (Owner)**
| Epic Kod | Epic Basligi (Jira Ismi) | Sorumlu (Owner) |
| :--- | :--- | :--- |
| **TAL-2** | Altyapi, DB ve Mimari | Abdullah Yilmaz |
| **TAL-3** | Veri Motoru ve AI Servis Mantigi | Ali Alper Tas |
| **TAL-4** | UI/UX ve Veri Gorsellestirme | Umut Can Kus |
| **TAL-5** | DevOps, Docker ve Dagitim | Abdullah Yilmaz |

---

# 1. Hafta (Tamamlandi)

## TASK 1
**Atanan:** Abdullah Yilmaz
**Baslik:** Proje Temel Klasor Mimarisinin Kurulmasi

**Aciklama:** uv kullanilarak Django projesi baslatilacak, Ruff konfigurasyonu yapilacak ve Clean Architecture klasor mimarisi (apps, core, infrastructure) olusturulacak.

---

# 2. Hafta

## TASK 2
**Atanan:** Abdullah Yilmaz (Lead Architect)
**Epic:** TAL-2 Altyapi, DB ve Mimari
**Baslik:** Custom User ve DB Setup

**Aciklama:** Projenin temel PostgreSQL baglantisinin yapilmasi ve Custom User modelinin Django auth sistemine entegre edilmesi.

**Alt Gorevler:**

- **ST-1:** DB ve App Ayarlari
- **ST-2:** User Modeli
- **ST-3:** Auth Ayarı

---

## TASK 3
**Atanan:** Ali Alper Tas (AI & Data Engineer)
**Epic:** TAL-3 Veri Motoru ve AI Servis Mantigi
**Baslik:** Kaggle Ingester Iskeleti

**Aciklama:** Kaggle CSV verilerini veritabanina aktarmak icin kullanilacak Django Management Command'in teknik iskeletinin olusturulmasi.

**Alt Gorevler:**

- **ST-1:** Klasor Yapisi
- **ST-2:** Command Iskeleti
- **ST-3:** AI Client Kurulumu

---

## TASK 4
**Atanan:** Umut Can Kus (Frontend Developer)
**Epic:** TAL-4 UI/UX ve Veri Gorsellestirme
**Baslik:** Base HTML ve Static Setup

**Aciklama:** Tum web sayfalarinin temelini olusturacak base.html sablonunun kurulmasi ve Bootstrap 5 kutuphanesinin projeye dahil edilmesi.

**Alt Gorevler:**

- **ST-1:** Static/Media Ayarı
- **ST-2:** Base HTML
- **ST-3:** Content Block

---

# 3. Hafta

## TASK 5
**Atanan:** Abdullah Yilmaz (Lead Architect)
**Epic:** TAL-2 Altyapi, DB ve Mimari
**Baslik:** Job, Skill ve Iliskili Tablolarin Olusturulmasi

**Etkilenecek Klasor/Dosyalar:**
- apps/jobs/models.py
- apps/talent_models/models.py
- config/settings.py

**Kurulmasi Gereken Kutuphane:** opendataloader-pdf

**Alt Gorevler:**

- **ST-1:** Kutuphane Kurulumu
  - opendataloader-pdf kutuphanesini kur ve requirements.txt guncelle

- **ST-2:** Job Modeli
  - apps/jobs/models.py dosyasina Job modeli ekle

- **ST-3:** Skill ve Iliski Modelleri
  - apps/talent_models/models.py dosyasina Skill, JobSkill, UserSkill modelleri ekle

- **ST-4:** Application ve UserProject Modelleri
  - apps/talent_models/models.py dosyasina Application ve UserProject modelleri ekle
  - config/settings.py icine apps.talent_models ekle

---

## TASK 6
**Atanan:** Ali Alper Tas (AI & Data Engineer)
**Epic:** TAL-3 Veri Motoru ve AI Servis Mantigi
**Baslik:** Resume Parser ve Matchmaking Servisleri

**Etkilenecek Klasor/Dosyalar:**
- core/services/resume_parser.py
- core/services/matchmaking_service.py

**Alt Gorevler:**

- **ST-1:** Resume Parser
  - core/services/resume_parser.py dosyasina opendataloader-pdf kullanarak PDF okuyup skill cikaran fonksiyonu yaz

- **ST-2:** Matchmaking Service
  - core/services/matchmaking_service.py dosyasina skill karsilastirma ve gap analysis fonksiyonlarini yaz

---

## TASK 7
**Atanan:** Umut Can Kus (Frontend Developer)
**Epic:** TAL-4 UI/UX ve Veri Gorsellestirme
**Baslik:** CV Upload Form ve Skill Tree Dashboard

**Etkilenecek Klasor/Dosyalar:**
- templates/base.html
- templates/dashboard/skill_tree.html
- apps/accounts/views.py
- apps/accounts/urls.py
- config/settings.py

**Kullanilacak Kutuphaneler:** Bootstrap 5, HTMX, Alpine.js, Chart.js

**Alt Gorevler:**

- **ST-1:** CV Upload Form
  - templates/base.html dosyasini olustur (Bootstrap, HTMX, Alpine.js CDN ekle)
  - apps/accounts/views.py ve urls.py dosyalarina CV upload islevi ekle
  - config/settings.py icine MEDIA_URL ve MEDIA_ROOT ekle

- **ST-2:** Skill Tree Dashboard
  - templates/dashboard/skill_tree.html dosyasini olustur (Chart.js radar grafik ile birlikte)

---

# 4. Hafta

## TASK 8
**Atanan:** Abdullah Yilmaz (Lead Architect)
**Epic:** TAL-2 Altyapi, DB ve Mimari
**Baslik:** Repository Katmani, AI Veri Kaydi ve Bagimlilik Yonetimi

**Aciklama:** Clean Architecture geregi veritabani sorgularinin repository katmanina tasinmasi, AI ciktilarinin JSONField olarak kaydedilmesi ve yeni kutuphanelerin (LiteLLM, Django-Q2) requirements.txt dosyasina eklenmesi.

**Etkilenecek Klasor/Dosyalar:**
- infrastructure/repositories/application_repository.py
- infrastructure/repositories/interview_repository.py
- apps/talent_models/models.py
- requirements.txt

**Alt Gorevler:**

- **ST-1:** Bagimlilik Yonetimi (LiteLLM, Django-Q2 ve PDF Parsing)
  - LiteLLM, Django-Q2 ve opendataloader-pdf kutuphanelerini kur ve requirements.txt dosyasini guncelle

- **ST-2:** Repository Katmaninin Kurulmasi
  - infrastructure/repositories/ altinda Application ve MockInterview repo siniflarini ekle

- **ST-3:** AI Veri Kaliciligi ve Kaydi
  - MockInterviews ve UserProjects modellerine LiteLLM ciktilarinin kaydedilmesi icin save mantigini guncelle

---

## TASK 9
**Atanan:** Ali Alper Tas (AI & Data Engineer)
**Epic:** TAL-3 Veri Motoru ve AI Servis Mantigi
**Baslik:** AI Coach Mantigi ve Arka Plan Gorevleri

**Aciklama:** LiteLLM entegrasyonu ile mulakat sorusu uretimi ve AI Portfolyo Mimari (Tech Stack onerisi) mantiginin kurulmasi; SerpApi islerinin arka plana aktarilmasi.

**Etkilenecek Klasor/Dosyalar:**
- core/services/ai_coach.py
- core/services/ingestion_service.py
- config/settings.py

**Alt Gorevler:**

- **ST-1:** AI Coach ve Portfolyo Mimari Mantigi
  - core/services/ai_coach.py icine Mock Interview ve Tech Stack onerisi ureten LiteLLM fonksiyonlarini ekle

- **ST-2:** AI Destekli Yetenek Ayiklama (Resume Parsing)
  - opendataloader-pdf ile cikarilan ham metnin LiteLLM yardimiyla analiz edilip UserSkills tablosuna islenmesi

- **ST-3:** Arka Plan Gorevleri Yapilandirmasinin Tamamlanmasi
  - Django-Q2 paketini kullanarak settings.py ayarlarini yap ve SerpApi gorevini arka plana ata

---

## TASK 10
**Atanan:** Umut Can Kus (Frontend Developer)
**Epic:** TAL-4 UI/UX ve Veri Gorsellestirme
**Baslik:** ATS Kanban Panosu ve Alpine.js Etkilesimi

**Aciklama:** Basvuru takip panelinin (Kanban) UI tasarimi ve HTMX/Alpine.js ile surukle-birak kart tasima ozelliginin eklenmesi.

**Etkilenecek Klasor/Dosyalar:**
- templates/dashboard/kanban.html
- static/js/kanban_logic.js

**Alt Gorevler:**

- **ST-1:** Kanban Arayuz Tasarimi
  - templates/dashboard/kanban.html dosyasini Bootstrap Grid kullanarak olustur

- **ST-2:** Surukle-Birak ve HTMX Etkilesimi
  - Alpine.js ve Sortable.js ile sutunlar arasi kart tasima ve HTMX ile statu guncelleme mantigini kur

---

# 5. Hafta

## TASK 11
**Atanan:** Abdullah Yilmaz (Lead Architect)
**Epic:** TAL-5 DevOps, Docker ve Dagitim
**Baslik:** Dockerize Etme ve CI/CD Pipeline Kurulumu

**Aciklama:** Projenin dockerize edilmesi ve GitHub Actions ile otomatik test/deploy sureclerinin kurulmasi.

**Etkilenecek Klasor/Dosyalar:**
- Dockerfile
- docker-compose.yml
- .github/workflows/main.yml

**Alt Gorevler:**

- **ST-1:** Docker Yapilandirmasi
  - Dockerfile ve docker-compose.yml (App, DB, Redis/Worker) dosyalarini production-ready hazirla

- **ST-2:** Canli Ortam Bagimliliklarinin Finalize Edilmesi
  - Gunicorn ve psycopg2-binary gibi canli ortam paketlerini requirements.txt dosyasina ekle

- **ST-3:** GitHub Actions CI/CD Akislarinin Hazirlanmasi
  - .github/workflows/main.yml dosyasini lint, test ve Render.com deploy adimlariyla kur

---

## TASK 12
**Atanan:** Ali Alper Tas (AI & Data Engineer)
**Epic:** TAL-3 Veri Motoru ve AI Servis Mantigi
**Baslik:** AI Model Optimizasyonu ve Sistem Entegrasyonu

**Aciklama:** AI promptlarinin finalize edilmesi ve tum AI servislerinin pipeline uzerinde tutarlilik kontrolleri (LiteLLM).

**Etkilenecek Klasor/Dosyalar:**
- core/services/ai_coach.py
- infrastructure/ai_client/

**Alt Gorevler:**

- **ST-1:** Prompt Iyilestirmesi ve Cikti Standardizasyonu
  - LiteLLM promptlarini daha tutarli ve JSON formatina uygun yanit verecek sekilde finalize et

- **ST-2:** Sistem Genel Entegrasyon Kontrolleri
  - Tum AI servislerinin (CV -> Parsing -> Gap -> Interview) veritabanı ile entegre calistigini dogrula

---

## TASK 13
**Atanan:** Umut Can Kus (Frontend Developer)
**Epic:** TAL-4 UI/UX ve Veri Gorsellestirme
**Baslik:** UX Denetimi ve Final Cilalama

**Aciklama:** Responsive kontrolleri ve veri olmayan sayfalar icin hata/yukleme durumlarinin gorsellestirilmesi.

**Etkilenecek Klasor/Dosyalar:**
- templates/base.html
- static/css/custom_polish.css

**Alt Gorevler:**

- **ST-1:** Responsive ve Mobil Uyumluluk Kontrolleri
  - Mobil ve tablet gorunumlerindeki UI hatalarini Bootstrap utilitileriyle gider

- **ST-2:** Hata ve Bos Durum (Empty State) Tasarimlari
  - Veri olmayan ilan listeleri veya bos dashboardlar icin "Empty State" tasarimlarini ekle

---

# 6. Hafta (Final Cilalama ve Pürüzlerin Giderilmesi)

## TASK 14
**Atanan:** Umut Can Kus (Frontend Developer)
**Epic:** TAL-4 UI/UX ve Veri Gorsellestirme
**Baslik:** UI/UX Puruzlerinin Giderilmesi ve Gorsel Iyilestirmeler

**Aciklama:** Umut'a ait olan UI arayuzundeki tum puzurlerin giderilmesi, responsive uyumluluk, gecis animasyonlari, form alanlarindaki dogrulama hata gosterimleri ve genel gorsel estetigin premium duzeye cikarilmasi.

**Etkilenecek Klasor/Dosyalar:**
- templates/base.html
- templates/dashboard/
- static/css/

**Alt Gorevler:**

- **ST-1:** Arayuz Puruzlerinin ve Hizalamalarin Giderilmesi
  - Responsive ve hizalama hatalarinin tum sayfalarda ve farkli ekran boyutlarinda giderilmesi
- **ST-2:** Form Dogrulamalari ve Feedback Arayuzleri
  - CV yukleme ve form islemlerinde yukleme (spinner/loading) ve hata geri bildirimlerinin (toast/alert) eklenmesi
- **ST-3:** Estetik ve Gecis Efektleri
  - Buton hover animasyonlari, modern kart tasarimlarinin cilalanmasi ve mikro-etkilesimlerin finalize edilmesi

---

## TASK 15
**Atanan:** Ali Alper Tas (AI & Data Engineer)
**Epic:** TAL-3 Veri Motoru ve AI Servis Mantigi
**Baslik:** Backend & AI Puruzlerinin Giderilmesi ve Prompt Optimizasyonu

**Aciklama:** Alper'in backend tarafindaki AI (LiteLLM) entegrasyonu puruzlerinin giderilmesi, prompt yanitlarinin tutarliliginin artirilmasi, JSON veri formatlarinin guvenli parse edilmesi ve API hata yonetimi.

**Etkilenecek Klasor/Dosyalar:**
- core/services/ai_coach.py
- apps/talent_models/models.py
- infrastructure/repositories/

**Alt Gorevler:**

- **ST-1:** LiteLLM Promptlarinin Son Haline Getirilmesi
  - Mulakat sorulari ve gap analysis promptlarinin kalitesini ve JSON yanit tutarliligini artiracak sekilde optimize edilmesi
- **ST-2:** Hata Yakalama ve Exception Handling
  - AI API servislerinin yavas yanit vermesi veya yanit vermemesi (timeout) durumlarinda uygulamanin cokmesini onleyecek try-except bloklarinin tamamlanmasi
- **ST-3:** JSON Veri Pars Etme ve Kayit Optimizasyonu
  - Veritabanina kaydedilecek AI ciktilarinin JSON formatlarinin guvenli sekilde parse edilmesi ve kayit mantiginin optimize edilmesi

