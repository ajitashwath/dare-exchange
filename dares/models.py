from django.db import models
from django.urls import reverse

class Dare(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    college = models.CharField(max_length=200)
    dare_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dare by {self.name} from {self.college}"

    def get_absolute_url(self):
        return reverse('dare_detail', args=[str(self.id)])