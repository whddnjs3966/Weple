# Developer Agent Skills - Weple Project

## 1. Core Framework & Environment
- **Django 6.0 / Python 3.10+**: Proficiency in the latest Django features and asynchronous support.
- **Project Structure**: Deep understanding of the 'Weple' project structure (apps: `accounts`, `core`, `vendors`, `weddings`, `reviews`).
- **Dependency Management**: Familiarity with `requirements.txt` (including `django-allauth`, `widget_tweaks`).

## 2. Specialized Wedding Logic
- **Wedding Group Logic**: Managing shared schedules through `WeddingGroup` and `WeddingProfile`.
- **D-Day & Scheduling**: Implementation of d-day offsets and wedding-date based task generation (referencing `weddings.signals`).
- **Budgeting System**: Managing `estimated_budget` within `ScheduleTask` and performing aggregate sums.

## 3. Database & ORM
- **Complex Relationships**: Handling OneToOne (Profile-User), ForeignKey (Task-Group), and ManyToMany (Post-Recommendations).
- **Advanced Querying**: Using `annotate`, `Sum`, and `Count` for dashboard statistics and community features.

## 4. Authentication & Social Login
- **Allauth Integration**: Naver/Social account management and custom login/signup flows (`CustomLoginView`).
