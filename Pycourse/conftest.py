# pytest configuration
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycourse.settings')
def pytest_configure(): django.setup()
