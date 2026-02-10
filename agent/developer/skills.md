# Developer Agent Skills — Weple Project

> **역할**: 백엔드 아키텍트 & 풀스택 개발자
> **핵심 기술**: Python · Django · REST API · Naver/Google API 연동
> **원칙**: WeddingGroup 중심 데이터 설계, 보안 우선, 테스트 가능한 코드

---

## 1. Core Framework & Environment

### Django & Python
- **Python 3.10+** 문법에 능숙 (타입 힌트, f-string, walrus operator, match-case 등)
- **Django 최신 버전** 기능 숙지 (비동기 뷰, `async def`, StreamingHttpResponse 등)
- `settings.py` 핵심 설정 (INSTALLED_APPS, MIDDLEWARE, AUTH, STATIC, MEDIA, ALLAUTH 등) 완벽 이해

### 프로젝트 구조
- **앱 구성**: `accounts`, `core`, `vendors`, `weddings`, `reviews`
- **의존성**: `requirements.txt` 관리 (`django-allauth`, `widget_tweaks`, `humanize` 등)
- **환경 분리**: `.env` 기반 시크릿 관리, DEBUG 모드 분기

---

## 2. Django Template Language (DTL) — 필수 숙지

> 개발부장은 뷰에서 전달하는 context 변수와 템플릿 문법의 연결을 정확히 이해해야 합니다.

### 2.1 템플릿 상속 구조
```django
{# base.html — 최상위 레이아웃 #}
{% load static %}
{% load humanize %}

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

```django
{# 자식 템플릿 #}
{% extends "base.html" %}
{% block content %}
    <h1>{{ page_title }}</h1>
{% endblock %}
```

### 2.2 핵심 태그 & 필터
| 태그/필터 | 용도 | 예시 |
|----------|------|------|
| `{% block name %}` | 템플릿 상속 블록 정의 | `{% block content %}{% endblock %}` |
| `{% include "path" %}` | 부분 템플릿 포함 | `{% include "weddings/includes/_tabs.html" %}` |
| `{% url 'name' %}` | URL 역참조 | `{% url 'weddings:dashboard' %}` |
| `{% static 'path' %}` | 정적 파일 경로 | `{% static 'images/logo.png' %}` |
| `{% csrf_token %}` | CSRF 보호 토큰 | 모든 POST `<form>`에 필수 |
| `{% if %} / {% elif %} / {% else %}` | 조건 분기 | `{% if user.is_authenticated %}` |
| `{% for item in list %}` | 반복문 | `{% for task in tasks %}` |
| `{% empty %}` | for문 결과 없을 때 | `{% empty %}<p>데이터 없음</p>` |
| `{% with var=value %}` | 변수 할당 | `{% with total=tasks.count %}` |
| `{{ value\|intcomma }}` | 숫자 콤마 포맷 | `{{ budget\|intcomma }}` → `1,500,000` |
| `{{ value\|date:"Y-m-d" }}` | 날짜 포맷 | `{{ wedding_date\|date:"Y년 m월 d일" }}` |
| `{{ value\|default:"없음" }}` | 기본값 | `{{ memo\|default:"메모 없음" }}` |
| `{{ value\|truncatewords:10 }}` | 글자 수 제한 | 본문 미리보기 등 |
| `{{ value\|linebreaksbr }}` | 줄바꿈 → `<br>` 변환 | 메모 표시 |

### 2.3 Context 변수 전달 패턴
```python
# views.py
def dashboard(request):
    context = {
        'tasks': ScheduleTask.objects.filter(group=group),
        'total_budget': tasks.aggregate(Sum('estimated_budget')),
        'wedding_date': profile.wedding_date,
        'd_day': (profile.wedding_date - date.today()).days,
    }
    return render(request, 'weddings/dashboard.html', context)
```
- 뷰에서 전달한 키 이름(예: `tasks`)이 템플릿에서 `{{ tasks }}`로 사용됨을 항상 인지
- 새 context 변수 추가 시 → 디자인부장에게 해당 변수의 타입과 구조를 반드시 안내

---

## 3. Wedding Business Logic

### WeddingGroup 중심 아키텍처
```
User ──1:1──▶ WeddingProfile ──FK──▶ WeddingGroup
                                        │
                        ┌───────────────┼───────────────┐
                        ▼               ▼               ▼
                  ScheduleTask    ScheduleMemo    CommunityPost
```

### 핵심 모델 필드
- **WeddingGroup**: 커플 단위의 최상위 그룹 (모든 데이터의 FK 참조 대상)
- **WeddingProfile**: `wedding_date`, `name`, `role` → User와 1:1
- **ScheduleTask**: `title`, `d_day_offset`, `estimated_budget`, `is_completed`, `memo`
- **ScheduleMemo**: 날짜별 메모 저장

### D-Day 로직
```python
# D-Day 계산
d_day = (wedding_profile.wedding_date - date.today()).days

# D-Day 기반 태스크 시기 표시
task_date = wedding_date - timedelta(days=task.d_day_offset)
# 예: d_day_offset=90 → 결혼 90일 전
```

### Signal 기반 자동화
- `weddings.signals`: 프로필 생성 시 기본 체크리스트 태스크 자동 생성
- 새 Signal 추가 시 `apps.py`의 `ready()` 메서드에 등록 필수

---

## 4. Database & ORM

### 마이그레이션 워크플로우
```bash
# 1. 모델 변경 후 마이그레이션 파일 생성
python manage.py makemigrations

# 2. 마이그레이션 적용
python manage.py migrate

# 3. (선택) 특정 앱만 마이그레이션
python manage.py makemigrations weddings
python manage.py migrate weddings
```

### 관계형 모델 패턴
| 관계 | 사용 사례 | Django 필드 |
|------|----------|------------|
| OneToOne | User ↔ WeddingProfile | `OneToOneField(User)` |
| ForeignKey | Task → WeddingGroup | `ForeignKey(WeddingGroup, on_delete=CASCADE)` |
| ManyToMany | Post ↔ Recommendations | `ManyToManyField(User, related_name='recommended_posts')` |

### QuerySet 최적화
```python
# ❌ N+1 문제 발생
for task in ScheduleTask.objects.all():
    print(task.group.name)  # 매번 쿼리 발생

# ✅ select_related로 JOIN
tasks = ScheduleTask.objects.select_related('group').all()

# ✅ 집계 함수 활용
from django.db.models import Sum, Count
total = tasks.aggregate(total_budget=Sum('estimated_budget'))

# ✅ prefetch_related (M2M 관계)
posts = CommunityPost.objects.prefetch_related('recommendations').all()
```

---

## 5. Authentication & Social Login

### django-allauth 설정
```python
# settings.py 핵심 설정
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'naver': {
        'APP': {
            'client_id': '<NAVER_CLIENT_ID>',
            'secret': '<NAVER_CLIENT_SECRET>',
        }
    },
    'google': {
        'APP': {
            'client_id': '<GOOGLE_CLIENT_ID>',
            'secret': '<GOOGLE_CLIENT_SECRET>',
        },
        'SCOPE': ['profile', 'email'],
    }
}
```

### OAuth 2.0 플로우 이해
```
[사용자] → 로그인 버튼 클릭
    → [Naver/Google 인증 서버] 로 리다이렉트
    → 사용자 동의 후 Callback URL로 코드 반환
    → [Django allauth] 가 코드 → 토큰 교환
    → SocialAccount 모델에 저장 → 로그인 완료
```

### CustomLoginView
- `accounts/views.py`에서 allauth LoginView를 오버라이드
- 추가 context (배경 이미지, 브랜드 정보 등) 제공
- 로그인 후 리다이렉트 경로 커스터마이징

---

## 6. External API Integration — Naver & Google

### 6.1 Naver API
> Naver Developers (https://developers.naver.com) 에서 애플리케이션 등록 후 사용

| API | 용도 (Weple) | 인증 방식 |
|-----|-------------|----------|
| **Naver Login** | 소셜 로그인 | OAuth 2.0 (allauth 처리) |
| **Naver Search API** | 웨딩 업체 검색 (블로그/지역 검색) | Client ID + Secret (Header) |
| **Naver Map API** | 업체 위치 표시, 예식장 지도 | Client ID (JS 방식) |

#### Naver Search API 호출 패턴
```python
import requests

def search_naver(query, display=10):
    """네이버 검색 API 호출"""
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {
        "query": query,
        "display": display,
        "sort": "comment",  # 정확도순: sim, 리뷰순: comment
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["items"]
```

#### Naver Map (JavaScript)
```html
<script src="https://oapi.map.naver.com/openapi/v3/maps.js?ncpClientId=YOUR_ID"></script>
<script>
    var map = new naver.maps.Map('map', {
        center: new naver.maps.LatLng(37.5665, 126.978),
        zoom: 15
    });
    new naver.maps.Marker({ position: center, map: map });
</script>
```

### 6.2 Google API
> Google Cloud Console (https://console.cloud.google.com) 에서 프로젝트 생성 후 사용

| API | 용도 (Weple) | 인증 방식 |
|-----|-------------|----------|
| **Google OAuth 2.0** | 소셜 로그인 | OAuth 2.0 (allauth 처리) |
| **Google Calendar API** | 웨딩 일정 동기화 | OAuth 2.0 + Service Account |
| **Google Maps API** | 업체 위치, 예식장 검색 | API Key (JS 방식) |
| **Google Places API** | 장소 검색, 리뷰 | API Key |

#### Google Calendar API 연동 예시
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def sync_to_google_calendar(user, task):
    """체크리스트 태스크를 Google Calendar에 동기화"""
    creds = Credentials.from_authorized_user_info(user.google_token)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': task.title,
        'start': {'date': str(task.target_date)},
        'end': {'date': str(task.target_date)},
        'description': task.memo or '',
    }
    service.events().insert(calendarId='primary', body=event).execute()
```

#### Google Maps (JavaScript)
```html
<script src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY"></script>
<script>
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 37.5665, lng: 126.978 },
        zoom: 15,
    });
    new google.maps.Marker({ position: { lat: 37.5665, lng: 126.978 }, map });
</script>
```

### 6.3 API 통신 공통 패턴
```python
import requests
from django.conf import settings

class APIClient:
    """외부 API 호출 공통 클래스"""

    @staticmethod
    def get(url, headers=None, params=None, timeout=10):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("API 요청 시간 초과")
        except requests.exceptions.HTTPError as e:
            raise Exception(f"API 오류: {e.response.status_code}")

    @staticmethod
    def post(url, headers=None, data=None, json=None, timeout=10):
        try:
            response = requests.post(url, headers=headers, data=data, json=json, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 요청 실패: {str(e)}")
```

---

## 7. Security & Performance

### 보안 필수 사항
| 항목 | 구현 방법 |
|------|----------|
| **CSRF 보호** | 모든 POST 폼에 `{% csrf_token %}`, AJAX에 `X-CSRFToken` 헤더 |
| **XSS 방지** | Django 템플릿은 기본 auto-escape, 필요 시 `{{ value\|escape }}` |
| **SQL Injection 방지** | ORM 사용 권장, `raw()` 사용 시 파라미터 바인딩 필수 |
| **인증 확인** | `@login_required` 데코레이터, `WeddingGroup` 소유권 검증 |
| **시크릿 관리** | API 키, DB 비밀번호는 `.env` 파일로 관리, `settings.py`에 하드코딩 금지 |

### AJAX CSRF 토큰 전송 패턴
```javascript
// Cookie에서 CSRF 토큰 추출
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fetch API 사용 시
fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
});
```

### 성능 최적화
- **QuerySet 최적화**: `select_related()`, `prefetch_related()` 적극 활용
- **Pagination**: 목록 뷰에 `Paginator` 적용 (커뮤니티, 검색 결과 등)
- **캐싱**: `django.core.cache` — 자주 변경되지 않는 데이터 (업체 카테고리 등)
- **Static 파일**: `{% static %}` 태그 사용, `collectstatic` 후 CDN 또는 Nginx 서빙

---

## 8. Testing & Debugging

### Django 테스트 기본 구조
```python
from django.test import TestCase, Client
from django.urls import reverse

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        # WeddingProfile, WeddingGroup 설정...

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('weddings:dashboard'))
        self.assertEqual(response.status_code, 302)  # 로그인 리다이렉트

    def test_dashboard_loads(self):
        self.client.login(username='test', password='pass')
        response = self.client.get(reverse('weddings:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'D-Day')
```

### API 모킹
```python
from unittest.mock import patch

class NaverSearchTest(TestCase):
    @patch('vendors.utils.requests.get')
    def test_search_returns_results(self, mock_get):
        mock_get.return_value.json.return_value = {"items": [{"title": "예식장A"}]}
        mock_get.return_value.raise_for_status = lambda: None
        results = search_naver("강남 예식장")
        self.assertEqual(len(results), 1)
```

### 디버깅 도구
```python
# Django Debug Toolbar (개발 환경)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# 로깅 설정
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',  # SQL 쿼리 로그 출력
            'handlers': ['console'],
        },
    },
}
```
