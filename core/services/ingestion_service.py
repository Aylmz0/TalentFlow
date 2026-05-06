import requests
import threading

class IngestionService:

    def __init__(self, api_key):
        self.api_key = api_key


    # 🔥 Arka plan iş
    def fetch_jobs_async(self, query="software engineer"):
        thread = threading.Thread(target=self.fetch_jobs, args=(query,))
        thread.start()


    # 🌐 SerpApi çağrısı
    def fetch_jobs(self, query):
        url = "https://serpapi.com/search"

        params = {
            "engine": "google_jobs",
            "q": query,
            "api_key": self.api_key
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            print("Jobs fetched:", len(data.get("jobs_results", [])))
        else:
            print("SerpApi error")