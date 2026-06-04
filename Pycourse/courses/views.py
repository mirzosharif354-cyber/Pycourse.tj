from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

from .models import Course, Topic, Video, Test, Task, Enrollment, VideoProgress, TestResult, TaskSubmission
from .utils import get_enrollment, calc_progress
from .decorators import admin_required
from users.models import CustomUser

# ───── PUBLIC ─────
def home_view(request):
    return render(request, 'courses/home.html', {
        'courses': Course.objects.filter(is_active=True)
    })

@login_required
def course_list_view(request):
    enrolled_ids = list(Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True))
    return render(request, 'courses/course_list.html', {
        'courses': Course.objects.filter(is_active=True),
        'enrolled_ids': enrolled_ids,
    })

@login_required
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment, progress = get_enrollment(request.user, course)
    watched  = list(VideoProgress.objects.filter(user=request.user, video__course=course, watched=True).values_list('video_id', flat=True))
    answered = list(TestResult.objects.filter(user=request.user, test__course=course).values_list('test_id', flat=True))
    return render(request, 'courses/course_detail.html', {
        'course': course, 'enrollment': enrollment, 'progress': progress,
        'topics': course.topics.all(), 'videos': course.videos.all(),
        'tests': course.tests.all(), 'tasks': course.tasks.all(),
        'watched': watched, 'answered': answered,
    })

def rating_view(request):
    students = CustomUser.objects.filter(role='student', is_active=True).order_by('-score')[:50]
    return render(request, 'courses/rating.html', {'students': students})

# ───── API ─────
@login_required
@require_POST
def api_video_watched(request, vid):
    video = get_object_or_404(Video, pk=vid)
    vp, created = VideoProgress.objects.get_or_create(user=request.user, video=video)
    if not vp.watched:
        vp.watched = True; vp.watched_at = timezone.now(); vp.save()
        request.user.score += 5; request.user.save()
    return JsonResponse({'ok': True, 'score': request.user.score})

@login_required
@require_POST
def api_test_submit(request, tid):
    test = get_object_or_404(Test, pk=tid)
    data = json.loads(request.body)
    answer = data.get('answer', '')
    correct = (answer == test.correct_answer)
    result, created = TestResult.objects.get_or_create(
        user=request.user, test=test,
        defaults={'selected_answer': answer, 'is_correct': correct}
    )
    if not created:
        return JsonResponse({'ok': True, 'correct': result.is_correct, 'correct_answer': test.correct_answer})
    if correct:
        request.user.score += test.score_points; request.user.save()
    return JsonResponse({'ok': True, 'correct': correct, 'correct_answer': test.correct_answer, 'score': request.user.score})

@login_required
@require_POST
def api_task_submit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    data = json.loads(request.body)
    code = data.get('code', '').strip()
    if not code:
        return JsonResponse({'ok': False, 'msg': 'Код холӣ аст!'})
    sub = TaskSubmission.objects.create(user=request.user, task=task, code=code)
    return JsonResponse({'ok': True, 'id': sub.id})

# ───── ADMIN VIEWS ─────
from .decorators import admin_required

@admin_required
def admin_panel_view(request):
    return render(request, 'courses/admin_panel.html', {
        'total_students':  CustomUser.objects.filter(role='student').count(),
        'total_courses':   Course.objects.count(),
        'total_videos':    Video.objects.count(),
        'total_tests':     Test.objects.count(),
        'total_tasks':     Task.objects.count(),
        'pending':         TaskSubmission.objects.filter(status='pending').count(),
        'recent_subs':     TaskSubmission.objects.select_related('user','task').order_by('-submitted_at')[:10],
        'top_students':    CustomUser.objects.filter(role='student').order_by('-score')[:8],
    })

@admin_required
def admin_students_view(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        action = request.POST.get('action')
        user = get_object_or_404(CustomUser, pk=uid)
        if action == 'toggle_active':
            user.is_active = not user.is_active; user.save()
            messages.success(request, f"{'Фаъол' if user.is_active else 'Ғайрифаъол'} шуд!")
        elif action == 'reset_score':
            user.score = 0; user.save()
            messages.success(request, 'Хол сифр шуд!')
        return redirect('admin_students')
    students = CustomUser.objects.filter(role='student').order_by('-score')
    return render(request, 'courses/admin_students.html', {'students': students})

@admin_required
def admin_courses_view(request):
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'add':
            Course.objects.create(
                title=request.POST['title'], category=request.POST['category'],
                description=request.POST.get('description',''), icon=request.POST.get('icon','📚'),
                duration_hours=request.POST.get('hours',0))
            messages.success(request, '✅ Курс илова шуд!')
        elif a == 'del':
            Course.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, '🗑 Ҳазф шуд!')
        return redirect('admin_courses')
    return render(request, 'courses/admin_courses.html', {'courses': Course.objects.all()})

@admin_required
def admin_videos_view(request):
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'add':
            c = get_object_or_404(Course, pk=request.POST['cid'])
            Video.objects.create(
                course=c, title=request.POST['title'],
                description=request.POST.get('desc',''),
                duration_minutes=request.POST.get('dur',0),
                video_url=request.POST.get('url',''),
                video_file=request.FILES.get('file'),
                order=c.videos.count()+1)
            messages.success(request, '✅ Видео илова шуд!')
        elif a == 'del':
            Video.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, '🗑 Ҳазф шуд!')
        return redirect('admin_videos')
    return render(request, 'courses/admin_videos.html', {
        'videos': Video.objects.select_related('course').all(),
        'courses': Course.objects.all()
    })

@admin_required
def admin_topics_view(request):
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'add':
            c = get_object_or_404(Course, pk=request.POST['cid'])
            Topic.objects.create(course=c, title=request.POST['title'],
                description=request.POST.get('desc',''), order=c.topics.count()+1)
            messages.success(request, '✅ Мавзуъ илова шуд!')
        elif a == 'del':
            Topic.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, '🗑 Ҳазф шуд!')
        return redirect('admin_topics')
    return render(request, 'courses/admin_topics.html', {
        'topics': Topic.objects.select_related('course').all(),
        'courses': Course.objects.all()
    })

@admin_required
def admin_tests_view(request):
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'add':
            c = get_object_or_404(Course, pk=request.POST['cid'])
            Test.objects.create(
                course=c, question=request.POST['question'],
                option_a=request.POST['oa'], option_b=request.POST['ob'],
                option_c=request.POST.get('oc',''), option_d=request.POST.get('od',''),
                correct_answer=request.POST['correct'],
                score_points=request.POST.get('pts',10))
            messages.success(request, '✅ Тест илова шуд!')
        elif a == 'del':
            Test.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, '🗑 Ҳазф шуд!')
        return redirect('admin_tests')
    return render(request, 'courses/admin_tests.html', {
        'tests': Test.objects.select_related('course').all(),
        'courses': Course.objects.all()
    })

@admin_required
def admin_tasks_view(request):
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'add':
            c = get_object_or_404(Course, pk=request.POST['cid'])
            Task.objects.create(
                course=c, title=request.POST['title'],
                description=request.POST.get('desc',''),
                starter_code=request.POST.get('code',''),
                score_points=request.POST.get('pts',50),
                order=c.tasks.count()+1)
            messages.success(request, '✅ Вазифа илова шуд!')
        elif a == 'del':
            Task.objects.filter(pk=request.POST['pk']).delete()
            messages.success(request, '🗑 Ҳазф шуд!')
        return redirect('admin_tasks')
    return render(request, 'courses/admin_tasks.html', {
        'tasks': Task.objects.select_related('course').all(),
        'courses': Course.objects.all()
    })

@admin_required
def admin_submissions_view(request):
    if request.method == 'POST':
        sub = get_object_or_404(TaskSubmission, pk=request.POST['pk'])
        a = request.POST.get('action')
        if a == 'approve':
            sub.status='approved'; sub.feedback=request.POST.get('fb','Баракалла!')
            sub.reviewed_at=timezone.now(); sub.save()
            sub.user.score += sub.task.score_points; sub.user.save()
            messages.success(request, '✅ Тасдиқ шуд!')
        elif a == 'reject':
            sub.status='rejected'; sub.feedback=request.POST.get('fb','Аз нав кӯшиш кун.')
            sub.reviewed_at=timezone.now(); sub.save()
            messages.success(request, '❌ Рад шуд!')
        return redirect('admin_submissions')
    subs = TaskSubmission.objects.select_related('user','task__course').order_by('-submitted_at')
    return render(request, 'courses/admin_submissions.html', {'subs': subs})
