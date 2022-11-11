from django.test import TestCase
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
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


    def test_storages(self):
        print(default_storage.__class__)

        image_url = 'https://ifh.cc/g/5qCAX2.jpg'
        res = requests.get(image_url)
        img_file = Image.open(BytesIO(res.content))

        # Image.frombytes# 이미지를 바이트로
        file = default_storage.open('storage_test.jpg', 'w')
        file.write(BytesIO(res.content))
        file.close()
    
    def test_storages_view(self):
        print( default_storage.exists('storage_test.jpg') )
        img_url = 'https://storage.cloud-media/storage_test.jpg'