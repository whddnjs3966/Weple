from django.db import models
from weddings.models import WeddingProfile

class VendorCategory(models.Model):
    name = models.CharField(max_length=50)  # 예: 예식장, 스튜디오 등
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vendor Categories"

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(VendorCategory, on_delete=models.CASCADE, related_name='vendors')
    region_sido = models.CharField(max_length=50)
    region_sigungu = models.CharField(max_length=50)
    address = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='vendors/', blank=True, null=True)
    naver_place_id = models.CharField(max_length=100, blank=True)
    google_place_id = models.CharField(max_length=100, blank=True)
    avg_rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    summary_positive = models.TextField(blank=True)
    summary_negative = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserVendorSelection(models.Model):
    STATUS_CHOICES = [
        ('candidate', '후보'),
        ('final', '최종 선택'),
    ]
    profile = models.ForeignKey(WeddingProfile, on_delete=models.CASCADE, related_name='vendor_selections')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='candidate')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'vendor')

    def __str__(self):
        return f"{self.profile.user.username} - {self.vendor.name} ({self.get_status_display()})"
