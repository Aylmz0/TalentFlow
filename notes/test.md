# TalentFlow - Unit Test Dokumantasyonu

Bu dokuman, projedeki test sureclerini, testlerin neyi kontrol ettigini ve nasil calistirilacagini aciklar.

## 1. Unit Test Nedir ve Neden Kullanilir?
Unit Test (Birim Testi), yazdigimiz kodun en kucuk parcalarinin (fonksiyonlar, siniflar) beklenen sonucu verip vermedigini otomatik olarak denetler. 

**Avantajlari:**
- Kodda hata yapildiginda aninda yakalanmasini saglar.
- Refactor (kodu iyilestirme) yaparken mevcut sistemin bozulmadigini garanti eder.
- Akademik notlandirmada projenin muhendislik kalitesini kanitlar.

## 2. Test Edilen Gorevler (Taskler)

### Task 1: Resume Parsing (Özgeçmiş Ayrıştırma)
- **Dosya:** `core/services/resume_parser.py`
- **Test:** `core/tests/test_resume_parser.py`
- **Amac:** Yuklenen PDF'den cikan metnin icinden yeteneklerin (Python, Django vb.) dogru ayiklanip ayiklanmadigini ve deneyim yilinin dogru tespit edilip edilmedigini denetler.

### Task 2: Matchmaking (Yetenek Eşleştirme & Skorlama)
- **Dosya:** `core/services/matchmaking_service.py`
- **Test:** `core/tests/test_matchmaking.py`
- **Amac:** Adayin yetenekleri ile is ilani yetenekleri karsilastirildiginda, puanin (yetenek_sayisi * 30) matematiksel olarak dogru hesaplanmasini garanti eder.

## 3. Testler Nasil Calistirilir?

Proje kok dizinindeyken su komutu terminalde calistirin:

```bash
# Sanal ortam aktifken
python manage.py test core.tests
```

**Cikti Anlami:**
- `....` : Her bir nokta, basariyla gecen bir testi temsil eder.
- `OK` : Tum testlerin hatasiz gectigini gosterir.
- `FAILED` : Kodda bir hata oldugunu ve testlerin takildigini gosterir.

## 4. Hoca Sunumu Icin "Hata Yakalama" Demosu (Showcase)

Hocaya testlerin gercekten calistigini kanitlamak icin su adimlari izleyebilirsiniz:

1. `core/services/matchmaking_service.py` dosyasini acin.
2. `score = len(matched) * 30` satirini bulup, bilerek `* 20` yapin.
3. Testi calistirin (`python manage.py test core.tests`).
4. Testin **FAIL** verdigini ve nerede hata oldugunu (Beklenen 60, Gelen 40 gibi) hocaya gosterin.
5. Kodu geri duzeltip tekrar calistirin ve **OK** sonucunu gosterin.

---
**Lead Architect Notu:** Yeni bir servis eklendiginde, lutfen `core/tests/` altina ilgili test dosyasini eklemeyi unutmayin.
