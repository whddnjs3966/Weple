from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    path('<int:vendor_id>/select/', views.add_selection, name='add_selection'),
]
