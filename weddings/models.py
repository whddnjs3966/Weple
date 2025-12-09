from django.db import models
from django.conf import settings
import random
import string

def generate_invite_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not WeddingGroup.objects.filter(invite_code=code).exists():
            return code

class WeddingGroup(models.Model):
    wedding_date = models.DateField(null=True, blank=True)
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group {self.invite_code} ({self.wedding_date})"

class WeddingProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wedding_profile')
    group = models.ForeignKey(WeddingGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')
    
    # Added wedding_date as requested for simplified onboarding
    wedding_date = models.DateField(null=True, blank=True)
    
    region_sido = models.CharField(max_length=50, blank=True, null=True)
    region_sigungu = models.CharField(max_length=50, blank=True, null=True)
    style = models.CharField(max_length=50, blank=True, null=True)
    budget_min = models.IntegerField(null=True, blank=True)
    budget_max = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

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

    # Changed profile -> group
    group = models.ForeignKey(WeddingGroup, on_delete=models.CASCADE, related_name='tasks', null=True)
    
    date = models.DateField(null=True, blank=True) # 실제 수행일
    expected_date = models.DateField(null=True, blank=True) # 예정일
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1)
    d_day_offset = models.IntegerField(null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

class DailyLog(models.Model):
    # Changed user -> group
    group = models.ForeignKey(WeddingGroup, on_delete=models.CASCADE, related_name='daily_logs', null=True)
    
    date = models.DateField()
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Changed unique_together to (group, date)
        unique_together = ('group', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Log for {self.date}"

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
