# Weple Development Workflow

> 개발부장(Developer)과 디자인부장(Designer)이 효율적으로 협업하기 위한 워크플로우 문서입니다.
> 각 에이전트는 반드시 자신의 `skills.md`를 숙지한 상태에서 이 워크플로우를 따르십시오.

---

## 1. Feature Request Analysis — 요구사항 분석

### 1.1 공통 분석
| 분석 항목 | 확인 내용 |
|----------|----------|
| **영향 범위** | 어떤 앱에 해당하는가? (`weddings`, `vendors`, `accounts`, `core`, `reviews`) |
| **기능 유형** | 신규 기능 / 기존 기능 수정 / 버그 수정 / UI 개선 |
| **데이터 변경** | 새 모델/필드가 필요한가? 마이그레이션이 발생하는가? |
| **UI 변경** | 새 페이지/컴포넌트가 필요한가? 기존 레이아웃 수정인가? |
| **외부 API** | Naver/Google API 연동이 필요한가? |

### 1.2 역할별 초기 분석
- **개발부장**: 모델 변경 여부, URL 패턴, 뷰 로직 복잡도, API 연동 필요성 판단
- **디자인부장**: 영향받는 템플릿 파일, 필요한 CSS 컴포넌트, 반응형 고려사항, 인터랙션 패턴 판단

### 1.3 협업 판단 기준
```
요구사항 접수
    │
    ├── 백엔드만 변경? ──▶ 개발부장 단독 진행
    │
    ├── 프론트엔드만 변경? ──▶ 디자인부장 단독 진행
    │
    └── 둘 다 변경? ──▶ 아래 전체 워크플로우 따르기
```

---

## 2. Backend Development — 개발부장 담당

> 📌 참조: `agent/developer/skills.md`

### Phase 1: 데이터 레이어
```
Step 1. Model 정의/수정
        ├── models.py에 필드 추가 또는 새 모델 생성
        ├── 관계 설정 (FK, OneToOne, M2M)
        └── 기본값, null/blank, on_delete 정책 확인

Step 2. Migration 실행
        ├── python manage.py makemigrations [app_name]
        ├── python manage.py migrate
        └── 기존 데이터 영향 여부 확인 (data migration 필요 시 작성)
```

### Phase 2: 비즈니스 로직
```
Step 3. View 작성/수정
        ├── 함수 기반 뷰 (FBV) 또는 클래스 기반 뷰 (CBV)
        ├── WeddingGroup 소유권 검증 (모든 POST 요청)
        ├── context 딕셔너리에 템플릿에 필요한 변수 전달
        └── @login_required 데코레이터 적용

Step 4. URL 패턴 등록
        ├── app/urls.py에 path() 추가
        ├── name 파라미터 지정 (템플릿에서 {% url %} 사용)
        └── config/urls.py include() 확인
```

### Phase 3: API 연동 (필요 시)
```
Step 5. External API 통합
        ├── Naver API: 검색, 지도, 로그인
        ├── Google API: Calendar, Maps, OAuth
        ├── API 키 .env 관리 확인
        └── 에러 핸들링 & 타임아웃 설정
```

### ⚡ 디자인부장에게 전달할 정보 (Handoff)
개발부장은 Phase 2 완료 후 다음 정보를 디자인부장에게 **반드시** 전달해야 합니다:

| 전달 항목 | 설명 | 예시 |
|----------|------|------|
| **context 변수 목록** | 뷰에서 전달하는 모든 변수의 이름, 타입, 구조 | `tasks` (QuerySet), `d_day` (int), `total_budget` (dict) |
| **URL name** | 템플릿에서 사용할 URL 이름 | `weddings:dashboard`, `weddings:add_task` |
| **HTTP method** | 각 URL이 지원하는 메서드 | `GET` (조회), `POST` (생성/수정/삭제) |
| **POST 파라미터** | 폼에서 전송해야 할 필드명 | `title`, `d_day_offset`, `estimated_budget` |
| **응답 형식** | 일반 렌더 / 리다이렉트 / JSON 응답 | redirect → dashboard 또는 JsonResponse |

**전달 형식 예시:**
```
📋 개발부장 → 디자인부장 Handoff

[뷰] dashboard (GET)
- context:
  - tasks: QuerySet[ScheduleTask] — .title, .d_day_offset, .estimated_budget, .is_completed
  - d_day: int — 결혼까지 남은 일수
  - total_budget: dict — {'total_budget__sum': Decimal}
  - wedding_date: date
  - memos: QuerySet[ScheduleMemo] — .date, .content

[뷰] add_task (POST)
- 필요 파라미터: title(str), d_day_offset(int), estimated_budget(int), memo(str, optional)
- 성공 시: redirect → weddings:dashboard
- 실패 시: redirect → weddings:dashboard (에러 메시지 포함)

[URL names]
- weddings:dashboard
- weddings:add_task
- weddings:delete_tasks
- weddings:update_task_status
```

---

## 3. Frontend Development — 디자인부장 담당

> 📌 참조: `agent/designer/skills.md`

### Phase 4: 템플릿 설계
```
Step 6. HTML 구조 작성
        ├── {% extends "base.html" %} 상속 확인
        ├── {% load static %}, {% load humanize %} 선언
        ├── 시맨틱 HTML 사용 (header, nav, main, section, article, footer)
        └── BEM 네이밍 컨벤션 준수

Step 7. Context 변수 매핑
        ├── 개발부장이 전달한 context 변수를 템플릿에 정확히 매핑
        ├── {{ variable }} — 변수 출력
        ├── {% for item in list %} — 반복 렌더링
        ├── {% if condition %} — 조건부 표시
        └── {{ value|intcomma }}, {{ date|date:"Y-m-d" }} — 필터 적용
```

### Phase 5: 스타일링
```
Step 8. CSS 작성
        ├── 기존 CSS 변수(--primary-color 등) 재사용
        ├── glass-card, fade-in 등 기존 패턴 활용
        ├── 반응형 미디어 쿼리 (모바일 → 태블릿 → 데스크톱)
        └── 인터랙티브 요소 (hover, active, transition)
```

### Phase 6: 인터랙션
```
Step 9. JavaScript 구현
        ├── 탭 전환, 모달, 체크박스 등 인터랙션 로직
        ├── AJAX 요청 시 CSRF 토큰 포함 (getCsrfToken())
        ├── 이벤트 위임 패턴 사용 (동적 요소 대응)
        └── 토스트 알림으로 사용자 피드백 제공
```

### ⚡ 개발부장에게 요청할 정보 (Request)
디자인부장은 작업 중 다음이 필요하면 개발부장에게 **명확히** 요청해야 합니다:

| 요청 항목 | 상황 |
|----------|------|
| **새 context 변수** | 템플릿에 표시할 데이터가 뷰에서 전달되지 않을 때 |
| **새 URL endpoint** | AJAX 요청을 보낼 대상 URL이 없을 때 |
| **JSON 응답 뷰** | JS에서 데이터를 비동기로 받아야 할 때 |
| **데이터 구조 확인** | context 변수의 필드명, 타입을 정확히 알아야 할 때 |

---

## 4. Quality Assurance — 품질 검증

### 4.1 공통 체크리스트
- [ ] **WeddingGroup 소유권**: 모든 POST 요청에서 현재 유저의 그룹인지 검증
- [ ] **CSRF 보호**: 모든 `<form method="post">`에 `{% csrf_token %}`, AJAX에 `X-CSRFToken` 헤더
- [ ] **소셜 로그인**: Naver/Google 로그인 플로우가 정상 작동하는지 확인
- [ ] **숫자 포맷**: 예산, 금액에 `{{ value|intcomma }}` 적용
- [ ] **날짜 포맷**: `{{ date|date:"Y년 m월 d일" }}` 또는 프로젝트 통일 형식
- [ ] **빈 데이터 처리**: `{% empty %}`, `{{ value|default:"없음" }}` 사용

### 4.2 개발부장 검증 항목
- [ ] 마이그레이션 정상 실행 (`makemigrations` → `migrate`)
- [ ] 새 필드에 기본값 또는 `null=True` 설정
- [ ] `select_related()` / `prefetch_related()` 적용 (N+1 방지)
- [ ] API 키가 `.env`에 있고 `settings.py`에 하드코딩되지 않음
- [ ] 에러 핸들링: try-except, 404 처리, 사용자 친화적 에러 메시지
- [ ] `@login_required` 데코레이터 적용 확인

### 4.3 디자인부장 검증 항목
- [ ] `{% load static %}`, `{% load humanize %}` 선언 확인
- [ ] `{% extends "base.html" %}`가 파일 첫 줄에 위치
- [ ] 모바일(375px), 태블릿(768px), 데스크톱(1024px) 반응형 확인
- [ ] hover/active 상태 시각적 피드백 존재
- [ ] 시맨틱 HTML 태그 사용 (`<section>`, `<article>`, `<nav>` 등)
- [ ] ARIA 속성 적용 (모달: `role="dialog"`, 탭: `role="tab"`)
- [ ] CSS 하드코딩 색상 없음 (모두 `var(--변수)` 사용)
- [ ] 이미지 `loading="lazy"`, `alt` 속성 포함

---

## 5. Scenario Workflows — 시나리오별 워크플로우

### 시나리오 A: 새 기능 추가 (예: 업체 리뷰 기능)
```
1. [공통]    요구사항 분석 → 영향 범위 파악
2. [개발]    reviews/models.py에 Review 모델 추가
3. [개발]    makemigrations → migrate
4. [개발]    reviews/views.py에 CRUD 뷰 작성
5. [개발]    reviews/urls.py에 URL 등록
6. [개발]    ⚡ Handoff: context 변수 & URL 정보 전달
7. [디자인]  reviews/templates/ 에 리스트/상세 템플릿 작성
8. [디자인]  CSS 컴포넌트 추가 (glass-card 패턴 활용)
9. [디자인]  JS 인터랙션 구현 (별점 입력, AJAX 제출)
10. [공통]   QA 체크리스트 검증
```

### 시나리오 B: 기존 UI 수정 (예: 대시보드 레이아웃 변경)
```
1. [디자인]  요구사항 분석 → 영향받는 템플릿 파일 파악
2. [디자인]  HTML/CSS 수정 (기존 context 변수 활용)
3. [디자인]  추가 데이터 필요 시 → ⚡ 개발부장에게 Request
4. [개발]    필요한 context 변수 추가 (views.py 수정)
5. [개발]    ⚡ Handoff: 새 변수 정보 전달
6. [디자인]  새 변수 매핑 → 템플릿 완성
7. [공통]    QA 체크리스트 검증
```

### 시나리오 C: 외부 API 연동 (예: 네이버 지도 업체 검색)
```
1. [공통]    요구사항 분석 → 필요 API 확인
2. [개발]    .env에 API 키 등록
3. [개발]    utils.py에 API 호출 함수 작성 (에러 핸들링 포함)
4. [개발]    views.py에서 API 데이터를 context로 전달
5. [개발]    ⚡ Handoff: API 응답 데이터 구조 & context 변수 전달
6. [디자인]  API 데이터를 표시할 UI 컴포넌트 설계
7. [디자인]  네이버 Map JS SDK 연동 (지도 표시)
8. [디자인]  로딩 상태, 에러 상태 UI 처리
9. [공통]    QA 체크리스트 검증 + API 키 보안 확인
```

### 시나리오 D: 버그 수정
```
1. [공통]    버그 재현 → 원인 파악 (백엔드 vs 프론트엔드)
2. [담당자]  해당 영역 수정
3. [담당자]  수정이 다른 영역에 영향 주는지 확인
4. [공통]    QA 체크리스트 검증
```

---

## 6. File Ownership — 파일 소유권 가이드

> 각 에이전트가 주로 수정하는 파일과 공동 관리 파일을 명확히 구분합니다.

| 파일/디렉토리 | 주 담당 | 비고 |
|--------------|--------|------|
| `models.py` | 🔧 개발 | 모델 정의, 필드 추가 |
| `views.py` | 🔧 개발 | 비즈니스 로직, context 전달 |
| `urls.py` | 🔧 개발 | URL 패턴 등록 |
| `forms.py` | 🔧 개발 | 폼 검증 로직 |
| `signals.py` | 🔧 개발 | 자동화 시그널 |
| `utils.py` | 🔧 개발 | API 호출, 유틸리티 함수 |
| `admin.py` | 🔧 개발 | 관리자 페이지 설정 |
| `settings.py` | 🔧 개발 | 프로젝트 설정 |
| `templates/*.html` | 🎨 디자인 | HTML 구조, DTL 태그 |
| `static/css/` | 🎨 디자인 | CSS 스타일 |
| `static/js/` | 🎨 디자인 | 프론트엔드 JS |
| `static/images/` | 🎨 디자인 | 이미지 에셋 |
| `base.html` | 🤝 공동 | 레이아웃 변경 시 상호 조율 |
| `requirements.txt` | 🔧 개발 | 패키지 추가 시 |
| `agent/workflow.md` | 🤝 공동 | 워크플로우 변경 시 합의 |

---

## 7. Communication Protocol — 소통 규칙

### 변경 알림 (필수)
다음 상황에서는 상대 에이전트에게 반드시 알려야 합니다:

| 상황 | 알림 방향 | 알림 내용 |
|------|----------|----------|
| 모델 필드 추가/변경 | 개발 → 디자인 | 필드명, 타입, 템플릿 반영 필요 여부 |
| context 변수 추가/변경 | 개발 → 디자인 | 변수명, 타입, 데이터 구조 |
| URL 변경/삭제 | 개발 → 디자인 | 영향받는 `{% url %}` 태그 목록 |
| 새 CSS 변수 필요 | 디자인 → 개발 | `:root`에 추가할 변수명/값 |
| 새 AJAX endpoint 필요 | 디자인 → 개발 | 요청 URL, method, 파라미터, 기대 응답 |
| base.html 수정 | 수정자 → 양쪽 | 변경 내용, 영향받는 자식 템플릿 |

### 충돌 방지
- **같은 파일 동시 수정 금지**: 특히 `base.html`, `dashboard.html` 등 공유 파일
- **순서 준수**: 데이터 레이어(모델) → 로직 레이어(뷰) → 프레젠테이션 레이어(템플릿) 순서
- **컨텍스트 동기화**: 개발부장의 Handoff 문서를 기준으로 디자인부장이 작업
