from django.db import models
from django.utils import timezone
from myApp.models import Contact
from django.contrib.auth import get_user_model

User = get_user_model()

# class Room(models.Model):
#     contact = models.OneToOneField(Contact, related_name='contact', on_delete=models.CASCADE)
#     is_closed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now=True)


# class Message(models.Model):
#     author = models.ForeignKey(User, related_name='author_messages', on_delete=models.SET_NULL, null=True)
#     room = models.ForeignKey(Room, related_name='room_messages', on_delete=models.CASCADE)    
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# class Participant(models.Model):
#     user = models.ForeignKey(User, related_name='user_participants', on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, related_name='room_participants', on_delete=models.CASCADE)
#     is_allowed = models.BooleanField(default=False) # 채팅방에 입장 허가 시 True
#     is_finished = models.BooleanField(default=False) # 채팅방에 참여중일 시 True

class Group(models.Model):
    name = models.CharField(max_length=100)
    contact = models.OneToOneField(Contact, on_delete=models.SET_NULL, related_name="group", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: image?
    
    # member status
    host = models.ForeignKey(User, related_name='user_groups', on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User, related_name="joined_groups", blank=True) # users joined
    pendings = models.ManyToManyField(User, related_name="pending_groups", blank=True) # users asked to join
    rejected = models.ManyToManyField(User, related_name ="rejected_groups", blank=True) # users rejected to join 

    def __str__(self):
        return self.name

    def last_10_messages(self, times=0):
        if not times:
            return list(group.messages.order_by("created_at"))[-30:0]
        return list(group.messages.order_by("created_at"))[-30*(times+1):(-30*times)]

    def to_json(self):
        last_message = self.messages.last()
        return {
            "name" : self.name,
            "group_profile_img" : self.contact.thumbnail.url if self.contact.thumbnail.url else "",
            "last_msg" : f"{last_message.author.username} : {last_message.text if last_message else ''}",
        }


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tup = tuple([self.author, self.group, self.text])
        return str(tup)

    def to_json(self):
        return {
            "author": self.author.username,
            "author_profile_img": self.author.image.url,
            "group": self.group.name,
            "content": message.text,
            "timestamp": str(message.created_at),
        }

    # def get_absolute_url(self):
    #     return reverse("home:group", kwargs={"grp_name": self.parent_group})
