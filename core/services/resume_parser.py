import os
import re
import litellm
from PyPDF2 import PdfReader


# 🤖 AI Parser
class ResumeAIParser:

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

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

            skills = [s.strip().lower() for s in result.split(",")]

            return skills

        except Exception as e:
            print("AI parsing hata:", e)
            return []


# 📄 Normal Parser
class ResumeParser:

    def __init__(self, text=None, pdf_path=None):
        if pdf_path:
            extracted_text = self.extract_text_from_pdf(pdf_path)
            self.text = extracted_text.lower() if extracted_text else ""
        else:
            self.text = text.lower() if text else ""

    # PDF → TEXT
    def extract_text_from_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "

            return text

        except Exception as e:
            print("PDF okuma hatası:", e)
            return ""

    # Basic Skill extraction
    def extract_skills(self):
        skills_db = [
            "python", "java", "c", "c++", "c#", "javascript",
            "docker", "kubernetes", "sql", "django", "flask"
        ]

        found_skills = []

        for skill in skills_db:
            if skill in self.text:
                found_skills.append(skill)

        return found_skills

    # Experience extraction
    def extract_experience_years(self):
        match = re.search(r"(\d+)\s+years", self.text)
        if match:
            return int(match.group(1))
        return 0

    # 🚀 FINAL PARSE (AI + NORMAL)
    def parse(self):
        ai_parser = ResumeAIParser()

        ai_skills = ai_parser.extract_skills_with_ai(self.text)

        # fallback (AI boş dönerse)
        if not ai_skills:
            ai_skills = self.extract_skills()

        return {
            "skills": ai_skills,
            "experience_years": self.extract_experience_years()
        }
