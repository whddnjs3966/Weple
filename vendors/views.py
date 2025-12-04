from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Vendor, VendorCategory, UserVendorSelection

@login_required
def vendor_list(request):
    """
    업체 목록 조회 및 필터링
    """
    category_slug = request.GET.get('category')
    region = request.GET.get('region')
    
    vendors = Vendor.objects.all()
    
    if category_slug:
        vendors = vendors.filter(category__slug=category_slug)
    
    if region:
        vendors = vendors.filter(Q(region_sido__contains=region) | Q(region_sigungu__contains=region))
        
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
