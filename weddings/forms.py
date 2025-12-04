from django import forms
from .models import WeddingProfile

class WeddingProfileForm(forms.ModelForm):
    class Meta:
        model = WeddingProfile
        fields = ['wedding_date', 'region_sido', 'region_sigungu']
        widgets = {
            'wedding_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'region_sido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 서울특별시'}),
            'region_sigungu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 강남구'}),
            'style': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '예: 호텔웨딩'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '최소 예산 (만원)'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '최대 예산 (만원)'}),
        }
        labels = {
            'wedding_date': '결혼 예정일',
            'region_sido': '예식 지역 (시/도)',
            'region_sigungu': '예식 지역 (시/군/구)',
            'style': '예식 형태',
            'budget_min': '최소 예산',
            'budget_max': '최대 예산',
        }
