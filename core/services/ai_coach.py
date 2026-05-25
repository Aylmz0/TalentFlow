import os
from django.conf import settings

class AICoach:
    """
    Kullanıcıların özgeçmişlerinden elde edilen yeteneklere (skills) göre:
    - Teknik mülakat soruları (Mock Interview) üreten,
    - Kariyer ve portfolyo için teknoloji yığını (Tech Stack) öneren
    yapay zeka servis katmanı.
    """

    def __init__(self):
        # API anahtarını öncelikle Django settings'den, bulamazsa çevre değişkenlerinden alır
        self.api_key = getattr(settings, "OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

    def _get_api_key(self):
        # LiteLLM'in kullanacağı API anahtarını döndürür ve yapılandırır
        import litellm
        litellm.api_key = self.api_key
        return self.api_key

    def generate_interview_questions(self, skills):
        """
        Adayın bildiği teknolojilere göre 5 adet teknik mülakat sorusu üretir.
        """
        if not skills:
            return "Yetenek (Skill) bilgisi bulunamadığı için mülakat soruları üretilemedi."

        prompt = f"""
        Aşağıdaki teknolojilere göre 5 adet teknik mülakat sorusu üret:

        Teknolojiler: {', '.join(skills)}

        Sorular kısa ve anlaşılır olsun.
        """
        return self._execute_completion(prompt, "Mülakat soruları oluşturulamadı.")

    def suggest_tech_stack(self, skills):
        """
        Adayın bildiği teknolojilere göre uygun bir proje tech stack (Backend, Frontend, DevOps vb.) önerir.
        """
        if not skills:
            return "Yetenek (Skill) bilgisi bulunamadığı için teknoloji önerisi üretilemedi."

        prompt = f"""
        Kullanıcının bildiği teknolojilere göre uygun bir proje tech stack öner:

        Teknolojiler: {', '.join(skills)}

        Backend, frontend ve devops araçlarını öner.
        """
        return self._execute_completion(prompt, "Tech stack önerisi oluşturulamadı.")

    def generate_mock_interview(self, skills):
        """
        (Geriye Uyumlu / Mock Interview)
        Aday için 5 adet kısa, anlaşılır ve teknik seviyede mülakat sorusu oluşturur.
        """
        if not skills:
            return "Yetenek (Skill) bilgisi bulunamadı."

        prompt = f"""
        Aşağıdaki teknolojilere sahip bir aday için 5 adet teknik mülakat sorusu oluştur.

        Teknolojiler: {', '.join(skills)}

        Sorular kısa, anlaşılır ve teknik seviyede olsun.
        """
        return self._execute_completion(prompt, "Mülakat soruları üretilemedi.")

    def suggest_portfolio_stack(self, skills):
        """
        (Geriye Uyumlu / Portfolyo Stack)
        Kullanıcının modern bir proje geliştirmesi için portfolyo tech stack önerir.
        """
        if not skills:
            return "Yetenek (Skill) bilgisi bulunamadı."

        prompt = f"""
        Kullanıcının bildiği teknolojilere göre bir proje geliştirmesi için modern bir tech stack öner.

        Teknolojiler: {', '.join(skills)}

        Şunları içersin:
        - Backend
        - Frontend
        - Veritabanı
        - DevOps araçları

        Kısa ve net yaz.
        """
        return self._execute_completion(prompt, "Tech stack önerisi üretilemedi.")

    def _execute_completion(self, prompt, error_message):
        """
        LiteLLM completion çağrısını güvenli bir şekilde yürüten yardımcı metot.
        """
        try:
            import litellm
            self._get_api_key()
            
            # API anahtarı boşsa doğrudan bilgilendirme dönelim (crash yerine gracefully handle)
            if not litellm.api_key:
                return "Hata: OpenAI API anahtarı (OPENAI_API_KEY) tanımlanmamış. Lütfen .env dosyanızı kontrol edin."

            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response['choices'][0]['message']['content']

        except Exception as e:
            # Hata durumunu loglayıp kullanıcıya crash yaşatmadan mesaj dönüyoruz
            print(f"AI Coach Hata Raporu: {e}")
            return error_message
