from django.db import models

class Contact(models.Model):
    Full_Name = models.CharField(max_length=255)
    Email = models.EmailField()
    Subject = models.CharField(max_length=255)
    Message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Full_Name
