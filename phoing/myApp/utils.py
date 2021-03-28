import os
from uuid import uuid4
from django.utils import timezone
import math

import requests
import re
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# from .models import Tag

# models.py에도 utils가 import 돼 있어 순환참조
# Tag 따로 안쓰길래 주석처리함
#from .models import Tag


def list_to_four_groups(queryset_list):
    l_zero = []
    l_one = []
    l_two = []
    l_three = []
    for idx, val in enumerate(queryset_list):
        if idx % 4 == 0:
            l_zero.append(val)
        elif idx % 4 == 1:
            l_one.append(val)
        elif idx % 4 == 2:
            l_two.append(val)
        else:
            l_three.append(val)
    return l_zero, l_one, l_two, l_three


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



def save_image_from_url(user, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    user.image.save(uuid_name_upload_to(user, user.email),
                    File(img_temp), save=True)
