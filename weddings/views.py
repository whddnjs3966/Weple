from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WeddingProfile, ScheduleTask, DailyLog, Notice, Question, WeddingGroup
from vendors.models import Vendor, VendorCategory
from .forms import WeddingProfileForm, GroupJoinForm, WeddingGroupForm
import calendar
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages

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
            # Profile fields are already cleaned but form.save() for existing instance is tricky with get_or_create
            # So let's manually update.
            profile.wedding_date = wedding_date
            profile.group = group
            profile.save()
            
            return redirect('dashboard')
    else:
        form = WeddingProfileForm()

    return render(request, 'weddings/onboarding.html', {
        'form': form
    })

@login_required
def dashboard(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        if not group:
            # Profile exists but no group? Go to onboarding or fix
            return redirect('onboarding')
    except WeddingProfile.DoesNotExist:
        return redirect('onboarding')

    today = timezone.now().date()
    
    # Update wedding_date handling (from Group)
    
    # 1. POST Handling
    if request.method == 'POST':
        # 1-0. Update Group Info (Date) - handled via separate endpoint or here? 
        # User requested modal update. Let's handle it here if easy, or separate view.
        # Let's check for specific hidden input.
        if 'update_date' in request.POST:
             new_date_str = request.POST.get('wedding_date')
             try:
                 new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
                 group.wedding_date = new_date
                 group.save()
             except ValueError:
                 pass
             return redirect('dashboard')

        # 1-1. Task Assignment (Schedule)
        if 'task_id' in request.POST:
            task_id = request.POST.get('task_id')
            date_str = request.POST.get('date')
            try:
                task = ScheduleTask.objects.get(id=task_id, group=group) # Check ownership by group
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
                    group=group, # Associate with Group
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
                task = ScheduleTask.objects.get(id=task_id, group=group)
                task.is_done = not task.is_done
                task.save()
            except ScheduleTask.DoesNotExist:
                pass
            return redirect(reverse('dashboard') + '?tab=todo')
    
    # 2. D-Day Calculation
    if group.wedding_date:
        d_day = (group.wedding_date - today).days
    else:
        d_day = None
    
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
        group=group, 
        date__range=(month_start, month_end)
    )
    month_logs_map = {log.date: log.content for log in month_logs_qs}
    
    month_tasks = ScheduleTask.objects.filter(
        group=group,
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
                is_wedding_day = (current_date == group.wedding_date)
                
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
    unscheduled_tasks = ScheduleTask.objects.filter(
        group=group
    ).filter(
        Q(date__isnull=True) | Q(is_done=False)
    ).order_by('date')

    # 5. Data for Right Panel (Upcoming Mixed List)
    # 5-1. Upcoming Tasks
    upcoming_tasks_qs = ScheduleTask.objects.filter(
        group=group,
        date__gte=today
    )
    
    # 5-2. Upcoming Logs
    upcoming_logs_qs = DailyLog.objects.filter(
        group=group,
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
            'd_day': (task.date - today).days if task.date else None,
            'is_done': task.is_done
        })
        
    upcoming_memos = []
    for log in upcoming_logs_qs.order_by('date')[:7]:
        content = log.content if log.content else "메모"
        upcoming_memos.append({
            'type': 'alarm',
            'id': log.id,
            'title': content,
            'date': log.date,
            'd_day': (log.date - today).days
        })

    # 6. Checklist Data (TimeTable style)
    checklist = ScheduleTask.objects.filter(
        group=group
    ).order_by('d_day_offset', 'id')

    # Navigation links
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    month_name = f"{year}년 {month}월"

    context = {
        'profile': profile,
        'group': group,  # Passed for invite_code display
        'd_day': d_day,
        'calendar': calendar_data,
        'current_year': year,
        'current_month': month,
        'month_name': month_name,
        'today': today,
        'unscheduled_tasks': unscheduled_tasks,
        'upcoming_schedules': upcoming_schedules,
        'upcoming_memos': upcoming_memos,
        'checklist': checklist,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'year_range': range(today.year - 5, today.year + 6),
        
        'vendor_categories': VendorCategory.objects.all(),
        'recommended_vendors': Vendor.objects.all()[:4],
        'notices': Notice.objects.all(),
        'questions': Question.objects.all(),
    }
    return render(request, 'weddings/dashboard.html', context)
