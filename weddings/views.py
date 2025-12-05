from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WeddingProfile, ScheduleTask, DailyLog, Notice, Question
from vendors.models import Vendor, VendorCategory
from .forms import WeddingProfileForm
import calendar
from datetime import datetime, timedelta
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
    profile = get_object_or_404(WeddingProfile, user=request.user)
    
    # 1. D-Day Calculation
    today = timezone.now().date()
    d_day = (profile.wedding_date - today).days
    
    # 2. Calendar Logic
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Handle month navigation
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
        
    cal = calendar.Calendar(firstweekday=6) # Sunday start
    month_days = cal.monthdayscalendar(year, month)
    
    # Get logs and tasks for the month
    month_start = datetime(year, month, 1).date()
    # Calculate month end correctly
    if month == 12:
        month_end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        month_end = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
    month_logs = DailyLog.objects.filter(
        user=request.user, 
        date__range=(month_start, month_end)
    ).values_list('date', flat=True)
    
    month_tasks = ScheduleTask.objects.filter(
        profile=profile,
        date__range=(month_start, month_end)
    ).values_list('date', flat=True)

    # Prepare calendar data
    calendar_data = []
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': 0, 'is_empty': True})
            else:
                current_date = datetime(year, month, day).date()
                is_today = (current_date == today)
                is_wedding_day = (current_date == profile.wedding_date)
                has_log = (current_date in month_logs)
                has_task = (current_date in month_tasks)
                
                # Check if this date is selected
                selected_date_str = request.GET.get('date')
                if selected_date_str:
                    is_selected = (str(current_date) == selected_date_str)
                else:
                    is_selected = is_today

                week_data.append({
                    'day': day,
                    'is_empty': False,
                    'is_today': is_today,
                    'is_selected': is_selected,
                    'is_wedding_day': is_wedding_day,
                    'has_log': has_log,
                    'has_task': has_task,
                    'date_obj': current_date,
                })
        calendar_data.append(week_data)

    # 3. Selected Date Details (Right Pane)
    selected_date_str = request.GET.get('date', str(today))
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = today

    # Handle Log Submission
    if request.method == 'POST':
        if 'log_content' in request.POST:
            log_content = request.POST.get('log_content')
            log_date_str = request.POST.get('date')
            log_date = datetime.strptime(log_date_str, '%Y-%m-%d').date()
            
            DailyLog.objects.update_or_create(
                user=request.user,
                date=log_date,
                defaults={'content': log_content}
            )
            return redirect(f'{request.path}?date={log_date}&year={year}&month={month}')
        
        elif 'question_content' in request.POST:
            q_title = request.POST.get('question_title')
            q_content = request.POST.get('question_content')
            Question.objects.create(
                author=request.user,
                title=q_title,
                content=q_content
            )
            return redirect('dashboard')

    current_log = DailyLog.objects.filter(user=request.user, date=selected_date).first()
    selected_date_tasks = ScheduleTask.objects.filter(profile=profile, date=selected_date)

    # 4. Timeline Data (Upcoming Tasks)
    upcoming_tasks = ScheduleTask.objects.filter(
        profile=profile,
        date__gte=today,
        is_done=False
    ).order_by('date')[:10]

    # 5. Checklist Data (Grouped by Category)
    all_tasks = ScheduleTask.objects.filter(profile=profile).order_by('is_done', 'date')
    
    # Group tasks by category
    checklist_data = {}
    for code, name in ScheduleTask.CATEGORY_CHOICES:
        tasks = all_tasks.filter(category=code)
        if tasks.exists():
            checklist_data[name] = tasks

    # Navigation links
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    month_name = f"{year}년 {month}월"

    # 6. Vendor Data
    vendor_categories = VendorCategory.objects.all()
    recommended_vendors = Vendor.objects.all()[:4]  # Simple recommendation logic for now

    # 7. Community Data
    notices = Notice.objects.all()
    questions = Question.objects.all()

    context = {
        'profile': profile,
        'd_day': d_day,
        'calendar': calendar_data,
        'current_year': year,
        'current_month': month,
        'month_name': month_name,
        'today': today,
        'selected_date': selected_date,
        'current_log': current_log,
        'selected_date_tasks': selected_date_tasks,
        'upcoming_tasks': upcoming_tasks,
        'checklist_data': checklist_data,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'year_range': range(today.year - 5, today.year + 6),
        'vendor_categories': vendor_categories,
        'recommended_vendors': recommended_vendors,
        'notices': notices,
        'questions': questions,
    }
    return render(request, 'weddings/dashboard.html', context)
    # Force reload
