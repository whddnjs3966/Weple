import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vendors.models import VendorCategory, Vendor

def create_dummy_data():
    # Categories
    categories = {
        'venue': '예식장',
        'studio': '스튜디오',
        'dress': '드레스',
        'makeup': '메이크업',
    }
    
    cats_objs = {}
    for slug, name in categories.items():
        cat, created = VendorCategory.objects.get_or_create(slug=slug, defaults={'name': name})
        cats_objs[slug] = cat
        print(f"Category: {name}")

    # Vendors
    venues = [
        ("더채플앳청담", "서울 강남구", "채플 스타일의 경건한 예식", 4.5),
        ("빌라드지디 강남", "서울 강남구", "하우스 웨딩의 정석", 4.3),
        ("아펠가모 반포", "서울 서초구", "밥펠가모라 불리는 맛집", 4.7),
        ("라움 아트센터", "서울 강남구", "럭셔리 소셜 베뉴", 4.8),
    ]

    studios = [
        ("가을스튜디오", "서울 송파구", "롯데타워 배경 야간씬 맛집", 4.6),
        ("마이퍼스트레이디", "서울 강남구", "클래식하고 우아한 인물 중심", 4.4),
    ]

    dresses = [
        ("엔조최재훈", "서울 강남구", "화려한 비즈 맛집", 4.9),
        ("로즈로사", "서울 강남구", "러블리하고 소녀스러운 감성", 4.5),
    ]

    makeups = [
        ("정샘물 웨스트", "서울 강남구", "투명하고 깨끗한 피부 표현", 4.7),
        ("애브뉴준오", "서울 강남구", "음영 메이크업의 강자", 4.6),
    ]

    data = [
        ('venue', venues),
        ('studio', studios),
        ('dress', dresses),
        ('makeup', makeups),
    ]

    for cat_slug, vendor_list in data:
        cat = cats_objs[cat_slug]
        for name, region, summary, rating in vendor_list:
            v, created = Vendor.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat,
                    'region_sido': '서울특별시',
                    'region_sigungu': region.split()[1],
                    'avg_rating': rating,
                    'review_count': random.randint(10, 100),
                    'summary_positive': summary,
                    'summary_negative': '주말 예약이 어려움' if random.random() > 0.5 else '주차 공간 협소'
                }
            )
            if created:
                print(f"Created Vendor: {name}")
            else:
                print(f"Vendor already exists: {name}")

if __name__ == '__main__':
    create_dummy_data()
