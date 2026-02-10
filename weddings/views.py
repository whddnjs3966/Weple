from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import WeddingProfile, ScheduleTask, DailyLog, Notice, Post, Comment, WeddingGroup
from vendors.models import Vendor, VendorCategory, UserVendorSelection
from .forms import WeddingProfileForm, GroupJoinForm, WeddingGroupForm, PostForm, CommentForm
import calendar
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import Q, Sum, Count
from django.contrib import messages
import json

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

    # Data for Modal (Unscheduled Tasks)
    unscheduled_tasks = ScheduleTask.objects.filter(
        group=group
    ).filter(
        Q(date__isnull=True) | Q(is_done=False)
    ).order_by('date')

    # Data for Right Panel (Upcoming Mixed List)
    # Upcoming Tasks
    upcoming_tasks_qs = ScheduleTask.objects.filter(
        group=group,
        date__gte=today
    ).order_by('date')[:7]
    
    # Upcoming Logs
    upcoming_logs_qs = DailyLog.objects.filter(
        group=group,
        date__gte=today
    ).order_by('date')[:7]
    
    # Separate Lists
    upcoming_schedules = []
    for task in upcoming_tasks_qs:
        upcoming_schedules.append({
            'type': 'task',
            'id': task.id,
            'title': task.title,
            'date': task.date,
            'd_day': (task.date - today).days if task.date else None,
            'is_done': task.is_done
        })
        
    upcoming_memos = []
    for log in upcoming_logs_qs:
        content = log.content if log.content else "메모"
        upcoming_memos.append({
            'type': 'alarm',
            'id': log.id,
            'title': content,
            'date': log.date,
            'd_day': (log.date - today).days
        })

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
        'upcoming_schedules': upcoming_schedules,
        'upcoming_memos': upcoming_memos,
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


@login_required
def vendor_main(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        if not group: pass
    except WeddingProfile.DoesNotExist:
        pass

    context = {
        'my_selected_vendors': UserVendorSelection.objects.filter(profile=profile, status='final').select_related('vendor', 'vendor__category'),
        'vendor_categories': VendorCategory.objects.all(),
        'recommended_vendors': Vendor.objects.all()[:4],
    }
    return render(request, 'weddings/vendor_main.html', context)

@login_required
def community_main(request):
    try:
        profile = request.user.wedding_profile
        group = profile.group
        # Community handling might not strictly need group, but consistency is good
        if not group: pass
    except WeddingProfile.DoesNotExist:
        pass

    # Community Search & Sort
    search_query = request.GET.get('q', '')
    sort_option = request.GET.get('sort', 'date')

    posts_qs = Post.objects.annotate(
        comment_count=Count('comments', distinct=True),
        recommendation_count=Count('recommendations', distinct=True)
    )

    # Filter by search query
    if search_query:
        posts_qs = posts_qs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__first_name__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    # Sort posts
    if sort_option == 'likes':
        posts_qs = posts_qs.order_by('-recommendation_count', '-created_at')
    else:  # default 'date'
        posts_qs = posts_qs.order_by('-created_at')

    notices = Notice.objects.annotate(comment_count=Count('comments'))
    
    context = {
        # 'profile': profile, # Can pass if needed for header, but base.html usually handles it if user is logged in
        'posts': posts_qs,
        'notices': notices,
        'search_query': search_query,
        'sort_option': sort_option,
    }
    return render(request, 'weddings/community_main.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_main')
    else:
        form = PostForm()
    return render(request, 'weddings/post_form.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'weddings/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def comment_create(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        notice_id = request.POST.get('notice_id')
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            
            if post_id:
                post = get_object_or_404(Post, id=post_id)
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
            elif notice_id:
                notice = get_object_or_404(Notice, id=notice_id)
                comment.notice = notice
                comment.save()
                # Redirect to community main or if there's a notice detail, go there.
                return redirect('community_main')
    
    return redirect('community_main')

@login_required
def post_recommend(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.recommendations.filter(id=request.user.id).exists():
        post.recommendations.remove(request.user)
    else:
        post.recommendations.add(request.user)
    
    # Redirect back to where the user came from (detail or dashboard)
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('community_main')

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('community_main')

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'weddings/post_form.html', {'form': form})
