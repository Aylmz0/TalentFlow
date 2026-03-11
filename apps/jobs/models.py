from django.db import models

class Job(models.Model):
    SOURCE_CHOICES = [
        ('KAGGLE', 'Kaggle Dataset'),
        ('LIVE_SERPAPI', 'Live SerpApi'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='KAGGLE')
    posted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"
