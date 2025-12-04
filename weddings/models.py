from django.db import models
from django.conf import settings

class WeddingProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wedding_profile')
    wedding_date = models.DateField()
    region_sido = models.CharField(max_length=50)
    region_sigungu = models.CharField(max_length=50, blank=True)
    style = models.CharField(max_length=50, blank=True)  # 예: '웨딩홀', '스몰웨딩'
    budget_min = models.IntegerField(null=True, blank=True)
    budget_max = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wedding ({self.wedding_date})"

class ScheduleTask(models.Model):
    profile = models.ForeignKey(WeddingProfile, on_delete=models.CASCADE, related_name='tasks')
    date = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    d_day_offset = models.IntegerField()  # D-100이면 -100
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.date}] {self.title}"

class DailyLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username}'s log for {self.date}"
