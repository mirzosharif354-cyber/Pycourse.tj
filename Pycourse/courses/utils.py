from .models import Enrollment, VideoProgress, TestResult

def calc_progress(user, course):
    total = course.videos.count() + course.tests.count()
    if total == 0:
        return 0
    watched  = VideoProgress.objects.filter(user=user, video__course=course, watched=True).count()
    answered = TestResult.objects.filter(user=user, test__course=course).count()
    return int((watched + answered) / total * 100)

def get_enrollment(user, course):
    enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)
    progress = calc_progress(user, course)
    enrollment.progress = progress
    enrollment.save()
    return enrollment, progress
