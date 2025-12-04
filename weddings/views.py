from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WeddingProfile, ScheduleTask, DailyLog
from .forms import WeddingProfileForm
import calendar
from datetime import datetime
from django.urls import reverse


@login_required
def onboarding(request):
    """
    최초 로그인 시 웨딩 정보를 입력받는 뷰
    """
    # 이미 프로필이 있다면 대시보드로 이동
    if hasattr(request.user, 'wedding_profile'):
        return redirect('dashboard')

    if request.method == 'POST':
        form = WeddingProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('dashboard')
    else:
        form = WeddingProfileForm()

    return render(request, 'weddings/onboarding.html', {'form': form})

@login_required
def dashboard(request):
    """
    메인 대시보드: D-Day, 캘린더, 이번 주 할 일 등 표시
    """
    try:
        profile = request.user.wedding_profile
    except WeddingProfile.DoesNotExist:
        return redirect('onboarding')

    # Handle Daily Log
    today = timezone.localdate()
    
    # Get selected date from query param or default to today
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    current_log = DailyLog.objects.filter(user=request.user, date=selected_date).first()
    
    if request.method == 'POST' and 'log_content' in request.POST:
        content = request.POST.get('log_content')
        # Get date from hidden input or query param, fallback to selected_date
        post_date_str = request.POST.get('date')
        if post_date_str:
             try:
                post_date = datetime.strptime(post_date_str, '%Y-%m-%d').date()
             except ValueError:
                post_date = selected_date
        else:
            post_date = selected_date

        # Re-fetch log for the post_date to ensure we update the correct one
        log_to_update = DailyLog.objects.filter(user=request.user, date=post_date).first()

        if log_to_update:
            log_to_update.content = content
            log_to_update.save()
        else:
            DailyLog.objects.create(user=request.user, date=post_date, content=content)
        
        return redirect(f'{reverse("dashboard")}?date={post_date.strftime("%Y-%m-%d")}')

    # Calendar Logic
    year_param = request.GET.get('year')
    month_param = request.GET.get('month')

    if year_param and month_param:
        try:
            year = int(year_param)
            month = int(month_param)
        except ValueError:
            year = today.year
            month = today.month
    else:
        year = today.year
        month = today.month

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    # Calculate previous and next month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Get logs for the current month to mark on calendar
    # Get logs for the current month to mark on calendar
    month_logs = DailyLog.objects.filter(
        user=request.user, 
        date__year=year, 
        date__month=month
    ).values_list('date__day', flat=True)

    # D-Day Calculation
    d_day = (profile.wedding_date - today).days
    
    # 이번 주 할 일 (오늘 ~ 7일 후)
    upcoming_tasks = ScheduleTask.objects.filter(
        profile=profile,
        date__gte=today,
        date__lte=today + timezone.timedelta(days=7),
        is_done=False
    ).order_by('date')

    # 놓친 할 일 (오늘 이전, 미완료)
    overdue_tasks = ScheduleTask.objects.filter(
        profile=profile,
        date__lt=today,
        is_done=False
    ).order_by('date')
    
    # Vendor Status
    vendor_status = {
        'venue': profile.vendor_selections.filter(vendor__category__slug='venue', status='final').exists(),
        'studio': profile.vendor_selections.filter(vendor__category__slug='studio', status='final').exists(),
        'dress': profile.vendor_selections.filter(vendor__category__slug='dress', status='final').exists(),
        'makeup': profile.vendor_selections.filter(vendor__category__slug='makeup', status='final').exists(),
    }

    context = {
        'profile': profile,
        'd_day': d_day,
        'upcoming_tasks': upcoming_tasks,
        'overdue_tasks': overdue_tasks,
        'vendor_status': vendor_status,
        'calendar': cal,
        'current_year': year,
        'current_month': month,
        'month_name': month_name,
        'today': today,
        'month_logs': month_logs,
        'current_log': current_log,
        'wedding_date': profile.wedding_date,
        'selected_date': selected_date,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    return render(request, 'weddings/dashboard.html', context)
    # Force reload
