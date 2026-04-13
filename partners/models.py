from django.db import models

class Partner(models.Model):
    image = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
