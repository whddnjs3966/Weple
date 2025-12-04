import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

try:
    u = User.objects.get(username='admin')
    u.set_password('admin')
    u.save()
    print("Password for 'admin' updated to 'admin'.")
except User.DoesNotExist:
    print("User 'admin' does not exist.")
