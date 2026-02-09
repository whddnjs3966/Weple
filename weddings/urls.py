from django.urls import path
from . import views

urlpatterns = [
    path('onboarding/', views.onboarding, name='onboarding'),
    path('dashboard/', views.dashboard_main, name='dashboard'),
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('checklist/', views.checklist_manage, name='checklist_manage'),
    path('vendors/', views.vendor_main, name='vendor_main'),
    path('community/', views.community_main, name='community_main'),
    path('community/write/', views.post_create, name='post_create'),
    path('community/<int:post_id>/', views.post_detail, name='post_detail'),
    path('community/comment/create/', views.comment_create, name='comment_create'),
    path('community/<int:post_id>/recommend/', views.post_recommend, name='post_recommend'),
    path('community/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('community/<int:post_id>/edit/', views.post_edit, name='post_edit'),
]
