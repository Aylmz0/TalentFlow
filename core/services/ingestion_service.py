import threading

import requests


class IngestionService:
    """
    SerpApi üzerinden iş ilanlarını çeken ve arka planda asenkron olarak 
    çalışabilen veri toplama (Ingestion) servis katmanı.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_jobs_async(self, query="software engineer"):
        """
        İş ilanlarını çekme işlemini ana iş parçacığını (main thread) bloklamadan 
        arka planda (background thread) başlatır.
        """
        thread = threading.Thread(
            target=self.fetch_jobs, 
            args=(query,), 
            name="SerpApiIngestionThread"
        )
        thread.daemon = True  # Uygulama kapandığında arka plan thread'i de düzgün sonlanır
        thread.start()

    def fetch_jobs(self, query):
        """
        SerpApi'ye istek atarak iş ilanlarını sorgular ve veriyi işler.
        Ağ hataları ve geçersiz API durumlarına karşı dayanıklıdır.
        """
        jobs = []
        if not self.api_key:
            print("SerpApi Hatası: API Anahtarı (SERPAPI_API_KEY) boş veya tanımlanmamış.")
            return jobs

        url = "https://serpapi.com/search"
        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": self.api_key
        }

        try:
            # timeout=10 ekleyerek ağ takılmalarında thread'in sonsuza kadar askıda kalmasını önlüyoruz
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    jobs = data.get("jobs_results", [])
                    print(f"SerpApi Başarılı: '{query}' araması için {len(jobs)} adet iş ilanı çekildi.")
                except ValueError:
                    print("SerpApi Hatası: Sunucudan geçersiz JSON yanıtı alındı.")
            elif response.status_code in {401, 403}:
                print(
                    f"SerpApi Yetkilendirme Hatası (HTTP {response.status_code}): "
                    "Lütfen API anahtarınızı kontrol edin."
                )
            else:
                print(f"SerpApi Sunucu Hatası: HTTP {response.status_code} - Yanıt: {response.text[:200]}")

        except requests.Timeout:
            print("SerpApi Hatası: İstek zaman aşımına uğradı (Timeout). Ağ bağlantısını kontrol edin.")
        except requests.RequestException as e:
            print(f"SerpApi Ağ Bağlantı Hatası: {e}")

        return jobs
