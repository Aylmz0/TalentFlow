from django.test import SimpleTestCase

from core.services.matchmaking_service import MatchmakingService


class TestMatchmakingService(SimpleTestCase):

    def test_score_calculation(self):
        """
        GOREV: Matchmaking - Yetenek eslesmesine gore puani dogru hesapliyor mu?
        """
        # Adayin buluna yetenekleri
        resume_data = {
            "skills": ["python", "docker"]
        }
        
        # Servisi baslat
        service = MatchmakingService(resume_data)
        
        # Sonucu al
        result = service.get_result()
        
        # Dogrulama: 2 yetenek eslesiyor (python ve docker). 
        # Bizim koddaki mantik: yetenek_sayisi * 30. Yani 2 * 30 = 60 olmali.
        self.assertEqual(result["score"], 60)
        self.assertIn("python", result["matched_skills"])
        self.assertIn("docker", result["matched_skills"])

    def test_zero_match_score(self):
        """
        GOREV: Matchmaking - Hic eslesme yoksa puan 0 mi?
        """
        resume_data = {
            "skills": ["ruby", "php"] # Bizim job_skills listesinde olmayan yetenekler
        }
        service = MatchmakingService(resume_data)
        result = service.get_result()
        
        self.assertEqual(result["score"], 0)
        self.assertEqual(len(result["matched_skills"]), 0)
