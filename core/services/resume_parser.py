import re
from PyPDF2 import PdfReader  # PDF okuma için


class ResumeParser:

    def __init__(self, text=None, pdf_path=None):
        if pdf_path:
            extracted_text = self.extract_text_from_pdf(pdf_path)
            self.text = extracted_text.lower() if extracted_text else ""
        else:
            self.text = text.lower() if text else ""

    # 🔥 PDF → TEXT
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

    # 🔍 Skill extraction
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

    # ⏳ Experience extraction
    def extract_experience_years(self):
        match = re.search(r"(\d+)\s+years", self.text)
        if match:
            return int(match.group(1))
        return 0

    # 🚀 Main parse
    def parse(self):
        return {
            "skills": self.extract_skills(),
            "experience_years": self.extract_experience_years()
        }
        # TAL-24: küçük düzenleme yapıldı