from django import forms
from .models import WeddingProfile, WeddingGroup, Post, Comment

class WeddingGroupForm(forms.ModelForm):
    class Meta:
        model = WeddingGroup
        fields = ['wedding_date']
        widgets = {
            'wedding_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'wedding_date': '결혼 예정일',
        }

class WeddingProfileForm(forms.ModelForm):
    class Meta:
        model = WeddingProfile
        fields = ['wedding_date'] # 다른 필드 제거
        widgets = {
            'wedding_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'style': 'padding: 1rem; border-radius: 12px;'
            }),
        }
        labels = {
            'wedding_date': '결혼 예정일',
        }

class GroupJoinForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '초대 코드 6자리 입력'}),
        label='초대 코드'
    )

    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        if not WeddingGroup.objects.filter(invite_code=code).exists():
            raise forms.ValidationError("유효하지 않은 초대 코드입니다.")
        return code

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-light border-0 py-3', 
                'style': 'border-radius: 15px;', 
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0 py-3', 
                'style': 'border-radius: 15px; height: 300px; resize: none;', 
                'placeholder': '내용을 자유롭게 입력하세요'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-light border-0 py-3', 
                'style': 'border-radius: 15px; resize: none; padding-right: 50px;', 
                'placeholder': '댓글을 남겨주세요...', 
                'rows': 2
            }),
        }
