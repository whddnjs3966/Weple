from django.db import models
from vendors.models import Vendor

class RawReview(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reviews')
    source = models.CharField(max_length=20) # Naver, Google
    author_name = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    written_at = models.DateField(null=True, blank=True)
    crawled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.source} ({self.rating})"
