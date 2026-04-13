from django.db import models

class Portfolio(models.Model):
    image = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255)
    version = models.PositiveIntegerField(blank=True, null=True)
    duration = models.PositiveIntegerField()
    link = models.URLField(blank=True, null=True)
    special = models.BooleanField(default=False)

    def __str__(self):
        return self.title
