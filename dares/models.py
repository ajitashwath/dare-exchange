from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator

class Dare(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    college = models.CharField(max_length=200)
    dare_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Dare by {self.name} from {self.college}"

    def get_absolute_url(self):
        return reverse('dare_detail', args=[str(self.id)])