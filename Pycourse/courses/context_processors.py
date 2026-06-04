from .models import Course
from chat.models import ChatRoom

def site_stats(request):
    return {
        'total_courses': Course.objects.filter(is_active=True).count(),
        'chat_rooms': ChatRoom.objects.filter(is_active=True),
    }
