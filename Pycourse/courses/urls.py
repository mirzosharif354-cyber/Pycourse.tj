from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('',           views.home_view,        name='home'),
    path('courses/',   views.course_list_view,  name='course_list'),
    path('courses/<int:pk>/', views.course_detail_view, name='course_detail'),
    path('rating/',    views.rating_view,       name='rating'),
    # API
    path('api/video/<int:vid>/watched/',    views.api_video_watched, name='api_video_watched'),
    path('api/test/<int:tid>/submit/',      views.api_test_submit,   name='api_test_submit'),
    path('api/task/<int:task_id>/submit/',  views.api_task_submit,   name='api_task_submit'),
    # Admin
    path('admin-panel/',              views.admin_panel_view,       name='admin_panel'),
    path('admin-panel/students/',     views.admin_students_view,    name='admin_students'),
    path('admin-panel/courses/',      views.admin_courses_view,     name='admin_courses'),
    path('admin-panel/videos/',       views.admin_videos_view,      name='admin_videos'),
    path('admin-panel/topics/',       views.admin_topics_view,      name='admin_topics'),
    path('admin-panel/tests/',        views.admin_tests_view,       name='admin_tests'),
    path('admin-panel/tasks/',        views.admin_tasks_view,       name='admin_tasks'),
    path('admin-panel/submissions/',  views.admin_submissions_view, name='admin_submissions'),
]
