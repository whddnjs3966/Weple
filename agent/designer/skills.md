# Design Specialist Agent Skills — Weple Project

> **역할**: UI/UX 전문가 & 인터랙티브 반응형 웹 디자이너
> **핵심 기술**: HTML · CSS · Vanilla JS · Django Template Language
> **원칙**: 모바일 퍼스트, 일관된 브랜드 아이덴티티, 접근성 우선

---

## 1. Visual Identity & Brand System

### 컬러 팔레트
```css
:root {
    /* Primary */
    --primary-color: #FF8E8E;        /* Soft Coral — 메인 포인트 */
    --primary-light: #FFB5B5;        /* 호버, 배경 하이라이트 */
    --primary-dark: #E67373;         /* 활성 상태, 강조 */

    /* Neutral */
    --bg-white: #FFFFFF;             /* 메인 배경 */
    --bg-light: #F8F9FA;            /* 섹션 배경, 카드 외부 */
    --bg-card: rgba(255, 255, 255, 0.85); /* 글래스모피즘 카드 */
    --text-primary: #2D2D2D;        /* 본문 텍스트 */
    --text-secondary: #6C757D;      /* 보조 텍스트, 라벨 */
    --border-color: #E9ECEF;        /* 구분선, 테두리 */

    /* Semantic */
    --success: #28A745;              /* 완료, 성공 */
    --warning: #FFC107;              /* 주의, 진행중 */
    --danger: #DC3545;               /* 삭제, 오류 */
    --info: #17A2B8;                /* 정보, 링크 */
}
```

### 타이포그래피 시스템
```css
/* 폰트 로드 */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

body {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-primary);
}

/* 타이포그래피 스케일 */
h1 { font-size: 2rem; font-weight: 700; }      /* 페이지 제목 */
h2 { font-size: 1.5rem; font-weight: 600; }    /* 섹션 제목 */
h3 { font-size: 1.25rem; font-weight: 600; }   /* 카드 제목 */
body { font-size: 1rem; font-weight: 400; }     /* 본문 */
small { font-size: 0.875rem; font-weight: 400; } /* 부가 정보 */
```

### 아이콘 & 이미지 가이드
- 아이콘: **이모지 기반** (💍, 📋, 📅, 💰 등) 또는 SVG 인라인 아이콘
- 이미지: `{% static 'images/...' %}` 경로 사용, WebP 포맷 권장
- 대시보드 카드 이미지: 가로 세로 비율 16:9 또는 4:3 유지

---

## 2. Django Template Language (DTL) — 필수 숙지

> 디자인부장은 Django 템플릿 문법을 정확히 이해하여 올바른 HTML을 작성해야 합니다.

### 2.1 템플릿 상속 (`{% extends %}` / `{% block %}`)
```django
{# base.html — 전체 레이아웃 골격 #}
{% load static %}
{% load humanize %}

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>{% include "includes/_header.html" %}</header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>{% include "includes/_footer.html" %}</footer>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

```django
{# dashboard.html — base.html을 상속 #}
{% extends "base.html" %}
{% load static %}
{% load humanize %}

{% block extra_css %}
<style>
    .dashboard__card { /* 대시보드 전용 스타일 */ }
</style>
{% endblock %}

{% block content %}
    <h1>대시보드</h1>
    <p>D-{{ d_day }}</p>
{% endblock %}
```

### 2.2 핵심 태그 정리
| 태그 | 용도 | 사용 예시 |
|------|------|----------|
| `{% extends "base.html" %}` | 부모 템플릿 상속 (파일 최상단에 위치) | `{% extends "base.html" %}` |
| `{% block name %}...{% endblock %}` | 상속 블록 정의/재정의 | `{% block content %}...{% endblock %}` |
| `{% include "path.html" %}` | 부분 템플릿 삽입 | `{% include "weddings/includes/_tabs.html" %}` |
| `{% load static %}` | static 태그 사용 선언 | 템플릿 상단 (extends 바로 아래) |
| `{% load humanize %}` | 숫자/날짜 포맷 필터 사용 선언 | intcomma, naturaltime 등 사용 시 |
| `{% static 'path' %}` | 정적 파일 URL 생성 | `<img src="{% static 'images/logo.png' %}">` |
| `{% url 'app:viewname' %}` | URL 역참조 | `<a href="{% url 'weddings:dashboard' %}">` |
| `{% csrf_token %}` | CSRF 보호 토큰 (POST 필수) | `<form method="post">{% csrf_token %}` |
| `{% if %}{% elif %}{% else %}{% endif %}` | 조건부 렌더링 | `{% if tasks %}...{% else %}없음{% endif %}` |
| `{% for item in list %}{% endfor %}` | 반복 렌더링 | `{% for task in tasks %}...{% endfor %}` |
| `{% empty %}` | for 결과가 없을 때 | `{% for p in posts %}...{% empty %}게시글 없음{% endfor %}` |
| `{% with var=expr %}{% endwith %}` | 임시 변수 선언 | `{% with total=budget\|intcomma %}` |

### 2.3 핵심 필터 정리
| 필터 | 용도 | 사용 예시 |
|------|------|----------|
| `{{ val\|intcomma }}` | 숫자에 콤마 | `{{ 1500000\|intcomma }}` → `1,500,000` |
| `{{ val\|date:"Y-m-d" }}` | 날짜 포맷 지정 | `{{ wedding_date\|date:"Y년 m월 d일" }}` |
| `{{ val\|default:"기본값" }}` | 값 없을 때 대체 | `{{ memo\|default:"메모 없음" }}` |
| `{{ val\|linebreaksbr }}` | 줄바꿈 → `<br>` | 메모, 본문 표시 |
| `{{ val\|truncatewords:N }}` | N단어로 자르기 | 목록 미리보기 |
| `{{ val\|length }}` | 리스트 길이 | `{{ tasks\|length }}개` |
| `{{ val\|add:N }}` | 숫자 덧셈 | `{{ forloop.counter\|add:offset }}` |
| `{{ val\|yesno:"Y,N,?" }}` | Boolean 텍스트 변환 | `{{ is_done\|yesno:"완료,미완료" }}` |

### 2.4 forloop 내장 변수
```django
{% for task in tasks %}
    {{ forloop.counter }}       {# 1부터 시작하는 번호 #}
    {{ forloop.counter0 }}      {# 0부터 시작하는 번호 #}
    {{ forloop.first }}         {# 첫 번째 반복이면 True #}
    {{ forloop.last }}          {# 마지막 반복이면 True #}
{% endfor %}
```

### 2.5 디자인 관련 주의사항
- `{% load static %}`과 `{% load humanize %}`는 **각 템플릿 파일마다** 선언해야 함
- `{% extends %}`는 반드시 **파일의 첫 줄**에 위치
- `{% include %}`로 불러오는 파일에서도 필요한 `{% load %}` 선언 필요
- `{{ variable }}` 안의 변수명은 개발부장이 `views.py`에서 전달하는 context 키와 동일해야 함

---

## 3. Responsive Web Design — 반응형 웹

### 모바일 퍼스트 전략
```css
/* 모바일 기본 (320px~) */
.dashboard__grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1rem;
}

/* 태블릿 (768px~) */
@media (min-width: 768px) {
    .dashboard__grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        padding: 1.5rem;
    }
}

/* 데스크톱 (1024px~) */
@media (min-width: 1024px) {
    .dashboard__grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        padding: 2rem;
    }
}

/* 와이드 (1440px~) */
@media (min-width: 1440px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
    }
}
```

### 브레이크포인트 체계
| 이름 | 너비 | 대상 기기 |
|------|------|----------|
| `xs` | 0 ~ 575px | 스마트폰 세로 |
| `sm` | 576 ~ 767px | 스마트폰 가로 |
| `md` | 768 ~ 1023px | 태블릿 |
| `lg` | 1024 ~ 1439px | 데스크톱 |
| `xl` | 1440px~ | 와이드 모니터 |

### 뷰포트 필수 설정
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 반응형 유틸리티 패턴
```css
/* 터치 영역 확보 (모바일 버튼) */
.btn--touch {
    min-height: 44px;
    min-width: 44px;
    padding: 0.75rem 1.5rem;
}

/* 숨김/표시 유틸리티 */
.hide-mobile { display: none; }
@media (min-width: 768px) {
    .hide-mobile { display: block; }
    .hide-desktop { display: none; }
}
```

---

## 4. Interactive UI/UX — 인터랙티브 디자인

### 4.1 CSS Transitions & Animations
```css
/* 부드러운 호버 트랜지션 */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* 페이드인 애니메이션 */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.fade-in {
    animation: fadeInUp 0.5s ease forwards;
}

/* 순차적 등장 (staggered animation) */
.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
```

### 4.2 마이크로 인터랙션
```css
/* 체크박스 완료 애니메이션 */
.task-checkbox:checked + .task-label {
    text-decoration: line-through;
    color: var(--text-secondary);
    transition: all 0.3s ease;
}

/* 버튼 클릭 피드백 */
.btn:active {
    transform: scale(0.96);
    transition: transform 0.1s ease;
}

/* 토글 스위치 */
.toggle {
    width: 48px;
    height: 24px;
    background: var(--border-color);
    border-radius: 12px;
    transition: background 0.3s ease;
    cursor: pointer;
}
.toggle.active {
    background: var(--primary-color);
}
.toggle::after {
    content: '';
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: white;
    transition: transform 0.3s ease;
}
.toggle.active::after {
    transform: translateX(24px);
}

/* 로딩 스피너 */
@keyframes spin {
    to { transform: rotate(360deg); }
}
.spinner {
    width: 24px;
    height: 24px;
    border: 3px solid var(--border-color);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}
```

### 4.3 모달/토스트/탭 패턴
```css
/* 모달 오버레이 */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
}
.modal-overlay.active {
    opacity: 1;
    visibility: visible;
}

/* 모달 컨텐츠 */
.modal-content {
    background: white;
    border-radius: 16px;
    padding: 2rem;
    max-width: 500px;
    width: 90%;
    transform: translateY(20px);
    transition: transform 0.3s ease;
}
.modal-overlay.active .modal-content {
    transform: translateY(0);
}

/* 토스트 알림 */
.toast {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: var(--text-primary);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.4s ease;
    z-index: 2000;
}
.toast.show {
    transform: translateY(0);
    opacity: 1;
}

/* 탭 전환 */
.tab-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    border-bottom: 3px solid transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}
.tab-btn--active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
    font-weight: 600;
}
```

---

## 5. CSS Architecture — CSS 설계

### BEM 네이밍 컨벤션
```css
/* Block: 독립적인 UI 컴포넌트 */
.dashboard { }

/* Element: Block의 하위 요소 (__) */
.dashboard__card { }
.dashboard__title { }
.dashboard__grid { }

/* Modifier: 상태/변형 (--) */
.dashboard__card--highlighted { }
.tab-btn--active { }
.task--completed { }
```

### Glassmorphism 패턴
```css
.glass-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    padding: 1.5rem;
}

.glass-card:hover {
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}
```

### CSS 변수 활용 원칙
- **새 색상 추가 금지**: 반드시 `:root`에 정의된 CSS 변수를 사용
- **하드코딩 금지**: `color: #FF8E8E` ❌ → `color: var(--primary-color)` ✅
- **일관성**: 여백, 둥근 모서리, 그림자도 가능하면 변수화
```css
:root {
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 15px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 25px rgba(0, 0, 0, 0.15);
}
```

---

## 6. Component Design — 주요 컴포넌트

### 6.1 대시보드 D-Day 배너
```html
<div class="dday-banner glass-card">
    <div class="dday-banner__emoji">💍</div>
    <div class="dday-banner__count">D-{{ d_day }}</div>
    <div class="dday-banner__date">{{ wedding_date|date:"Y년 m월 d일" }}</div>
</div>
```

### 6.2 체크리스트 테이블
```html
<table class="checklist-table">
    <thead>
        <tr>
            <th>선택</th>
            <th>시기 (D-Day)</th>
            <th>할 일 (Task)</th>
            <th>예상 예산</th>
            <th>상태 (Status)</th>
        </tr>
    </thead>
    <tbody>
        {% for task in tasks %}
        <tr class="checklist-table__row {% if task.is_completed %}task--completed{% endif %}">
            <td><input type="checkbox" name="task_ids" value="{{ task.id }}"></td>
            <td>D-{{ task.d_day_offset }}</td>
            <td>{{ task.title }}</td>
            <td>{{ task.estimated_budget|intcomma }}원</td>
            <td>
                <span class="status-badge {% if task.is_completed %}status-badge--done{% endif %}">
                    {{ task.is_completed|yesno:"완료,미완료" }}
                </span>
            </td>
        </tr>
        {% empty %}
        <tr><td colspan="5">등록된 체크리스트가 없어요.</td></tr>
        {% endfor %}
    </tbody>
</table>
```

### 6.3 캘린더
```css
.calendar {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 2px;
}
.calendar__day {
    aspect-ratio: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background 0.2s ease;
}
.calendar__day--today {
    background: var(--primary-light);
    font-weight: 700;
}
.calendar__day--selected {
    background: var(--info);
    color: white;
}
.calendar__day--wedding {
    background: var(--primary-color);
    color: white;
}
```

### 6.4 커뮤니티 게시판
```html
<div class="community">
    <div class="community__tabs">
        <button class="tab-btn tab-btn--active" data-tab="free">자유게시판</button>
        <button class="tab-btn" data-tab="notice">공지사항</button>
    </div>
    <div class="community__search">
        <input type="text" placeholder="제목, 작성자, 본문내용" class="search-input">
        <button class="btn btn--primary">검색</button>
    </div>
    <div class="community__list">
        {% for post in posts %}
        <div class="post-card glass-card fade-in">
            <h3 class="post-card__title">{{ post.title }}</h3>
            <p class="post-card__meta">{{ post.author }} · {{ post.created_at|date:"m/d" }}</p>
            <p class="post-card__preview">{{ post.content|truncatewords:20 }}</p>
        </div>
        {% endfor %}
    </div>
</div>
```

---

## 7. Frontend JavaScript — 프론트엔드 인터랙션

### 7.1 Vanilla JS 이벤트 위임
```javascript
// 이벤트 위임 패턴 (동적 요소에도 작동)
document.querySelector('.checklist-table').addEventListener('click', function(e) {
    const row = e.target.closest('.checklist-table__row');
    if (!row) return;

    if (e.target.type === 'checkbox') {
        handleTaskToggle(row, e.target.checked);
    }
});
```

### 7.2 Fetch API를 활용한 AJAX
```javascript
// CSRF 토큰 추출
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value
        || document.cookie.match(/csrftoken=([^;]+)/)?.[1];
}

// POST 요청 예시 (체크리스트 상태 업데이트)
async function updateTaskStatus(taskId, isCompleted) {
    try {
        const response = await fetch(`/weddings/task/${taskId}/update/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ is_completed: isCompleted }),
        });
        if (!response.ok) throw new Error('업데이트 실패');

        // 성공 시 토스트 표시
        showToast('저장되었어요! ✅');
    } catch (error) {
        showToast('오류가 발생했어요. 다시 시도해주세요.', 'error');
    }
}
```

### 7.3 탭 전환 로직
```javascript
// 탭 전환
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // 모든 탭 버튼 비활성화
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('tab-btn--active'));
        // 모든 탭 컨텐츠 숨기기
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('tab-content--active'));

        // 클릭된 탭 활성화
        btn.classList.add('tab-btn--active');
        const tabId = btn.dataset.tab;
        document.getElementById(`tab-${tabId}`).classList.add('tab-content--active');
    });
});
```

### 7.4 모달 제어
```javascript
function openModal(modalId) {
    const overlay = document.getElementById(modalId);
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // 배경 스크롤 방지
}

function closeModal(modalId) {
    const overlay = document.getElementById(modalId);
    overlay.classList.remove('active');
    document.body.style.overflow = '';
}

// 오버레이 클릭 시 닫기
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModal(overlay.id);
    });
});

// ESC 키로 닫기
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => closeModal(m.id));
    }
});
```

### 7.5 토스트 알림 함수
```javascript
function showToast(message, type = 'success', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    // 등장 애니메이션
    requestAnimationFrame(() => toast.classList.add('show'));

    // 자동 제거
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, duration);
}
```

---

## 8. Accessibility & Performance — 접근성 & 성능

### 시맨틱 HTML
```html
<!-- ✅ 올바른 예시 -->
<header>...</header>
<nav>...</nav>
<main>
    <section>
        <h2>체크리스트</h2>
        <article>...</article>
    </section>
</main>
<footer>...</footer>

<!-- ❌ 잘못된 예시 -->
<div class="header">...</div>
<div class="nav">...</div>
<div class="main">...</div>
```

### WAI-ARIA 가이드
```html
<!-- 탭 접근성 -->
<div role="tablist">
    <button role="tab" aria-selected="true" aria-controls="panel-1">일정관리</button>
    <button role="tab" aria-selected="false" aria-controls="panel-2">체크리스트</button>
</div>
<div role="tabpanel" id="panel-1">...</div>

<!-- 모달 접근성 -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <h2 id="modal-title">할 일 추가</h2>
    ...
</div>

<!-- 아이콘 버튼 접근성 -->
<button aria-label="삭제">🗑️</button>
<button aria-label="메뉴 열기">☰</button>
```

### 이미지 최적화
```html
<!-- Lazy Loading -->
<img src="{% static 'images/venue.webp' %}"
     alt="예식장 이미지"
     loading="lazy"
     decoding="async"
     width="400"
     height="300">

<!-- 반응형 이미지 -->
<picture>
    <source media="(max-width: 768px)" srcset="{% static 'images/hero-mobile.webp' %}">
    <source media="(min-width: 769px)" srcset="{% static 'images/hero-desktop.webp' %}">
    <img src="{% static 'images/hero-desktop.webp' %}" alt="웨플 메인 이미지">
</picture>
```

### CSS 성능 최적화
```css
/* GPU 가속 활용 (transform, opacity만 애니메이션) */
/* ✅ Good — GPU 가속 */
.card { transition: transform 0.3s ease, opacity 0.3s ease; }

/* ❌ Bad — 레이아웃 재계산 유발 */
.card { transition: width 0.3s ease, height 0.3s ease; }

/* will-change로 힌트 제공 (사용 후 해제 권장) */
.card:hover { will-change: transform; }
```

### 폼 접근성
```html
<form method="post" action="{% url 'weddings:add_task' %}">
    {% csrf_token %}
    <div class="form-group">
        <label for="task-title">할 일</label>
        <input type="text" id="task-title" name="title"
               required
               placeholder="예: 예식장 투어"
               aria-describedby="task-title-help">
        <small id="task-title-help">체크리스트에 추가할 항목을 입력하세요.</small>
    </div>
    <button type="submit" class="btn btn--primary">추가</button>
</form>
```
