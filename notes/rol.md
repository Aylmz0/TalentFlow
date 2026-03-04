# TalentFlow Intelligence - Ekip Rolleri ve Sorumluluk Dağılımı

---

## 1. Lead Architect & Project Manager (PM)
**Rol Sahibi:** [Abdullah Yılmaz]
**Odak Noktası:** Proje Omurgası, Veritabanı Mimarisi, DevOps ve Güvenlik.

**Ana Sorumluluklar:**
*Veritabanı (DB):* N-N ilişkili hibrit yapıya uygun olarak `Users`, `Jobs`, `Skills`, `Applications`, `MockInterviews` ve `UserProjects` modellerini (ORM) tasarlamak.
*Altyapı:* Django 4+ proje ayarlarını (`config/` klasörü) kurmak ve API anahtarları için `.env` gizliliğini sağlamak.
*DevOps:* GitHub Actions (CI/CD) süreçlerini yazmak, projeyi Dockerize etmek (`Dockerfile`) ve Render.com üzerinde canlıya almak.

**Odaklanılması Gereken Klasörler ve Teknolojiler:**
*Klasörler:* `config/`, `infrastructure/repositories/`, `apps/` altındaki tüm `models.py` dosyaları.
*Teknolojiler:* Python 3.10+, Django 4+, PostgreSQL (JSONB desteği).

---

## 2. AI & Data Engineer
**Rol Sahibi:** [Ali Alper Taş]
**Odak Noktası:** İş Mantığı (Business Logic), AI Entegrasyonu ve Arka Plan Servisleri.

**Ana Sorumluluklar:**
*Veri Motoru (Ingestion):* Statik Kaggle verisini içeri almak ve Django-Q2 ile arka planda çalışarak her gece SerpApi üzerinden yeni ilan çeken `ingestion_service.py` dosyasını yazmak.
*Görsel Analiz Motoru:* Yüklenen PDF'i okuyan `resume_parser.py` ve eksik yetenekleri bulan (Gap Analysis) `matchmaking_service.py` servislerini yazmak.
*AI Kariyer Koçu & Mimar:* LiteLLM ve Gemini API kullanarak mülakat sorusu üreten/puanlayan ve "Tech Stack" (Proje Mimarisi) öneren `ai_coach.py` servisini kodlamak.

**Odaklanılması Gereken Klasörler ve Teknolojiler:**
*Klasörler:* `core/services/`, `infrastructure/serp_api/`, `infrastructure/gemini_client/`.
*Teknolojiler:* LiteLLM, Google Gemini API, Django-Q2 (veya Celery), SerpApi.

---

## 3. Frontend & Interaction Developer
**Rol Sahibi:** [Umut Can Kuş]
**Odak Noktası:** UI/UX, Veri Görselleştirme ve SPA Etkileşimleri.

**Ana Sorumluluklar:**
*UI İnşası:* Bootstrap 5 ve Django Templates kullanarak Dashboard, İlan Detay, Kanban Panosu ve AI Portföy Mimarı (`architect.html`) arayüzlerini hızlıca prototiplemek.
*Veri Görselleştirme:* Analiz servisinden gelen verileri kullanarak yetenek ağacını ve eksikleri Chart.js ile "Radar Grafiği" olarak ekrana çizdirmek.
*ATS Kanban Etkileşimi:* Başvuru takip sistemindeki sürükle-bırak (Drag & Drop) işlemlerini HTMX kullanarak sayfayı yenilemeden gerçekleştirmek.
*Mikro Etkileşimler:* Açılır pencereler ve SPA hissi veren tüm etkileşimler için Alpine.js kullanmak.

**Odaklanılması Gereken Klasörler ve Teknolojiler:**
*Klasörler:* `templates/` (`dashboard/`, `interviews/`, `partials/`), `static/`.
*Teknolojiler:* Django Templates, Bootstrap 5, Chart.js, HTMX, Alpine.js.