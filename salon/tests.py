from django.test import TestCase
from django.contrib import auth
from salon.models import ImageUploadModel, MusicUploadModel
from salon.utils import uuid_name_upload_to

# Create your tests here.

class YourTestClass(TestCase):
    pass
    # @classmethod
    # def setUpTestData(cls):
    #     print()
    #     print("setUpTestData: Run once to set up non-modified data for all class methods.")
    #     auth.user_logged_in()
    #     user = (username="홍길동", email="test@test.com", password="1234")
    #     user.save()

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    # def test_image_upload_model(self):
    #     user = Member.objects.get(id=1)
    #     filepath = uuid_name_upload_to(None, filename="iamge_file.png")
    #     imgfile = ImageUploadModel(user=user, description="photo", document=filepath)
    #     imgfile.save()
    #     print(imgfile)

    # def test_music_upload_model(self):
    #     user = Member.objects.get(id=1)
    #     filepath = uuid_name_upload_to(None, filename="music_file.mid")
    #     muscifile = MusicUploadModel(user=user, title="music", file=filepath)
    #     muscifile.save()
    #     print(muscifile)

    # def test_str_index(self):
    #     a = 'music_file.mid'
    #     print('---------', a[-3:])

    # def test_result_favorite(self):
    #     result_favorite = 1
    #     user = Member.objects.get(id=1)
    #     favorite = MusicUploadModel(user = user, result_favorite=result_favorite)
    #     favorite.save()
    #     print(favorite, favorite.result_favorite )

    # def test_home():
    #     image = ImageUploadModel.objects.filter(name='melon_image')
    #     print(image)
