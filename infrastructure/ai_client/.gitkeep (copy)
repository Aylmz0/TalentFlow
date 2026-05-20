import os
import litellm


class AIClient:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        litellm.api_key = self.api_key

    def generate(self, prompt):
        try:
            response = litellm.completion(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            return response["choices"][0]["message"]["content"]

        except Exception as e:
            print("AI Client hata:", e)
            return "AI yanıt üretilemedi."