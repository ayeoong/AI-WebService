from os import path
from uuid import uuid4
<<<<<<< HEAD
from django.utils import timezone
=======
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image
from django.conf import settings
import openai
import time
from salon.music import generateMusic
from google.cloud import storage

import six
from google.cloud import translate_v2 as translate


>>>>>>> 9507045 (구버전 구글트랜스 삭제)

def uuid_name_upload_to(instance, filename): # instance는 이미지, 음악 파일
    # app_label = instance.__class__._meta.app_label # 앱 별로
    # cls_name = instance.__class__.__name__.lower() # 모델 별로
    # ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex # 32 characters <-> uuid4 = 36 characters
    extension = path.splitext(filename)[-1].lower() # 확장자 추출 뒤 소문자로 변환
    return '/'.join([
        # app_label,
        # cls_name,
        # ymd_path,
        uuid_name + extension,
    ])


  