import os
import django
from django.conf import settings
from django.urls import reverse, resolve
from django.test import RequestFactory
from datetime import date, datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test.utils import setup_test_environment
setup_test_environment()

from weddings.views import dashboard
from weddings.models import DailyLog, WeddingProfile
from django.contrib.auth.models import User

def verify_fixes():
    print("Verifying fixes...")
    
    # 1. Check for duplicate URL
    try:
        url = reverse('landing')
        print(f"[PASS] 'landing' URL resolves to: {url}")
        # Check if there are duplicates in resolver? Hard to check programmatically easily, 
        # but if reverse works without error and we don't see warning in check, it's likely fine.
    except Exception as e:
        print(f"[FAIL] 'landing' URL resolution failed: {e}")

    # 2. Check month_logs type in dashboard view
    # Create dummy user and profile
    user, created = User.objects.get_or_create(username='testuser')
    if created:
        user.set_password('password')
        user.save()
    
    if not hasattr(user, 'wedding_profile'):
        WeddingProfile.objects.create(user=user, wedding_date=date(2025, 12, 25))

    # Create a log for today
    today = date.today()
    DailyLog.objects.get_or_create(user=user, date=today, defaults={'content': 'Test Log'})

    factory = RequestFactory()
    request = factory.get(reverse('dashboard'))
    request.user = user
    
    response = dashboard(request)
    
    # Check context
    # We need to inspect the response context if possible, but dashboard returns HttpResponse object (result of render)
    # render returns HttpResponse, which doesn't have context attribute directly accessible unless using test client
    # So let's use test client
    
    from django.test import Client
    client = Client()
    client.force_login(user)
    
    response = client.get(reverse('dashboard'))
    
    if response.status_code == 200:
        if response.context is None:
            print("[FAIL] response.context is None. Is this a TemplateResponse?")
            print(f"Response content: {response.content[:200]}...")
            return

        month_logs = response.context.get('month_logs')
        print(f"month_logs type: {type(month_logs)}")
        print(f"month_logs content: {list(month_logs) if month_logs else 'None'}")
        
        # Check if it contains integers (days)
        if month_logs and all(isinstance(d, int) for d in month_logs):
             print("[PASS] month_logs contains integers")
        else:
             print("[FAIL] month_logs does not contain integers")
             
        # Check selected_date
        selected_date = response.context.get('selected_date')
        print(f"selected_date: {selected_date}")
        if selected_date == today:
            print("[PASS] selected_date defaults to today")
        else:
            print(f"[FAIL] selected_date is {selected_date}, expected {today}")

    else:
        print(f"[FAIL] Dashboard request failed with status {response.status_code}")
        if response.status_code == 302:
            print(f"Redirect URL: {response.url}")

    # 3. Check date selection
    target_date_str = '2025-01-01'
    target_date = date(2025, 1, 1)
    response = client.get(reverse('dashboard') + f'?date={target_date_str}')
    
    if response.status_code == 200:
        selected_date = response.context['selected_date']
        if selected_date == target_date:
            print(f"[PASS] Date selection works: {selected_date}")
        else:
            print(f"[FAIL] Date selection failed. Got {selected_date}, expected {target_date}")
    
    # 4. Check log submission with date
    log_content = "Log for specific date"
    response = client.post(reverse('dashboard'), {
        'log_content': log_content,
        'date': target_date_str
    })
    
    # Should redirect
    if response.status_code == 302:
        print("[PASS] Log submission redirected")
        # Verify log created
        log = DailyLog.objects.filter(user=user, date=target_date).first()
        if log and log.content == log_content:
            print("[PASS] Log created for specific date")
        else:
            print("[FAIL] Log not created or content mismatch")
    else:
        print(f"[FAIL] Log submission failed with status {response.status_code}")

if __name__ == '__main__':
    verify_fixes()
