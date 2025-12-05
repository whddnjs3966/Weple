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
    CATEGORY_CHOICES = [
        ('MEETING', '상견례'),
        ('VENUE', '예식장'),
        ('SDM', '스드메'),
        ('ATTIRE', '예복/한복'),
        ('INVITATION', '청첩장'),
        ('HONEYMOON', '신혼여행'),
        ('FURNISHING', '혼수'),
        ('CONTRACT', '계약/결제'),
        ('OTHER', '기타'),
    ]
    
    DIFFICULTY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    profile = models.ForeignKey(WeddingProfile, on_delete=models.CASCADE, related_name='tasks')
    date = models.DateField(null=True, blank=True) # 실제 수행일 (완료일)
    expected_date = models.DateField(null=True, blank=True) # 예정일
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    d_day_offset = models.IntegerField(null=True, blank=True)  # D-100이면 -100
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

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

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notices')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    is_answered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
