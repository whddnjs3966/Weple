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
        
        # Wedding Checklist Templates (Category, Title, Start D-Day Offset, Description)
        # Offset: Negative means days BEFORE wedding.
        default_tasks = [
            # D-365 ~ D-200 (Early Planning)
            ('MEETING', '양가 부모님 첫인사', -365, '양가 부모님께 정식으로 인사드리고 결혼 승낙을 받습니다.'),
            ('MEETING', '상견례 날짜/장소 확정', -300, '양가 어른들의 일정을 조율하여 상견례 날짜와 장소를 정합니다.'),
            ('VENUE', '웨딩홀 투어 및 계약', -300, '원하는 지역/시간대/보증인원을 고려해 웨딩홀을 비교하고 계약합니다.'),
            ('SDM', '본식 스냅/DVD 예악', -280, '인기 있는 스냅/DVD 업체는 1년 전부터 마감되니 미리 예약하세요.'),
            ('HONEYMOON', '신혼여행지 결정', -270, '휴양지 vs 관광지 등 취향에 맞춰 신혼여행지를 결정합니다.'),
            
            # D-200 ~ D-150 (Major Vendors)
            ('SDM', '스드메 업체 선정 및 계약', -200, '스튜디오, 드레스, 메이크업 업체를 선정하고 계약합니다(플래너 동행 여부 결정).'),
            ('HONEYMOON', '신혼여행 항공권 예약', -190, '얼리버드 특가 등을 활용해 항공권을 미리 예매합니다.'),
            ('ATTIRE', '신랑 예복 맞춤 상담/계약', -180, '맞춤 예복 제작 기간을 고려하여 미리 상담을 받습니다.'),
            ('ATTIRE', '양가 혼주 한복 알아보기', -170, '맞춤 대여 또는 구매 여부를 결정하고 업체를 알아봅니다.'),
            ('SDM', '드레스 투어', -150, '드레스샵 2~3곳을 투어하며 원하는 스타일의 샵을 지정합니다.'),

            # D-150 ~ D-100 (Details & Housing)
            ('FURNISHING', '신혼집 알아보기', -140, '예산과 출퇴근 거리를 고려해 신혼집을 구하고 계약합니다.'),
            ('SDM', '웨딩 촬영(스튜디오)', -130, '스튜디오 리허설 촬영을 진행합니다. (간식 준비 필수!)'),
            ('ATTIRE', '예물/예단 준비', -120, '양가 협의 하에 예물/예단 범위를 정하고 준비합니다.'),
            ('HONEYMOON', '신혼여행 숙소 예약', -110, '여행 동선에 맞춰 숙소를 예약합니다.'),
            ('FURNISHING', '가전/가구 리스트업 및 구매', -100, '신혼집 입주 날짜에 맞춰 필요한 가전/가구를 구매합니다.'),

            # D-100 ~ D-60 (Invitations & Ceremony)
            ('INVITATION', '청첩장 샘플 신청 및 주문', -90, '여러 업체에서 샘플을 받아보고 디자인을 결정하여 주문합니다.'),
            ('INVITATION', '하객 리스트 정리', -85, '예상 하객 인원을 파악하고 주소록을 정리합니다.'),
            ('OTHER', '주례/사회자/축가 섭외', -80, '예식을 빛내줄 지인이나 전문 사회자를 섭외합니다.'),
            ('SDM', '모바일 청첩장 제작', -70, '스튜디오 수정본이 나오면 모바일 청첩장을 제작합니다.'),
            ('OTHER', '식전 영상 사진 셀렉', -65, '연애 시절 사진과 웨딩 사진을 모아 식전 영상을 제작합니다.'),
            ('INVITATION', '종이 청첩장 발송 및 모임', -60, '지인들에게 식사를 대접하며 청첩장을 전달합니다.'),

            # D-60 ~ D-30 (Final Checks)
            ('ATTIRE', '본식 드레스 가봉', -45, '본식 날 입을 드레스를 최종 선택하고 사이즈를 체크합니다.'),
            ('ATTIRE', '부케 고르기', -40, '드레스와 홀 분위기에 어울리는 부케를 선택/주문합니다.'),
            ('CONTRACT', '폐백 음식 주문', -35, '폐백을 진행한다면 음식을 주문합니다.'),
            ('CONTRACT', '웨딩홀 시식 및 식순 체크', -30, '실제 식사를 시식해보고, 예식 순서와 BGM을 점검합니다.'),
            ('FURNISHING', '이바지 음식 준비', -25, '필요 시 친정어머니께서 준비하실 이바지 음식을 체크합니다.'),

            # D-20 ~ D-Day (D-Day Prep)
            ('OTHER', '본식 BGM/식권/소품 준비', -20, '식중 영상, 포토테이블 사진, 식권 도장 등 소품을 챙깁니다.'),
            ('SDM', '웨딩카/메이크업샵 이동수단 확인', -15, '당일 이동 동선과 차량을 확보합니다.'),
            ('OTHER', '네일/염색/피부관리', -10, '본식 일주일 전 컨디션 관리에 들어갑니다.'),
            ('CONTRACT', '최종 보증인원 확정', -7, '웨딩홀에 최종 식수 인원을 통보합니다.'),
            ('CONTRACT', '사회자/축가자 최종 리허설', -5, '대본과 MR을 전달하고 최종 확인합니다.'),
            ('OTHER', '본식 가방 싸기', -1, '반지, 신분증, 헬퍼비(봉투), 여분 마스크 등 당일 준비물 챙기기.'),
            ('OTHER', '결혼식', 0, '가장 행복한 주인공이 되는 날!'),
        ]

        tasks_to_create = []
        for category, title, offset, desc in default_tasks:
            # Note: date is set to None initially ("Unscheduled").
            # expected_date can be useful if we want to show "Target Date".
            # For this MVP, we rely on d_day_offset for sorting.
            tasks_to_create.append(
                ScheduleTask(
                    profile=instance,
                    date=None,  # Unscheduled initially
                    title=title,
                    description=desc,
                    d_day_offset=offset,
                    category=category
                )
            )
        
        ScheduleTask.objects.bulk_create(tasks_to_create)
