from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Vendor, VendorCategory, UserVendorSelection

@login_required
def vendor_list(request):
    """
    업체 목록 조회 및 필터링 (네이버/구글 API 연동 추가)
    """
    category_slug = request.GET.get('category')
    region = request.GET.get('region')
    
    # 1. API 검색 및 데이터 저장 (지역 + 카테고리가 모두 있을 때만)
    if category_slug and region:
        category = get_object_or_404(VendorCategory, slug=category_slug)
        search_query = f"{region} {category.name}"
        
        # 유틸리티 함수 호출 (lazy import to avoid circular dependency if any)
        from .utils import search_naver_local, search_google_places
        
        # 네이버 검색
        naver_results = search_naver_local(search_query)
        for item in naver_results:
            # title에 HTML 태그가 포함될 수 있으므로 제거 (간단히)
            clean_title = item['title'].replace('<b>', '').replace('</b>', '')
            
            # 이미 존재하는지 확인 (naver_place_id가 없으면 이름/주소로 대략적 확인 가능하나, 여기선 mapx/mapy등 고유값 부재로 이름+카테고리 사용 권장. 
            # 하지만 간단히 이름으로 중복 체크하거나, 항상 생성하지 않도록 주의)
            # 네이버 API는 place_id를 명시적으로 주지 않는 경우가 있어, 링크나 이름으로 식별
            
            # 여기서는 편의상 Naver Search 결과는 display만 하거나, 
            # Google Place Search를 주력으로 사용하여 Place ID를 저장하는 것이 관리가 용이함.
            # 사용자 요청에 따라 'naver_place_id' 필드가 모델에 있으므로,
            # 네이버 결과는 link 등을 ID로 쓰거나, Google API 결과를 우선시 할 수 있음.
            # 이 코드에서는 Google Places API 결과를 우선적으로 DB에 저장하는 로직을 구현함.
            pass 

        # 구글 장소 검색 (Text Search)
        google_results = search_google_places(search_query)
        for result in google_results:
            place_id = result.get('place_id')
            name = result.get('name')
            address = result.get('formatted_address', '')
            rating = result.get('rating', 0.0)
            user_ratings_total = result.get('user_ratings_total', 0)
            
            # DB 존재 여부 확인 (Google Place ID 기준)
            vendor, created = Vendor.objects.get_or_create(
                google_place_id=place_id,
                defaults={
                    'name': name,
                    'category': category,
                    'region_sido': region.split(' ')[0] if region else '', # 간단한 파싱
                    'region_sigungu': region.split(' ')[1] if region and len(region.split(' ')) > 1 else '',
                    'address': address,
                    'avg_rating': rating,
                    'review_count': user_ratings_total,
                }
            )
            
            # 이미 존재하면 정보 업데이트 (옵션)
            if not created:
                if vendor.avg_rating != rating or vendor.review_count != user_ratings_total:
                    vendor.avg_rating = rating
                    vendor.review_count = user_ratings_total
                    vendor.save()

    # 2. DB 조회 및 필터링 (기존 로직 유지)
    vendors = Vendor.objects.all()
    
    if category_slug:
        vendors = vendors.filter(category__slug=category_slug)
    
    if region:
        vendors = vendors.filter(Q(region_sido__contains=region) | Q(region_sigungu__contains=region) | Q(address__contains=region))
        
    categories = VendorCategory.objects.all()
    
    context = {
        'vendors': vendors,
        'categories': categories,
        'current_category': category_slug,
        'current_region': region,
    }
    return render(request, 'vendors/vendor_list_v2.html', context)

@login_required
def vendor_detail(request, vendor_id):
    """
    업체 상세 정보 및 리뷰 요약
    """
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    
    # 사용자의 선택 상태 확인
    selection = None
    if hasattr(request.user, 'wedding_profile'):
        selection = UserVendorSelection.objects.filter(
            profile=request.user.wedding_profile,
            vendor=vendor
        ).first()
        
    context = {
        'vendor': vendor,
        'selection': selection,
    }
    return render(request, 'vendors/vendor_detail.html', context)

@login_required
def add_selection(request, vendor_id):
    """
    업체를 후보로 등록하거나 최종 선택
    """
    if request.method == 'POST':
        vendor = get_object_or_404(Vendor, pk=vendor_id)
        profile = request.user.wedding_profile
        status = request.POST.get('status', 'candidate')
        
        # 이미 존재하는 경우 업데이트, 없으면 생성
        selection, created = UserVendorSelection.objects.update_or_create(
            profile=profile,
            vendor=vendor,
            defaults={'status': status}
        )
        
        return redirect('vendor_detail', vendor_id=vendor.id)
    return redirect('vendor_list')

@login_required
def my_candidates_list(request):
    """
    후보 업체 목록 (status='candidate')
    """
    if hasattr(request.user, 'wedding_profile'):
        profile = request.user.wedding_profile
        candidates = UserVendorSelection.objects.filter(
            profile=profile,
            status='candidate'
        ).select_related('vendor', 'vendor__category')
    else:
        candidates = []

    context = {
        'candidates': candidates,
    }
    return render(request, 'vendors/my_candidates_list.html', context)
