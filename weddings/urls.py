from django.urls import path
from . import views

urlpatterns = [
    path('onboarding/', views.onboarding, name='onboarding'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
