# Weple Development Workflow

## 1. Feature Request Analysis
- Analyze the request against the existing apps (`weddings` for logic, `vendors` for data).
- Developer Agent checks if new models or fields are required (e.g., adding `location` to `ScheduleTask`).

## 2. Backend First (Developer Agent)
- **Step 1**: Update `models.py` and run migrations.
- **Step 2**: Create or update `views.py` with the required business logic (D-day calc, filtering, etc.).
- **Step 3**: Define URL patterns in the respective app's `urls.py`.

## 3. Frontend Integration (Design Agent)
- **Step 4**: Design the UI in `templates/` following the existing `glass-card` and `fade-in` styles.
- **Step 5**: Map backend context variables to the template.
- **Step 6**: Add necessary JavaScript for interactivity (modals, checkbox logic).

## 4. Quality Assurance
- Verify that social login (Naver) remains functional.
- Ensure all numbers are formatted with `intcomma` (humanize).
- Check that `WeddingGroup` ownership is validated in every POST request.
