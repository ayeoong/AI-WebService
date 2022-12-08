import os
import json
from urllib.request import urlopen
from uuid import uuid4
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



def uuid_name_upload_to(instance, filename): # instance는 이미지, 음악 파일
    # app_label = instance.__class__._meta.app_label # 앱 별로
    # cls_name = instance.__class__.__name__.lower() # 모델 별로
    # ymd_path = timezone.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex # 32 characters <-> uuid4 = 36 characters
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출 뒤 소문자로 변환
    return '/'.join([
        # app_label,
        # cls_name,
        # ymd_path,
        uuid_name + extension,
    ])

def image_generation(text): #실제 배포용 말고는 더미 이미지 사용
    try:
        if settings.TEST_LIVE_MODE or settings.REAL_LIVE_MODE:
            openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
            openai.api_key = "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"

            response = openai.Image.create( prompt=text,
                                    n=1,
                                    size="1024x1024")
            image_url = response['data'][0]['url']
        else:
            time.sleep(5)
            image_url = 'https://ifh.cc/g/5qCAX2.jpg'        
        return image_url
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)



def music_generation(tags):
    try:
        if settings.TEST_MODE or settings.TEST_LIVE_MODE or settings.REAL_LIVE_MODE:
            mus_filename =  generateMusic(tags)
        else:
            mus_filename = '로컬주소'
        return mus_filename
    except Exception as e:
        print("error_music", e)


def get_taglist(text):
    nltk_url = 'https://silken-oxygen-369215.de.r.appspot.com/'   # 배포 주소
    text_spapce = text.replace(' ', '%20')
    url_req = nltk_url + text_spapce

    try:
        f = urlopen(url_req)
        with f as url:
            data = json.loads(url.read().decode())['tokens']
    except Exception as e:
        print("error_tag", e)
        data = []
    return data


def translate_text(text):

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language='en')
    return result["translatedText"]



def save_img_and_thumbnail(content, img_filename):
    img_tn_filename = "_tn.".join(img_filename.split('.')) # 섬네일명: 이미지파일명_tn.jpg 

    img_file = Image.open(BytesIO(content))
    save_img(img_file, img_filename)

    img_file = Image.open(BytesIO(content))
    img_file.thumbnail((300, 300))
    save_img(img_file, img_tn_filename)  # 섬네일저장

    # img_filename = img_path + img_filename
    # img_tn_filename = img_path + img_tn_filename

    return img_filename, img_tn_filename


def save_img(image_file, img_filename):
    if settings.DEV_MODE or settings.TEST_MODE:
        img_storage_path = 'media/images/' #setting.media_images
        img_filepath = img_storage_path + img_filename
        image_file.save(img_filepath, 'PNG')
    else:
        with BytesIO() as output:  
            image_file.save(output, 'PNG') 
            with default_storage.open('/images/' + img_filename, 'w') as f:
                f.write(output.getvalue())
        


def save_music(music_file, mus_filename):
    if settings.DEV_MODE or settings.TEST_MODE:
        with open('media/musics/'+ mus_filename, 'wb') as f:
            f.write(music_file)
    else:
        with default_storage.open('/musics/' + mus_filename, 'w') as f:
            f.write(music_file)


def delete_img(img_filename):
    if settings.DEV_MODE or settings.TEST_MODE:
        os.remove(os.path.join(settings.MEDIA_ROOT, img_filename))

    else:
        bucket_name='dall-e-2-contents'
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('images/' + img_filename)
        blob.delete()

        print(f"Blob {img_filename} deleted.")


def delete_mus(mus_filename):

    if settings.DEV_MODE or settings.TEST_MODE:
        os.remove(os.path.join(settings.MEDIA_ROOT, mus_filename))
        
    else:    
        bucket_name='dall-e-2-contents'
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('musics/' + mus_filename)
        blob.delete()

        print(f"Blob {mus_filename} deleted.")
  