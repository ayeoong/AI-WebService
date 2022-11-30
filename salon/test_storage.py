from django.test import TestCase
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
# from .models import TestStorage
from .utils import save_storage_img
import requests
from .music import generateMusic
import os
from django.conf import settings
from google.cloud import storage

import time


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

    def test_midi_to_wave(self):
        print( os.listdir(os.getcwd()) )
        print( os.listdir(settings.MEDIA_ROOT + '/musics/') )
        FluidSynth().midi_to_audio(str(settings.MEDIA_ROOT + '/musics/MuseNet-Composition.mid'), str(settings.MEDIA_ROOT + '/musics/melody.wav'))
        #print( os.listdir('/media/musics/') )


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

        music_file = 'media\musics\MuseNet-Composition.mid'
        mus_filename = 'test_mid.mid'

        # with default_storage.open('/musics/' + mus_filename, 'w') as f:
        #     f.write(music_file)
        #     print('성공적으로 저장하였습니다')
        #     time.sleep(5)

        # with default_storage.open('/musics/' + mus_filename, 'r') as f:
        #     f.read()
        #     print('성공적으로 읽었습니다')
        #     time.sleep(5)

        # default_storage.delete(music_file)
        # print('성공적으로 삭제하였습니다')

        # with default_storage.open('/musics/' + mus_filename, 'r') as f:
        #     f.read()
        #     print('파일이 존재하지 않습니다')
        #     time.sleep(5)



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

        def delete_blob(bucket_name, blob_name):
            """Deletes a blob from the bucket."""
            # bucket_name = "your-bucket-name"
            # blob_name = "your-object-name"

            storage_client = storage.Client()

            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()

            print(f"Blob {blob_name} deleted.")        