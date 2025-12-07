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
    today = timezone.now().date()
    
    # 1. POST Handling
    if request.method == 'POST':
        # 1-1. Task Assignment (Schedule)
        if 'task_id' in request.POST:
            task_id = request.POST.get('task_id')
            date_str = request.POST.get('date')
            try:
                task = ScheduleTask.objects.get(id=task_id, profile=profile)
                task.date = datetime.strptime(date_str, '%Y-%m-%d').date()
                task.save()
            except (ScheduleTask.DoesNotExist, ValueError):
                pass
            return redirect(f'{request.path}?date={date_str}')

        # 1-2. Daily Log (Memo)
        elif 'log_content' in request.POST:
            log_content = request.POST.get('log_content')
            date_str = request.POST.get('date')
            try:
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                DailyLog.objects.update_or_create(
                    user=request.user,
                    date=log_date,
                    defaults={'content': log_content}
                )
            except ValueError:
                pass
            return redirect(f'{request.path}?date={date_str}')
            
        # 1-3. Question
        elif 'question_content' in request.POST:
            q_title = request.POST.get('question_title')
            q_content = request.POST.get('question_content')
            Question.objects.create(
                author=request.user,
                title=q_title,
                content=q_content
            )
            return redirect('dashboard')
            
        # 1-4. Toggle Task Completion (Checklist)
        elif 'toggle_task_id' in request.POST:
            task_id = request.POST.get('toggle_task_id')
            try:
                task = ScheduleTask.objects.get(id=task_id, profile=profile)
                task.is_done = not task.is_done
                task.save()
            except ScheduleTask.DoesNotExist:
                pass

            return redirect(reverse('dashboard') + '?tab=todo')
    
    # 2. D-Day Calculation
    d_day = (profile.wedding_date - today).days
    
    # 3. Calendar Logic
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
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
    if month == 12:
        month_end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        month_end = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
    month_logs_qs = DailyLog.objects.filter(
        user=request.user, 
        date__range=(month_start, month_end)
    )
    month_logs_map = {log.date: log.content for log in month_logs_qs}
    
    month_tasks = ScheduleTask.objects.filter(
        profile=profile,
        date__range=(month_start, month_end)
    ).values_list('date', flat=True)
    
    # Prepare calendar data
    calendar_data = []
    selected_date_str = request.GET.get('date')
    
    for week in month_days:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': 0, 'is_empty': True})
            else:
                current_date = datetime(year, month, day).date()
                is_today = (current_date == today)
                is_wedding_day = (current_date == profile.wedding_date)
                
                log_content = month_logs_map.get(current_date, '')
                has_log = (current_date in month_logs_map)
                has_task = (current_date in month_tasks)
                
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
                    'log_content': log_content,
                    'has_task': has_task,
                    'date_obj': current_date,
                })
        calendar_data.append(week_data)

    # 4. Data for Modal (Unscheduled Tasks)
    # Tasks that are not done OR don't have a date yet
    from django.db.models import Q
    unscheduled_tasks = ScheduleTask.objects.filter(
        profile=profile
    ).filter(
        Q(date__isnull=True) | Q(is_done=False)
    ).order_by('date')

    # 5. Data for Right Panel (Upcoming Mixed List)
    # 5-1. Upcoming Tasks
    upcoming_tasks_qs = ScheduleTask.objects.filter(
        profile=profile,
        date__gte=today
    )
    
    # 5-2. Upcoming Logs
    upcoming_logs_qs = DailyLog.objects.filter(
        user=request.user,
        date__gte=today
    )
    
    # 5-3. Separate Lists
    upcoming_schedules = []
    for task in upcoming_tasks_qs.order_by('date')[:7]:
        upcoming_schedules.append({
            'type': 'task',
            'id': task.id,
            'title': task.title,
            'date': task.date,
            'd_day': (task.date - today).days,
            'is_done': task.is_done
        })
        
    upcoming_memos = []
    for log in upcoming_logs_qs.order_by('date')[:7]:
        # Use full content for display in the list (will be line-broken in template)
        content = log.content if log.content else "메모"
        upcoming_memos.append({
            'type': 'alarm',
            'id': log.id,
            'title': content,
            'date': log.date,
            'd_day': (log.date - today).days
        })
        
    # No longer need upcoming_mixed_list, passing separate lists

    # 6. Checklist Data (TimeTable style)
    # Sort by d_day_offset (Ascending) e.g. -300 -> -200 -> -5
    checklist = ScheduleTask.objects.filter(
        profile=profile
    ).order_by('d_day_offset', 'id')

    # Navigation links
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    month_name = f"{year}년 {month}월"

    # Context
    context = {
        'profile': profile,
        'd_day': d_day,
        'calendar': calendar_data,
        'current_year': year,
        'current_month': month,
        'month_name': month_name,
        'today': today,
        'unscheduled_tasks': unscheduled_tasks,     # For Modal
        'upcoming_schedules': upcoming_schedules,   # For Right Panel (Tab 1)
        'upcoming_memos': upcoming_memos,           # For Right Panel (Tab 2)
        'checklist': checklist,                     # New Sorted Checklist
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'year_range': range(today.year - 5, today.year + 6),
        
        # Vendor & Community (Keeping existing)
        'vendor_categories': VendorCategory.objects.all(),
        'recommended_vendors': Vendor.objects.all()[:4],
        'notices': Notice.objects.all(),
        'questions': Question.objects.all(),
    }
    return render(request, 'weddings/dashboard.html', context)
