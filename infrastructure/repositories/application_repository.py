from apps.talent_models.models import Application

class ApplicationRepository:
    """
    Clean Architecture prensiplerine uygun olarak, Application (Başvuru) 
    veritabanı sorgularını ve CRUD işlemlerini soyutlayan repository katmanı.
    """

    @staticmethod
    def get_by_id(pk):
        """
        Bir başvuruyu ID (Primary Key) üzerinden getirir. Bulamazsa None döner.
        """
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return None

    @staticmethod
    def get_by_user_and_job(user_id, job_id):
        """
        Bir kullanıcının belirli bir ilana yaptığı başvuruyu getirir.
        """
        try:
            return Application.objects.get(user_id=user_id, job_id=job_id)
        except Application.DoesNotExist:
            return None

    @staticmethod
    def get_all_by_user(user_id):
        """
        Belirli bir kullanıcının yaptığı tüm başvuruları listeler.
        """
        return Application.objects.filter(user_id=user_id).order_by('-created_at')

    @staticmethod
    def create(user, job, status='APPLIED', notes=""):
        """
        Yeni bir iş başvurusu kaydı oluşturur ve kaydeder.
        """
        application = Application(
            user=user,
            job=job,
            status=status,
            notes=notes
        )
        application.save()
        return application

    @staticmethod
    def update_status(application_id, new_status):
        """
        Var olan bir başvurunun durumunu günceller.
        """
        application = ApplicationRepository.get_by_id(application_id)
        if application:
            application.status = new_status
            application.save()
            return application
        return None

    @staticmethod
    def save(application):
        """
        Gönderilen Application nesnesini veritabanına kaydeder/günceller.
        """
        application.save()
        return application
