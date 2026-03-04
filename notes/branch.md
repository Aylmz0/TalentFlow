
---

# 🚩 TalentFlow Ekip Çalışma Kuralları

Bu projede düzeni sağlamak ve hocanın "izlenebilirlik" kuralına uymak adına her ekip üyesi aşağıdaki adımları sırasıyla takip etmek zorundadır.

### 1. İş Kabulü (Jira)

* Panodaki **TO DO** sütunundan bir görev seç ve üzerine al. 


* Kartı **IN PROGRESS** sütununa sürükle.
* Kartın içindeki **"Create Branch"** butonuna basarak dalını oluştur. 


* **Önemli:** Dal isimlendirmesi mutlaka Jira koduyla başlamalıdır.
* **Format:** `TAL-[GörevNo]-[İsminiz]-[Özet]`
* **Örnek:** `TAL-2-yil-modeller` veya `TAL-3-alp-servis-yazimi`



### 2. Yerel Çalışma (Terminal)

* Bilgisayarında her zaman en güncel `main` dalında olduğundan emin ol:
```bash
git checkout main
git pull origin main

```


* Jira'da oluşturduğun yeni dala geçiş yap:
```bash
git fetch
git checkout DAL_ADINIZ

```



### 3. Kodun Gönderilmesi (GitHub)

* İşin bittiğinde değişikliklerini commit et ve kendi dalına pushla:
```bash
git add .
git commit -m "TAL-X: Yapılan işin özeti"
git push origin DAL_ADINIZ

```



### 4. Pull Request ve Review (ONAY SÜRECİ)

* GitHub'a git ve dalın için bir **Pull Request (PR)** aç.
* Sağ taraftaki **Reviewers** kısmından mutlaka takım liderini (Abdullah) veya bir arkadaşını seç.
* 
**ASLA KENDİ KODUNU ONAY ALMADAN MERGE ETME!** 


* İnceleyen kişi yorum yaparsa düzeltmeleri yap. Onay (Approve) gelmeden kod ana dala birleşmeyecektir.

### 5. Kapatma

* Onay alındıktan sonra kodu `main` dalına birleştir (Merge).
* Jira'daki kartı **DONE** sütununa at. 



---

Bu dosyayı oluşturduktan sonra şu komutlarla GitHub'a gönderip herkese ilan edebilirsin:

```bash
git add GELISTIRICI_REHBERI.md
git commit -m "TAL-1: Git ve Jira kullanım rehberi yayınlandı"
git push origin main

```

Rehber işi bittiğine göre, artık **TAL-2** kartını açıp o meşhur **Hibrit Veritabanı Modellerine** (User, Job, Skill) odaklanalım mı?