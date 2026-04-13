from django.db import models

class Blog(models.Model):
    image = models.URLField()
    link = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    source = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.title
