from django.test import TestCase
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
# from .models import TestStorage
from .utils import save_storage_img
import requests

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

