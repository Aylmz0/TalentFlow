# TalentFlow - Gorev Listesi

Bu dosya, Jira'da verilecek gorevleri tutar. Icerik degistirilmemistir.

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
