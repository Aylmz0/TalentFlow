import os
import litellm


class AICoach:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    # 🎯 Mülakat sorusu üretimi
    def generate_interview_questions(self, skills):
        if not skills:
            return "Skill bilgisi bulunamadı."

        prompt = f"""
        Aşağıdaki teknolojilere göre 5 adet teknik mülakat sorusu üret:

        Teknolojiler: {', '.join(skills)}

        Sorular kısa ve anlaşılır olsun.
        """

        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key
            )

            return response['choices'][0]['message']['content']

        except Exception as e:
            print("AI Coach hata:", e)
            return "Mülakat soruları oluşturulamadı."

    # 🚀 Tech stack önerisi
    def suggest_tech_stack(self, skills):
        if not skills:
            return "Skill bilgisi bulunamadı."

        prompt = f"""
        Kullanıcının bildiği teknolojilere göre uygun bir proje tech stack öner:

        Teknolojiler: {', '.join(skills)}

        Backend, frontend ve devops araçlarını öner.
        """

        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key
            )

            return response['choices'][0]['message']['content']

        except Exception as e:
            print("AI Coach hata:", e)
            return "Tech stack önerisi oluşturulamadı."