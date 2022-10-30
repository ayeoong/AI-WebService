from django.test import TestCase
from salon.models import Member, ImageUploadModel, MusicUploadModel
from salon.utils import uuid_name_upload_to

# Create your tests here.

class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print()
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        user = Member(username="홍길동", email="test@test.com", password="1234")
        user.save()

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_image_upload_model(self):
        user = Member.objects.get(id=1)
        filepath = uuid_name_upload_to(None, filename="iamge_file.png")
        imgfile = ImageUploadModel(user=user, description="photo", document=filepath)
        imgfile.save()
        print(imgfile)

    def test_music_upload_model(self):
        user = Member.objects.get(id=1)
        filepath = uuid_name_upload_to(None, filename="music_file.mid")
        muscifile = MusicUploadModel(user=user, title="music", file=filepath)
        muscifile.save()
        print(muscifile)

    def test_str_index(self):
        a = 'music_file.mid'
        print('---------', a[-3:])