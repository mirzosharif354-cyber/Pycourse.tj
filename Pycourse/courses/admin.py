from django.contrib import admin
from .models import Course, Topic, Video, Test, Task, Enrollment, TaskSubmission

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title','category','duration_hours','is_active')
    list_filter  = ('category','is_active')
    search_fields = ('title',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','course','order')
    list_filter  = ('course',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title','course','order','duration_minutes','is_free')
    list_filter  = ('course','is_free')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('question','course','correct_answer','score_points')
    list_filter  = ('course',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','course','score_points')
    list_filter  = ('course',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user','course','progress','enrolled_at')

@admin.register(TaskSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display  = ('user','task','status','submitted_at')
    list_filter   = ('status',)
    list_editable = ('status',)
