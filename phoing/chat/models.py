from django.db import models
from myApp.models import Contact
from user.models import User

class Room(models.Model):
    contact = models.OneToOneField(Contact, related_name='contact', on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, related_name='room_messages', on_delete=models.CASCADE)    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Participant(models.Model):
    user = models.ForeignKey(User, related_name='user_participants', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_participants', on_delete=models.CASCADE)
    is_allowed = models.BooleanField(default=False) # 채팅방에 입장 허가 시 True
    is_finished = models.BooleanField(default=False) # 채팅방에 참여중일 시 True


    


    






