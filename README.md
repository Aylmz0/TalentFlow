<p align="center">
  <h1 align="center">TalentFlow</h1>
  <p align="center">
    AI Destekli Bütünleşik Kariyer Yönetim Platformu
    <br />
    <a href="https://talentflow.yilmazcs.xyz"><strong>Canlı Demo »</strong></a>
    <br />
    <br />
    <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python">
    <img src="https://img.shields.io/badge/django-4.2-green" alt="Django">
    <img src="https://img.shields.io/badge/license-MIT-yellow" alt="License">
  </p>
</p>

## Hakkında

TalentFlow, yazılım geliştiriciler için kariyerlerini yönetmelerini sağlayan açık kaynak bir platformdur. CV'nizi yükleyin, yapay zeka yeteneklerinizi analiz etsin, kariyer yollarını keşfedin, iş başvurularınızı Kanban panosunda takip edin ve AI ile mülakat pratiği yapın.

### Özellikler

- **CV'den AI Yetenek Analizi** — PDF CV'nizi yükleyin, AI teknik yeteneklerinizi çıkarsın. Radar, çubuk ve kategori grafikleriyle görselleştirin.
- **Kariyer Yolu Eşleştirme** — 8 farklı role (Senior Python Developer, DevOps Engineer, Full Stack Developer, Data Scientist, Cloud Architect, SRE, Frontend Developer, Backend Developer) uyum oranınızı hesaplayın, eksik yeteneklerinizi görün.
- **Kanban İş Takibi** — Başvuru sürecinizi 4 sütunda yönetin: Başvuruldu, Mülakat, Teklif, Reddedildi. Sürükle-bırak desteği ile statü güncelleme.
- **AI Mülakat Simülasyonu** — İş ilanı bazında AI tarafından üretilmiş 5 teknik soru ile mülakat yapın. Cevaplarınız puanlansın, geri bildirim alın.
- **CV İyileştirme** — AI mevcut CV'nizi analiz eder: güçlü yanlarınızı çıkarır, madde madde iyileştirme önerileri sunar ve yeniden yazılmış bir CV oluşturur.
- **Portföy Mimarı** — Proje fikrinizi yazın, AI size teknoloji stack'i (backed, frontend, database, DevOps) ve FOSS alternatifleriyle birlikte roadmap çıkarsın.
- **Canlı İş İlanları** — SerpAPI entegrasyonu ile güncel iş ilanlarını çekin. API anahtarı yoksa 10 premium statik ilan ile çalışmaya devam edin.

## Başlarken

### Gereksinimler

- Python 3.10+
- PostgreSQL 14+ (production) veya SQLite (development)
- OpenRouter API anahtarı (AI özellikleri için)

### Kurulum

```bash
# 1. Projeyi klonla
git clone https://github.com/yilmaz/talentflow.git
cd talentflow

# 2. Sanal ortam oluştur ve aktifleştir
python -m venv .venv
source .venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Çevre değişkenlerini ayarla
cp .env.example .env   # veya manuel oluştur (aşağıdaki tabloya bak)

# 5. Veritabanını oluştur ve migrate et
python manage.py migrate

# 6. İş ilanlarını yükle (opsiyonel)
python manage.py seed_jobs

# 7. Geliştirme sunucusunu başlat
python manage.py runserver
```

### Çevre Değişkenleri

| Değişken | Zorunlu | Açıklama |
|---|---|---|
| `DEBUG` | Hayır | Django debug modu (varsayılan: `True`) |
| `SECRET_KEY` | Evet | Django gizli anahtarı |
| `DATABASE_URL` | Hayır | Varsayılan: `sqlite:///db.sqlite3`, production'da PostgreSQL |
| `OPENROUTER_API_KEY` | Evet | OpenRouter üzerinden AI API çağrıları için |
| `SERPAPI_API_KEY` | Hayır | Varsa canlı Google Jobs ilanları çekilir, yoksa statik ilanlar kullanılır |

### Test ve Kalite

```bash
# Unit test
python manage.py test

# Linting
ruff check .
```

## Proje Mimarisi

```
TalentFlow/
├── apps/                    # Web katmanı (views & urls)
│   ├── accounts/            # Giriş, kayıt, CV yükleme
│   ├── jobs/                # İş ilanı modeli + seed_jobs komutu
│   └── talent_models/       # Yetenek, başvuru, mülakat, proje modelleri
├── core/
│   └── services/            # İş mantığı (framework bağımsız)
│       ├── ai_coach.py      # AI etkileşimleri (LiteLLM/OpenRouter)
│       ├── resume_parser.py # PDF → metin → yetenek çıkarma
│       ├── matchmaking_service.py
│       └── ingestion_service.py  # SerpAPI iş ilanı çekme
├── config/                  # Django settings, URL yapılandırması
├── templates/               # HTML şablonları (dashboard, interviews, partials)
├── static/                  # CSS, JS (Alpine.js, HTMX, Chart.js, Sortable.js)
└── media/                   # Kullanıcı yüklemeleri (CV PDF'leri)
```

## Tech Stack

| Alan | Teknoloji |
|---|---|
| Programlama Dili | Python, JavaScript |
| Backend Framework | Django 4.2 |
| ORM | Django ORM |
| Veritabanı | PostgreSQL (prod), SQLite (dev) |
| Frontend | Django Templates + Bootstrap 5 |
| İstemci Kütüphaneleri | Alpine.js, HTMX, Chart.js, Sortable.js |
| PDF İşleme | PyPDF2 |
| Yapay Zeka | LiteLLM → OpenRouter (Gemini) |
| Kod Kalitesi | Ruff (flake8-django) |
| Test | unittest, pytest |
| CI/CD | GitHub Actions (lint → test → rsync deploy) |
| Deployment | Ubuntu VPS, Caddy (reverse proxy + SSL), tmux |
| Harici API | SerpAPI (opsiyonel, canlı iş ilanları) |

## Lisans

MIT
