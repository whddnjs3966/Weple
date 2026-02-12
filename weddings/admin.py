from django.contrib import admin
from .models import WeddingGroup, WeddingProfile, ScheduleTask, DailyLog, Notice, Post, PostComment, NoticeComment

@admin.register(WeddingGroup)
class WeddingGroupAdmin(admin.ModelAdmin):
    list_display = ('invite_code', 'wedding_date', 'created_at')

@admin.register(WeddingProfile)
class WeddingProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'created_at')

@admin.register(ScheduleTask)
class ScheduleTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'date', 'is_done', 'category')
    list_filter = ('is_done', 'category', 'group')

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'group', 'created_at')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')

@admin.register(NoticeComment)
class NoticeCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'notice', 'created_at')
