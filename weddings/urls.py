from django.urls import path
from . import views

urlpatterns = [
    path('onboarding/', views.onboarding, name='onboarding'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('community/write/', views.post_create, name='post_create'),
    path('community/<int:post_id>/', views.post_detail, name='post_detail'),
    path('community/comment/create/', views.comment_create, name='comment_create'),
]
