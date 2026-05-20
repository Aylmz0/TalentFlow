import os
import litellm


class ResumeAIParser:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    # 🤖 AI ile skill çıkarma
    def extract_skills_with_ai(self, text):
        if not text:
            return []

        prompt = f"""
        Aşağıdaki CV metnini analiz et ve sadece teknik skill'leri liste olarak ver.

        CV:
        {text}

        Çıktı formatı:
        python, docker, kubernetes, sql
        """

        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key
            )

            result = response["choices"][0]["message"]["content"]

            # string → liste
            skills = [s.strip().lower() for s in result.split(",")]

            return skills

        except Exception as e:
            print("AI parsing hata:", e)
            return []