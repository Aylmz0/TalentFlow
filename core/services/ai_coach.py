import os
import re
import litellm
from django.conf import settings


class AICoach:
    """
    Kullanıcıların özgeçmişlerinden elde edilen yeteneklere (skills) göre:
    - Teknik mülakat soruları (Mock Interview) üreten,
    - Kariyer ve portfolyo için teknoloji yığını (Tech Stack) öneren,
    - Akıllı mülakat cevaplarını puanlayan,
    - AI destekli Portföy Mimarisi çizen
    yapay zeka servis katmanı.
    """

    def __init__(self):
        # API anahtarını, modeli ve base_url'i Django settings veya env'den alır
        self.api_key = getattr(settings, "OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
        self.model = getattr(settings, "AI_MODEL", os.getenv("AI_MODEL", "google/gemini-flash-1.5"))
        self.base_url = getattr(settings, "AI_BASE_URL", "https://openrouter.ai/api/v1")

    def _get_api_key(self):
        litellm.api_key = self.api_key
        litellm.api_base = self.base_url
        return self.api_key

    def generate_interview_questions(self, skills):
        """
        Adayın bildiği teknolojilere göre 5 adet teknik mülakat sorusu üretir.
        """
        if not skills:
            return "Yetenek (Skill) bilgisi bulunamadığı için mülakat soruları üretilemedi."

        prompt = f"""
        Aşağıdaki teknolojilere göre bir teknik mülakat için tam olarak 5 adet soru üret:

        Teknolojiler: {', '.join(skills)}

        Lütfen çıktıyı düz bir metin olarak, her soru yeni bir satırda ve numarayla başlayacak şekilde ver (örn. "1. Python'da GIL nedir?").
        Sadece soruları döndür, başka hiçbir giriş, selamlama veya açıklama yazma.
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

        Backend, frontend, database ve devops araçlarını içeren kısa, net ve premium bir öneri şablonu oluştur.
        """
        return self._execute_completion(prompt, "Tech stack önerisi oluşturulamadı.")

    def generate_portfolio_architecture(self, idea: str) -> str:
        """
        Kullanıcının proje fikri için detaylı teknoloji yığını ve roadmap mimarisi üretir (JSON döner).
        """
        if not idea:
            return "Proje fikri boş olamaz."

        prompt = f"""
        Kullanıcının proje fikri: "{idea}"
        
        Bu proje için modern, ölçeklenebilir ve FOSS (Açık Kaynak Kodlu) alternatifleri de içeren bir teknoloji mimarisi oluştur.
        Çıktıyı kesinlikle aşağıdaki JSON şemasında ver, markdown kod blokları (```json ... ```) DAHİL OLMADAN, sadece ham JSON string döndür:
        {{
            "recommended_stack": {{
                "backend": {{"primary": "...", "foss_alternative": "..."}},
                "frontend": {{"primary": "...", "foss_alternative": "..."}},
                "database": {{"primary": "...", "foss_alternative": "..."}},
                "devops": {{"primary": "...", "foss_alternative": "..."}}
            }},
            "roadmap": [
                "1. Adım: ...",
                "2. Adım: ...",
                "3. Adım: ...",
                "4. Adım: ...",
                "5. Adım: ..."
            ]
        }}
        
        JSON şemasının geçerli ve parse edilebilir olmasına son derece dikkat et. JSON haricinde hiçbir açıklama veya ek metin ekleme.
        """
        return self._execute_completion(prompt, "Portföy mimarisi oluşturulamadı.")

    def score_interview_answers(self, questions: list, answers: list) -> str:
        """
        Kullanıcının teknik mülakat sorularına verdiği cevapları değerlendirip puanlar (JSON döner).
        """
        if not questions or not answers:
            return "Soru veya cevaplar eksik."

        q_and_a = []
        for i, (q, a) in enumerate(zip(questions, answers, strict=False)):
            q_and_a.append(f"Soru {i+1}: {q}\nCevap: {a}\n")

        prompt = f"""
        Teknik mülakat sorularına verilen cevapları değerlendir ve puanla.
        
        Sorular ve Cevaplar:
        {"".join(q_and_a)}
        
        Çıktıyı kesinlikle aşağıdaki JSON şemasında ver, markdown kod blokları (```json ... ```) DAHİL OLMADAN, sadece ham JSON string döndür:
        {{
            "overall_score": 75,
            "feedback": "Adayın genel performansı hakkında yapıcı geribildirim...",
            "per_question": [
                {{"score": 80, "comment": "..."}},
                {{"score": 70, "comment": "..."}}
            ]
        }}
        
        JSON şemasının geçerli ve parse edilebilir olmasına son derece dikkat et. JSON haricinde hiçbir açıklama veya ek metin ekleme.
        """
        return self._execute_completion(prompt, "Puanlama yapılamadı.")

    def _execute_completion(self, prompt, error_message):
        """
        LiteLLM completion çağrısını güvenli bir şekilde yürüten yardımcı metot.
        """
        try:
            self._get_api_key()
            
            if not self.api_key:
                return (
                    "Hata: OpenRouter API anahtarı (OPENROUTER_API_KEY) tanımlanmamış. "
                    "Lütfen .env dosyanızı kontrol edin."
                )

            # OpenRouter için LiteLLM çağrısı
            response = litellm.completion(
                model=f"openrouter/{self.model}",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # LiteLLM Pydantic nesnesi olarak döndüğü için nesne niteliği üzerinden okuyoruz
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
            # Sözlük fallback
            elif isinstance(response, dict) and 'choices' in response:
                content = response['choices'][0]['message']['content']
            else:
                return error_message

            # LLM bazen çıktıya markdown json kod blokları ekleyebilir (```json ... ```). Bunları temizleyelim.
            if content:
                content = re.sub(r"^```json\s*", "", content, flags=re.MULTILINE)
                content = re.sub(r"^```\s*", "", content, flags=re.MULTILINE)
                content = content.strip()

            return content

        except Exception as e:
            print(f"AI Coach Hata Raporu: {e}")
            return error_message
