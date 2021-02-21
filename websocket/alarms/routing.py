from . import consumers
from django.urls import re_path
websocket_urlpatterns = [
    re_path(r'ws/test/(?P<username>.*)/', consumers.UserTestConsumer),
]