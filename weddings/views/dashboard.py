from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from weddings.models import WeddingProfile, WeddingGroup
from weddings.forms import WeddingProfileForm
from datetime import datetime

@login_required
def onboarding(request):
    """
    최초 로그인 시 웨딩 정보를 입력받는 뷰.
    그룹 생성(새로 시작하기)만 구현 (초대 코드는 UI만 존재).
    """
    if hasattr(request.user, 'wedding_profile') and request.user.wedding_profile.group:
        return redirect('dashboard')

    if request.method == 'POST':
        # New Wedding Flow
        form = WeddingProfileForm(request.POST)
        
        if form.is_valid():
            # 1. Create Profile object (don't save yet)
            profile, created = WeddingProfile.objects.get_or_create(user=request.user)
            
            # 2. Extract minimal data (wedding_date)
            wedding_date = form.cleaned_data.get('wedding_date')
            
            # 3. Create Group automatically
            group = WeddingGroup.objects.create(wedding_date=wedding_date)
            
            # 4. Link Group and save Profile
            # profile.wedding_date = wedding_date # Removed
            profile.group = group
            profile.save()
            
            return redirect('dashboard')
    else:
        form = WeddingProfileForm()

    return render(request, 'weddings/onboarding.html', {
        'form': form
    })

@login_required
def dashboard_main(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        if not group:
            # Profile exists but no group? Go to onboarding or fix
            return redirect('onboarding')
    except WeddingProfile.DoesNotExist:
        return redirect('onboarding')

    today = timezone.now().date()
    
    # POST Handling
    if request.method == 'POST':
        # 1. Update Profile Name
        if 'update_profile_name' in request.POST:
            new_name = request.POST.get('profile_name')
            if new_name:
                request.user.first_name = new_name  # first_name 필드를 이름으로 사용
                request.user.save()
            # Do not return yet, check for date update

        # 2. Update Wedding Date
        if 'update_date' in request.POST:
             new_date_str = request.POST.get('wedding_date')
             try:
                 new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
                 group.wedding_date = new_date
                 group.save()
                 
                 # Sync profile for consistency if needed
                 profile.wedding_date = new_date
                 profile.save()
             except (ValueError, TypeError):
                 # Handle invalid date format or empty string
                 pass
                 
        return redirect('dashboard')

    if group.wedding_date:
        d_day = (group.wedding_date - today).days
    else:
        d_day = None
    
    context = {
        'profile': profile,
        'group': group,  # Passed for invite_code display
        'd_day': d_day,
        'today': today,
    }
    return render(request, 'weddings/dashboard.html', context)
