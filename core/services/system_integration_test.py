from core.services.resume_parser import ResumeParser
from core.services.ai_coach import AICoach
from apps.talent_models.models import UserSkills


class SystemIntegrationTest:

    def run_full_pipeline(self, pdf_path, user):
        print("🚀 Pipeline başlatıldı")

        # Parsing
        parser = ResumeParser(pdf_path=pdf_path)
        parsed_data = parser.parse()

        skills = parsed_data.get("skills", [])

        print("✔ Parsing:", skills)

        # DB kayıt
        for skill in skills:
            UserSkills.objects.create(
                user=user,
                skill_name=skill
            )

        print("✔ DB kayıt tamam")

        # AI
        coach = AICoach()

        interview = coach.generate_mock_interview(skills)
        tech_stack = coach.suggest_portfolio_stack(skills)

        print("✔ AI tamam")

        return {
            "skills": skills,
            "interview": interview,
            "tech_stack": tech_stack
        }