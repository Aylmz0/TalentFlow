class MockInterviewRepository:
    """
    Clean Architecture prensiplerine uygun olarak, MockInterview (Yapay Mülakat) 
    veritabanı sorgularını ve CRUD işlemlerini soyutlayan repository katmanı.
    
    Not: ST-3 aşamasında eklenecek olan MockInterview modeliyle tam uyumludur. 
    Lokal import yapısı sayesinde model henüz oluşturulmamış olsa bile projeyi çökertmez.
    """

    @staticmethod
    def get_by_id(pk):
        """
        Bir mülakat kaydını ID (Primary Key) üzerinden getirir. Bulamazsa None döner.
        """
        try:
            from apps.talent_models.models import MockInterview
            return MockInterview.objects.get(pk=pk)
        except (ImportError, AttributeError):
            print("Hata: MockInterview modeli talent_models.models altında bulunamadı (ST-3 bekleniyor).")
            return None
        except Exception:
            return None

    @staticmethod
    def get_all_by_user(user_id):
        """
        Belirli bir kullanıcının tüm yapay mülakat geçmişini listeler.
        """
        try:
            from apps.talent_models.models import MockInterview
            return MockInterview.objects.filter(user_id=user_id).order_by('-created_at')
        except (ImportError, AttributeError):
            print("Hata: MockInterview modeli talent_models.models altında bulunamadı (ST-3 bekleniyor).")
            return []

    @staticmethod
    def create(user, job, questions, user_answers=None, score=0):
        """
        Yeni bir yapay mülakat kaydı oluşturur ve veritabanına kaydeder.
        """
        try:
            from apps.talent_models.models import MockInterview
            mock_interview = MockInterview(
                user=user,
                job=job,
                questions=questions,
                user_answers=user_answers or {},
                score=score
            )
            mock_interview.save()
            return mock_interview
        except (ImportError, AttributeError) as e:
            print(f"Hata: MockInterview kaydı oluşturulamadı. Model eksik: {e}")
            return None

    @staticmethod
    def save(mock_interview):
        """
        Gönderilen MockInterview nesnesini veritabanına kaydeder/günceller.
        """
        mock_interview.save()
        return mock_interview
