import os
import django
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vendors.models import VendorCategory

def add_categories():
    new_categories = {
        'meeting': '상견례장소',
        'hanbok': '한복',
    }
    
    for slug, name in new_categories.items():
        cat, created = VendorCategory.objects.get_or_create(slug=slug, defaults={'name': name})
        if created:
            print(f"Created Category: {name} ({slug})")
        else:
            print(f"Category already exists: {name} ({slug})")

if __name__ == '__main__':
    add_categories()
