from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .models import WeddingProfile, ScheduleTask

@receiver(post_save, sender=WeddingProfile)
def create_default_schedule(sender, instance, created, **kwargs):
    """
    WeddingProfile이 생성되거나 업데이트될 때(날짜 변경 등),
    기본 스케줄을 생성하거나 업데이트하는 로직.
    MVP에서는 생성 시점에만 템플릿을 복사하는 형태로 단순화.
    """
    if created:
        wedding_date = instance.wedding_date
        
        # MVP용 하드코딩된 스케줄 템플릿
        # (title, d_day_offset, description)
        default_tasks = [
            ("웨딩홀 투어 및 계약", -300, "인기 있는 웨딩홀은 1년 전부터 마감되니 서두르세요!"),
            ("스드메(스튜디오/드레스/메이크업) 알아보기", -240, "원하는 스타일을 스크랩하고 업체를 선정해보세요."),
            ("본식 스냅/DVD 예약", -210, "유명한 작가님들은 빨리 마감됩니다."),
            ("신혼여행 예약", -180, "항공권과 숙소를 미리 예약해야 저렴합니다."),
            ("드레스 투어", -150, "입어보고 싶은 드레스샵 2-3곳을 투어해보세요."),
            ("웨딩 촬영", -120, "스튜디오 촬영을 진행하고 모바일 청첩장용 사진을 셀렉하세요."),
            ("청첩장 주문", -90, "하객 리스트를 정리하고 청첩장을 주문하세요."),
            ("청첩장 모임 시작", -60, "지인들에게 청첩장을 전달하며 식사를 대접하세요."),
            ("본식 드레스 가봉", -30, "본식 날 입을 드레스를 최종 결정하고 사이즈를 체크하세요."),
            ("부케 주문 및 사회자/축가 섭외", -20, "예식 분위기에 맞는 부케와 식순을 챙겨주세요."),
            ("최종 점검", -7, "식권, 포토테이블, 식순 등 빠진 것이 없는지 확인하세요."),
            ("결혼식", 0, "행복한 결혼식 날입니다!"),
        ]

        tasks_to_create = []
        for title, offset, desc in default_tasks:
            task_date = wedding_date + timedelta(days=offset)
            tasks_to_create.append(
                ScheduleTask(
                    profile=instance,
                    date=task_date,
                    title=title,
                    description=desc,
                    d_day_offset=offset
                )
            )
        
        ScheduleTask.objects.bulk_create(tasks_to_create)
