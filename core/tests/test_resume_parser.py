from django.test import SimpleTestCase

from core.services.resume_parser import ResumeParser


class TestResumeParser(SimpleTestCase):

    def test_extract_skills_success(self):
        """
        GOREV: Resume Parser - Metin icinden yetenekleri dogru ayikliyor mu?
        """
        # Test verisi
        test_text = "I am a developer experienced in Python, Django and SQL."
        parser = ResumeParser(text=test_text)
        
        # Beklenen yetenekler
        expected_skills = ["python", "django", "sql"]
        
        # Fonksiyonu calistir
        result = parser.extract_skills()
        
        # Dogrula
        for skill in expected_skills:
            self.assertIn(skill, result)

    def test_extract_experience_years(self):
        """
        GOREV: Resume Parser - Deneyim yilini dogru tespit ediyor mu?
        """
        test_text = "I have 5 years of experience in backend development."
        parser = ResumeParser(text=test_text)
        
        self.assertEqual(parser.extract_experience_years(), 5)
