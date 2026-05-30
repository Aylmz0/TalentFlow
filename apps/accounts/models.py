from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    target_role = models.CharField(max_length=255, blank=True)
    cv_file = models.FileField(upload_to='cv_files/', blank=True, null=True)

    def __str__(self):
        return self.username
