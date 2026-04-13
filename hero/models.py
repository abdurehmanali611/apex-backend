from django.db import models

class HeroStat(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
