import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vendors.models import Vendor, VendorCategory

def create_data():
    # Categories
    categories = ['웨딩홀', '스튜디오', '드레스', '메이크업']
    cat_objs = {}
    for name in categories:
        slug = {'웨딩홀': 'hall', '스튜디오': 'studio', '드레스': 'dress', '메이크업': 'makeup'}[name]
        cat, created = VendorCategory.objects.get_or_create(name=name, defaults={'slug': slug})
        cat_objs[name] = cat
        print(f"Category: {name}")

    # Vendors
    vendors_data = [
        {
            'name': '아모리스 역삼',
            'category': '웨딩홀',
            'region_sido': '서울',
            'region_sigungu': '강남구',
            'avg_rating': 4.5,
            'review_count': 120
        },
        {
            'name': '더채플앳청담',
            'category': '웨딩홀',
            'region_sido': '서울',
            'region_sigungu': '강남구',
            'avg_rating': 4.8,
            'review_count': 200
        },
        {
            'name': '가을스튜디오',
            'category': '스튜디오',
            'region_sido': '서울',
            'region_sigungu': '송파구',
            'avg_rating': 4.2,
            'review_count': 50
        },
    ]

    for v_data in vendors_data:
        cat = cat_objs[v_data.pop('category')]
        Vendor.objects.get_or_create(name=v_data['name'], defaults={**v_data, 'category': cat})
        print(f"Vendor: {v_data['name']}")

if __name__ == '__main__':
    create_data()
