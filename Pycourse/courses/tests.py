from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Course, Topic, Video, Test, Task, Enrollment

User = get_user_model()

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(title='Test', category='python', description='Test', icon='🐍')
    def test_course_str(self):
        self.assertEqual(str(self.course), 'Test')
    def test_total_videos(self):
        self.assertEqual(self.course.total_videos(), 0)
