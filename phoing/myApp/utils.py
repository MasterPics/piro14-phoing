import os
from uuid import uuid4
from django.utils import timezone
import math

import requests
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile



def uuid_name_upload_to(instance, filename):
    app_label = instance.__class__._meta.app_label  # 앱 별로
    cls_name = instance.__class__.__name__.lower()  # 모델 별로
    ymd_path = timezone.now().strftime('%Y/%m/%d')  # 업로드하는 년/월/일 별로
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()  # 확장자 추출하고, 소문자로 변환
    return '/'.join([
        app_label,
        cls_name,
        ymd_path,
        uuid_name[:2],
        uuid_name + extension,
    ])


def get_distance(latlng1, latlng2):
    R = 6373.0
    lat1 = math.radians(latlng1[0])
    lon1 = math.radians(latlng1[1])
    lat2 = math.radians(latlng2[0])
    lon2 = math.radians(latlng2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return c


def get_contacts_in_ten_kilo(user):
    user_lat = user.lat
    user_lng = user.lng

    valid_contacts = list()

    contacts = Contact.objects.all()
    for contanct in contancts:
        distance = get_distance(
            [user.lat, user.lng],
            [contact.lat, contact.lng]
        )
        if distance < 10:
            valid_contacts.append(contact)
    return valid_contacts


def save_image_from_url(user, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    user.image.save(uuid_name_upload_to(user, user.email),
                    File(img_temp), save=True)


