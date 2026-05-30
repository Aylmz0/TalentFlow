from apps.talent_models.models import MockInterview

class MockInterviewRepository:
    """
    Clean Architecture prensiplerine uygun olarak, MockInterview (Yapay Mülakat) 
    veritabanı sorgularını ve CRUD işlemlerini soyutlayan repository katmanı.
    """

    @staticmethod
    def get_by_id(pk):
        """
        Bir mülakat kaydını ID (Primary Key) üzerinden getirir. Bulamazsa None döner.
        """
        try:
            return MockInterview.objects.get(pk=pk)
        except MockInterview.DoesNotExist:
            return None

    @staticmethod
    def get_all_by_user(user_id):
        """
        Belirli bir kullanıcının tüm yapay mülakat geçmişini listeler.
        """
        return MockInterview.objects.filter(user_id=user_id).order_by('-created_at')

    @staticmethod
    def create(user, job, questions, user_answers=None, score=0):
        """
        Yeni bir yapay mülakat kaydı oluşturur ve veritabanına kaydeder.
        """
        mock_interview = MockInterview(
            user=user,
            job=job,
            questions=questions,
            user_answers=user_answers or {},
            score=score
        )
        mock_interview.save()
        return mock_interview

    @staticmethod
    def save(mock_interview):
        """
        Gönderilen MockInterview nesnesini veritabanına kaydeder/günceller.
        """
        mock_interview.save()
        return mock_interview
