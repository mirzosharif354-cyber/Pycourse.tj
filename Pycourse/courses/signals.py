from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskSubmission

@receiver(post_save, sender=TaskSubmission)
def notify_on_submission(sender, instance, created, **kwargs):
    """Placeholder: notify admin when new task is submitted."""
    if created:
        pass  # Add email/notification logic here
