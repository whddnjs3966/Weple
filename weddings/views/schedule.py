from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q, Sum
from weddings.models import WeddingProfile, ScheduleTask, DailyLog, WeddingGroup
import calendar
from datetime import datetime, timedelta
import json

@login_required
def schedule_list(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        if not group: return redirect('onboarding')
    except WeddingProfile.DoesNotExist: return redirect('onboarding')

    today = timezone.now().date()

    # POST Handling
    if request.method == 'POST':
        # Task Assignment (Schedule)
        if 'task_id' in request.POST:
            task_id = request.POST.get('task_id')
            date_str = request.POST.get('date')
            try:
                task = ScheduleTask.objects.get(id=task_id, group=group) # Check ownership by group
                task.date = datetime.strptime(date_str, '%Y-%m-%d').date()
                task.save()
            except (ScheduleTask.DoesNotExist, ValueError):
                pass
            return redirect(f'{reverse("schedule_list")}?date={date_str}&year={date_str[:4]}&month={int(date_str[5:7])}')

        # Daily Log (Memo)
        elif 'log_content' in request.POST:
            log_content = request.POST.get('log_content')
            date_str = request.POST.get('date')
            if date_str:
                try:
                    log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    DailyLog.objects.update_or_create(
                        group=group, # Associate with Group
                        date=log_date,
                        defaults={'content': log_content}
                    )
                except ValueError:
                    pass
                return redirect(f'{reverse("schedule_list")}?date={date_str}&year={date_str[:4]}&month={int(date_str[5:7])}')
                
    # Calendar Logic
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
    
    # Fetch tasks for the month (efficiently)
    month_tasks_qs = ScheduleTask.objects.filter(
        group=group,
        date__range=(month_start, month_end)
    ).select_related('group')
    
    # Map date -> list of tasks
    month_tasks_map = {}
    for t in month_tasks_qs:
        if t.date not in month_tasks_map:
            month_tasks_map[t.date] = []
        month_tasks_map[t.date].append(t)

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
                
                # Get tasks for this day
                day_tasks = month_tasks_map.get(current_date, [])
                
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
                    'tasks': day_tasks, # Pass list of tasks
                    'date_obj': current_date,
                })
        calendar_data.append(week_data)

    # Data for Modal (Unscheduled Tasks)
    unscheduled_tasks = ScheduleTask.objects.filter(
        group=group
    ).filter(
        Q(date__isnull=True) | Q(is_done=False)
    ).order_by('date')

    # Timeline Events: Combined Tasks + Logs (Today ~ Wedding Day)
    timeline_events = []
    
    # Filter range
    start_date = today
    end_date = group.wedding_date if group.wedding_date else today + timedelta(days=365) # Default 1 year if set
    
    tasks = ScheduleTask.objects.filter(
        group=group,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')

    logs = DailyLog.objects.filter(
        group=group,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')

    for t in tasks:
        d_day = (t.date - today).days
        timeline_events.append({
            'type': 'task',
            'title': t.title,
            'date': t.date,
            'd_day': d_day,
            'category': t.get_category_display(),
            'category_code': t.category,
            'is_done': t.is_done
        })

    for l in logs:
        d_day = (l.date - today).days
        timeline_events.append({
            'type': 'log',
            'title': l.content[:20] + "..." if len(l.content) > 20 else l.content,
            'date': l.date,
            'd_day': d_day,
            'category': 'Memo', # Distinguish memos
            'category_code': 'memo'
        })

    # Sort combined events by date
    timeline_events.sort(key=lambda x: x['date'])

    # Smart D-Day Logic (Returning 3 Recommendations)
    d_day_actions = []
    if group.wedding_date:
        days_left = (group.wedding_date - today).days
        if days_left > 180:
            d_day_actions = [
                {"title": "상견례 장소 예약", "desc": "양가 어른들을 모실 조용한 장소를 알아보세요."},
                {"title": "예식장 투어", "desc": "원하는 날짜와 보증인원을 고려해 투어를 시작하세요."},
                {"title": "예산 계획 수립", "desc": "전체적인 결혼 준비 예산을 파트너와 상의하세요."}
            ]
        elif days_left > 120:
            d_day_actions = [
                {"title": "스드메 계약", "desc": "스튜디오, 드레스, 메이크업 업체를 확정하세요."},
                {"title": "본식 스냅 예약", "desc": "인기 있는 스냅/DVD 업체는 빨리 마감됩니다."},
                {"title": "신혼여행지 결정", "desc": "항공권과 숙소를 미리 예약하면 저렴합니다."}
            ]
        elif days_left > 60:
            d_day_actions = [
                {"title": "청첩장 주문", "desc": "청첩장 디자인을 고르고 초안을 확인하세요."},
                {"title": "예물/예복 맞춤", "desc": "제작 기간을 고려해 미리 방문 상담을 받으세요."},
                {"title": "하객 리스트 정리", "desc": "초대할 하객 명단을 1차적으로 정리해보세요."}
            ]
        elif days_left > 30:
            d_day_actions = [
                {"title": "사회자/주례 섭외", "desc": "결혼식을 이끌어줄 분들에게 부탁을 드려보세요."},
                {"title": "식중 영상 제작", "desc": "식전 영상과 성장 동영상을 준비할 시기입니다."},
                {"title": "부케 선정", "desc": "드레스와 홀 분위기에 어울리는 부케를 고르세요."}
            ]
        elif days_left > 7:
            d_day_actions = [
                {"title": "본식 드레스 가봉", "desc": "최종적으로 드레스 상태와 사이즈를 점검하세요."},
                {"title": "식권/방명록 준비", "desc": "당일 사용할 물품들을 꼼꼼히 챙겨두세요."},
                {"title": "컨디션 조절", "desc": "충분한 수면과 휴식으로 최상의 컨디션을 만드세요."}
            ]
        elif days_left >= 0:
            d_day_actions = [
                {"title": "준비물 최종 점검", "desc": "반지, 포토테이블 사진 등 당일 준비물을 확인하세요."},
                {"title": "마음의 준비", "desc": "긴장하지 말고 행복한 하루를 즐길 준비를 하세요."},
                {"title": "부모님께 감사 인사", "desc": "키워주신 은혜에 감사하는 마음을 전하세요."}
            ]
        else:
            d_day_actions = [
                {"title": "신혼여행 즐기기", "desc": "행복한 추억을 많이 만드세요!"},
                {"title": "감사 인사 드리기", "desc": "와주신 하객분들께 감사의 연락을 돌리세요."},
                {"title": "혼인신고", "desc": "법적인 부부가 되기 위한 절차를 확인하세요."}
            ]
    else:
        d_day_actions = [
            {"title": "결혼 날짜 정하기", "desc": "행복한 시작을 위한 날짜를 먼저 확정해주세요."},
            {"title": "웨딩홀 알아보기", "desc": "어떤 분위기의 결혼식을 원하는지 상의해보세요."},
            {"title": "예산 논의하기", "desc": "대략적인 결혼 준비 자금을 확인해보세요."}
        ]
        days_left = None

    # Navigation links
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        'profile': profile,
        'group': group,
        'calendar': calendar_data,
        'current_year': year,
        'current_month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'year_range': range(today.year - 5, today.year + 6),
        'unscheduled_tasks': unscheduled_tasks,
        
        # New Context Data
        'timeline_events': timeline_events,
        'd_day_actions': d_day_actions,
        'days_left': days_left,
    }
    return render(request, 'weddings/schedule_main.html', context)

@login_required
def checklist_manage(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        if not group: return redirect('onboarding')
    except WeddingProfile.DoesNotExist: return redirect('onboarding')

    if request.method == 'POST':
        # Toggle Task Completion
        if 'toggle_task_id' in request.POST:
            task_id = request.POST.get('toggle_task_id')
            try:
                task = ScheduleTask.objects.get(id=task_id, group=group)
                task.is_done = not task.is_done
                task.save()
            except ScheduleTask.DoesNotExist:
                pass
            return redirect('checklist_manage')

        # Bulk Delete
        elif 'delete_task_ids' in request.POST:
            ids_str = request.POST.get('delete_task_ids', '')
            if ids_str:
                try:
                    if ids_str.startswith('[') and ids_str.endswith(']'):
                         ids = json.loads(ids_str)
                         ids = [int(i) for i in ids]
                    else:
                        ids = [int(id_str) for id_str in ids_str.split(',')]
                    
                    ScheduleTask.objects.filter(id__in=ids, group=group).delete()
                except (ValueError, Exception):
                    pass
            return redirect('checklist_manage')

        # Create New Task
        elif 'new_task_title' in request.POST:
            title = request.POST.get('new_task_title')
            budget_str = request.POST.get('new_task_budget', '0')
            description = request.POST.get('new_task_memo', '')
            d_day_input = request.POST.get('new_task_d_day') # This is number now, "000"
            
            try:
                budget = int(budget_str) if budget_str else 0
            except ValueError:
                budget = 0
                
            task_date = None
            d_day_offset = None
            
            if d_day_input:
                try:
                    # User inputs "100" meaning D-100.
                    # d_day_offset should be -100.
                    days_left = int(d_day_input)
                    d_day_offset = -days_left
                    
                    if group.wedding_date:
                         # date = wedding_date + offset (e.g. wedding - 100 days)
                         task_date = group.wedding_date + timedelta(days=d_day_offset)
                except ValueError:
                    pass
            
            ScheduleTask.objects.create(
                group=group,
                title=title,
                estimated_budget=budget,
                description=description,
                date=task_date,
                d_day_offset=d_day_offset, # Also save offset if model has it
                category='OTHER'
            )
            return redirect('checklist_manage')
            
        # Update Task Budget
        elif 'update_budget_task_id' in request.POST:
            task_id = request.POST.get('update_budget_task_id')
            new_budget_str = request.POST.get('budget_value', '0')
            try:
                # Remove commas if any
                new_budget = int(new_budget_str.replace(',', ''))
                task = ScheduleTask.objects.get(id=task_id, group=group)
                task.estimated_budget = new_budget
                task.save()
            except (ValueError, ScheduleTask.DoesNotExist):
                pass
            return redirect('checklist_manage')
    
    # Checklist Data (TimeTable style)
    checklist = ScheduleTask.objects.filter(
        group=group
    ).order_by('d_day_offset', 'id')

    total_budget = checklist.aggregate(total=Sum('estimated_budget'))['total'] or 0
    
    context = {
        'profile': profile,
        'group': group,
        'checklist': checklist,
        'total_budget': total_budget,
    }
    return render(request, 'weddings/checklist_main.html', context)
