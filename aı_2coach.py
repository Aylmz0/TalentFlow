import os
import litellm


class AICoach:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    # 🎯 Mock Interview (Mülakat Soruları)
    def generate_mock_interview(self, skills):
        if not skills:
            return "Skill bilgisi bulunamadı."

        prompt = f"""
        Aşağıdaki teknolojilere sahip bir aday için 5 adet teknik mülakat sorusu oluştur.

        Teknolojiler: {', '.join(skills)}

        Sorular kısa, anlaşılır ve teknik seviyede olsun.
        """

        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            print("Mock Interview hata:", e)
            return "Mülakat soruları üretilemedi."

    # 🚀 Tech Stack Önerisi (Portfolyo Mimari)
    def suggest_portfolio_stack(self, skills):
        if not skills:
            return "Skill bilgisi bulunamadı."

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

        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            print("Tech Stack hata:", e)
            return "Tech stack önerisi üretilemedi."