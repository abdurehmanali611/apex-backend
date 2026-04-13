from django.db import models

class Team(models.Model):
    image = models.URLField()
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    facebook = models.URLField()
    instagram = models.URLField()
    linkedin = models.URLField()
    telegram = models.URLField()

    def __str__(self):
        return self.name
