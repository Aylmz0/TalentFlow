import re

class ResumeParser:

    def __init__(self, text):
        self.text = text.lower()

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

    def extract_experience_years(self):
        match = re.search(r"(\d+)\s+years", self.text)
        if match:
            return int(match.group(1))
        return 0

    def parse(self):
        return {
            "skills": self.extract_skills(),
            "experience_years": self.extract_experience_years()
        }