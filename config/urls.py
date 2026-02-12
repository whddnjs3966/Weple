from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', core_views.CustomLoginView.as_view(), name='login'),
    # path('accounts/', include('django.contrib.auth.urls')), # Removed to avoid conflict with allauth
    path('signup/', core_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('weddings/', include('weddings.urls')),
    path('vendors/', include('vendors.urls')),
    path('', core_views.landing, name='landing'),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
