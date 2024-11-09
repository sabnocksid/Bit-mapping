from django.db import models

class DrawingAttempt(models.Model):
    target_letter = models.CharField(max_length=1)
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
