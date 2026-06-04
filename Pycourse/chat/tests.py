from django.test import TestCase
from .models import ChatRoom, Message

class ChatRoomTest(TestCase):
    def setUp(self):
        self.room = ChatRoom.objects.create(slug='test', name='Test', icon='💬')
    def test_room_str(self):
        self.assertEqual(str(self.room), 'Test')
