from django.test import TestCase
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
# from .models import TestStorage
import requests
from .music import generateMusic
from django.conf import settings
from google.cloud import storage
import six
from google.cloud import translate_v2 as translate


from google.cloud import storage

class StorageTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print()
        print("setUpTestData: Run once to set up non-modified data for all class methods.")


    def setUp(self):
        print()
        print("==============setUp: Run once for every test method to setup clean data.")


    def tearDown(self):
        print("==============tearDown: Run once for every test method")


    # def test_storages(self):
    #     print(default_storage.__class__)
    #     #바이트를 이미지로
    #     image_url = 'https://ifh.cc/g/5qCAX2.jpg'
    #     res = requests.get(image_url)
    #     img_file = Image.open(BytesIO(res.content))
        

    #     # Image.frombytes# 이미지를 바이트로
    #     file = default_storage.open('storage_test.jpg', 'w') 
    #     file.write(img_file.tobytes())
    #     file.close() #
    
    def test_storages_view(self):
        print( default_storage.exists('storage_test.jpg') )
        img_url = 'https://storage.cloud-media/storage_test.jpg'
    
    def test_storages2(self):
        image_url = 'https://ifh.cc/g/5qCAX2.jpg' 
        res = requests.get(image_url)
        img_file = Image.open(BytesIO(res.content)) #url에서 바이트를 가져와 메모리에 올림, 그걸 이미지로 open

        filename = 'storage_test.jpg'
        save_storage_img(img_file, filename)

        img_file.thumbnail((150, 150))  
        filename = 'storage_test' + '_tn' + '.jpg'
        save_storage_img(img_file, filename)
    
    def test_pj_mode(self):
        PJ_MODE = 3           # 0:dev, 1:test, 2:live

        pj_mode = {}
        pj_mode[0] = [True, False, False, False]
        pj_mode[1] = [False, True, False, False]
        pj_mode[2] = [False, False, True, False]
        pj_mode[3] = [False, False, False, True]

        DEV_MODE= pj_mode[PJ_MODE][0] #
        TEST_MODE = pj_mode[PJ_MODE][1] #
        TEST_LIVE_MODE = pj_mode[PJ_MODE][2] #gcp스토리지 및 sql 활성화  달리만 주석
        REAL_LIVE_MODE = pj_mode[PJ_MODE][3] #달리 음악 생성 모델 활성화

        # GCP 프로젝트지명 및 SQL 활성화
        if TEST_LIVE_MODE:
            GOOGLE_CLOUD_PROJECT='dall-e-2'
            USE_CLOUD_SQL_AUTH_PROXY=True
            print('TEST_LIVE_MODE')
        elif REAL_LIVE_MODE:
            GOOGLE_CLOUD_PROJECT='dall-e-2'
            USE_CLOUD_SQL_AUTH_PROXY=True
            print('REAL_LIVE_MODE')
        
    
    def test_pj_mode2(self):
        PJ_MODE = 2
        pj_mode = [False, False, False, False]
        pj_mode[PJ_MODE] = True

        DEV_MODE= pj_mode[0]
        TEST_MODE = pj_mode[1]
        TEST_LIVE_MODE = pj_mode[2]
        REAL_LIVE_MODE = pj_mode[3]

        print(DEV_MODE, TEST_MODE, TEST_LIVE_MODE, REAL_LIVE_MODE)

    def test_storage_music(self):
        filename = 'testmusic'
        with BytesIO() as output:
            music =  generateMusic('disney')
            music.open()
            music.write(output)
            with default_storage.open('/musics/' + filename, 'w') as f:
                f.write(output.getvalue())



    def test_storage_corf(self):
        bucket('dall-e-2-media')
        def bucket(bucket_name):
            """Prints out a bucket's metadata."""
            # bucket_name = 'your-bucket-name'

            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)

            print(f"ID: {bucket.id}")
            print(f"Name: {bucket.name}")
            print(f"Storage Class: {bucket.storage_class}")
            print(f"Location: {bucket.location}")
            print(f"Location Type: {bucket.location_type}")
            print(f"Cors: {bucket.cors}")
            print(f"Default Event Based Hold: {bucket.default_event_based_hold}")
            print(f"Default KMS Key Name: {bucket.default_kms_key_name}")
            print(f"Metageneration: {bucket.metageneration}")
            print(
                f"Public Access Prevention: {bucket.iam_configuration.public_access_prevention}"
            )
            print(f"Retention Effective Time: {bucket.retention_policy_effective_time}")
            print(f"Retention Period: {bucket.retention_period}")
            print(f"Retention Policy Locked: {bucket.retention_policy_locked}")
            print(f"Requester Pays: {bucket.requester_pays}")
            print(f"Self Link: {bucket.self_link}")
            print(f"Time Created: {bucket.time_created}")
            print(f"Versioning Enabled: {bucket.versioning_enabled}")
            print(f"Labels: {bucket.labels}")


    def test_del_contents(self):

        mus_filename = 'test_mid.mid'

        """Deletes a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # blob_name = "your-object-name"
        bucket_name='dall-e-2-contents'
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('musics/test_mid.mid')
        print(blob)
        blob.delete()

        print(f"Blob {mus_filename} deleted.")

    def test_tag(self):
        def get_taglist(text):
            nltk_url = 'https://silken-oxygen-369215.de.r.appspot.com/'   # 배포 주소
            text_spapce = text.replace(' ', '%20')
            url_req = nltk_url + text_spapce

            f = urlopen(url_req)
            with f as url:
                data = json.loads(url.read().decode())['tokens']
            return data


    def test_translate(self):
        def translate_text(text):

            translate_client = translate.Client()

            if isinstance(text, six.binary_type):
                text = text.decode("utf-8")

            # Text can also be a sequence of strings, in which case this method
            # will return a sequence of results for each text.
            result = translate_client.translate(text, target_language='en')

            print(u"Text: {}".format(result["input"]))
            print(u"Translation: {}".format(result["translatedText"]))
            print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
            print(result)
        translate_text('수영하는 비행기')
