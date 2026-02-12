# Design Specialist Agent Skills — Weple Project

> **역할**: UI/UX 전문가 & 인터랙티브 웹 디자이너 (Web-First)
> **핵심 기술**: HTML · CSS · Vanilla JS · Django Template Language
> **원칙**: **웹(Desktop) 우선**, 심미적인 웨딩 무드(Glass, Floral), **DTL 태그 내 띄어쓰기 금지**

---

## 1. Visual Identity & Brand System

### 1.1 Design Concept: "Romantic Glass & Dreamy Flow"
- **Keywords**: Elegant, Airy, Glass, Floral, Sparkle (반지, 보석)
- **Background**: 단순 단색이 아닌, 은은한 그라디언트와 `floating blobs` 애니메이션 활용
- **Object**: 유리 질감(Glassmorphism), 꽃잎, 웨딩 반지, 드레스 텍스처 등을 배경이나 장식 요소로 적극 활용

### 1.2 컬러 팔레트 (Soft Coral & Pure White)
```css
:root {
    /* Primary (Romantic Coral) */
    --primary-color: #FF8E8E;        /* 메인 포인트 (사랑스러운 코랄) */
    --primary-light: #FFB5B5;        /* 호버, 부드러운 배경 */
    --primary-dark: #E67373;         /* 텍스트 강조 */

    /* Glass & Background */
    --bg-white: #FFFFFF;             /* 기본 배경 */
    --bg-glass: rgba(255, 255, 255, 0.75); /* 블러 처리된 유리 카드 */
    --bg-glass-border: rgba(255, 255, 255, 0.4); /* 유리 테두리 */
    
    /* Text */
    --text-primary: #2D2D2D;         /* 본문 (Too dark하지 않게) */
    --text-secondary: #6C757D;       /* 서브 텍스트 */
    
    /* Semantic */
    --success: #28A745;
    --danger: #DC3545;
}
```

### 1.3 타이포그래피 & 에셋
- **Font**: 'Pretendard' (웹 가독성 최우선)
- **Images**: 고해상도 웨딩 이미지 (Unsplash, Pexels 등) 활용. `object-fit: cover` 필수.
- **Icons**: 단순 이모지보다 **Bootstrap Icons (`bi-`)** 또는 **SVG** 활용 권장. (고급스러움 유지)

---

## 2. Django Template Language (DTL) — **NO SPACES Rule**

> **🚨 CRITICAL RULE**: HTML 가독성과 IDE 호환성을 위해 **DTL 태그 내부에 띄어쓰기를 절대 사용하지 않습니다.**
> - `{{ value }}` (X) → `{{value}}` (O)
> - `{% if user %}` (X) → `{%if user%}` (O)
> - `{% load static %}` (X) → `{%load static%}` (O)

### 2.1 템플릿 상속 (`{%extends%}` / `{%block%}`)
```django
{#base.html — 전체 레이아웃 골격#}
{%load static%}
{%load humanize%}

<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="{%static 'css/style.css'%}">
    {%block extra_css%}{%endblock%}
</head>
<body>
    <header>{%include "includes/_header.html"%}</header>
    <main>
        {%block content%}{%endblock%}
    </main>
    <footer>{%include "includes/_footer.html"%}</footer >
    {%block extra_js%}{%endblock%}
</body>
</html>
```

### 2.2 핵심 태그 정리 (No-Space 규칙 준수)
| 태그 | 올바른 사용법 (No Spaces) |
|------|----------|
| `{%extends%}` | `{%extends "base.html"%}` |
| `{%block%}` | `{%block content%}`...`{%endblock%}` |
| `{%include%}` | `{%include "path.html"%}` |
| `{%load%}` | `{%load static%}` |
| `{%static%}` | `<img src="{%static 'img/logo.png'%}">` |
| `{%url%}` | `<a href="{%url 'weddings:dashboard'%}">` |
| `{%csrf_token%}` | `{%csrf_token%}` |
| `{%if%}` | `{%if user.is_authenticated%}` |
| `{%for%}` | `{%for task in tasks%}` |
| `{%empty%}` | `{%empty%}` |
| `{%with%}` | `{%with total=tasks.count%}` |

### 2.3 필터 사용 예시 (No Spaces)
- `{{val|intcomma}}`
- `{{date|date:"Y-m-d"}}`
- `{{memo|default:"없음"}}`
- `{{content|linebreaksbr}}`
- `{{list|length}}`
- `{{value|yesno:"Y,N"}}`

### 2.4 주의사항
- **자동 포맷팅 주의**: IDE의 Prettier 등이 자동으로 `{{ value }}`로 바꾸지 않도록 설정 확인.
- 항상 코드를 작성한 후 태그 내 공백이 없는지 재검토.

---

## 3. Responsive Web Design — **Web First Strategy**

### 3.1 Web-First (Desktop Priority)
- **Rich Experience**: 데스크톱에서는 **넓은 화면을 활용한 2-3단 레이아웃**, 고해상도 이미지, 호버 효과를 적극 제공.
- **Graceful Degradation**: 모바일에서는 레이아웃을 단순히 1단으로 쌓되(Stack), 핵심 기능은 유지.
- **Container Width**: `max-width: 1200px` (or 1440px) 중앙 정렬을 기본으로 함.

### 3.2 브레이크포인트 (Desktop Focus)
| 기기 | 너비 | 레이아웃 전략 |
|---|---|---|
| **Desktop (Default)** | **1024px ~** | **3-Column Grid, Sidebar, Full Parallax** |
| Tablet | 768px ~ 1023px | 2-Column Grid, Condensed Sidebar |
| Mobile | ~ 767px | 1-Column Stack, Bottom Sheet, Hidden Hover |

### 3.3 반응형 유틸리티
```css
/* 데스크톱 전용 (Web First) */
.desktop-only { display: block; }
.mobile-only { display: none; }

@media (max-width: 768px) {
    .desktop-only { display: none; }
    .mobile-only { display: block; }
}
```

---

## 4. Interactive UI/UX — **Modern Wedding Trends**

### 4.1 Scroll & Reveal Animations (스크롤 인터랙션)
> 사용자가 스크롤할 때 콘텐츠가 부드럽게 떠오르거나(Fade Up), 이미지가 서서히 선명해지는 효과 필수.
```css
/* Scroll Reveal Class */
.reveal-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.reveal-on-scroll.visible {
    opacity: 1;
    transform: translateY(0);
}
```

### 4.2 Glassmorphism & Hover Effects (고급스러움)
```css
/* Premium Glass Card */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--bg-glass-border);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
    border-radius: 20px;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.glass-card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 12px 40px rgba(255, 142, 142, 0.2); /* Soft Pink Glow */
}
```

### 4.3 Parallax & Floating Elements (신비로운 분위기)
- **Parallax**: 배경 이미지가 스크롤 속도보다 느리게 움직여 깊이감(Depth) 부여.
- **Floating Blobs**: 배경에 은은하게 움직이는 핑크/보라 빛의 원형 그라디언트 배치.
```css
@keyframes float {
    0% { transform: translate(0, 0); }
    50% { transform: translate(15px, -15px); }
    100% { transform: translate(0, 0); }
}
.floating-obj { animation: float 6s ease-in-out infinite; }
```

### 4.4 Micro-Interactions
- **Heart Click**: 하트 클릭 시 파티클이 터지는 애니메이션.
- **Button Hover**: 그라디언트가 흐르거나(Shine effect), 크기가 살짝 커지는 효과.

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
