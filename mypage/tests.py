from django.test import TestCase
from django.contrib.auth.models import User
from .models import ArtLike
from salon.models import ArtUploadModel


class MypageTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print()
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        user = User.objects.create(username='tester')
        user.set_password('1234')
        user.save()
        user2 = User.objects.create(username='tester2')
        user2.set_password('1234')
        user2.save()
        ArtUploadModel(user=user, name='test_photo', filename='test.jpg').save()

    def setUp(self):
        print("================setUp: Run once for every test method to setup clean data.")
    
    def tearDown(self):
        print("================tearDown: Run once for every test method.")

    def test_like(self):
        user = User.objects.get(username='tester')
        user2 = User.objects.get(username='tester2')
        art = ArtUploadModel.objects.get(id=1)

        self.save_toggle_like(user, art)
        self.save_toggle_like(user2, art)

        result = ArtLike.objects.filter(art=art).count()
        self.assertEqual(2, result )

        self.save_toggle_like(user, art)

        result = ArtLike.objects.filter(art=art).count()
        self.assertEqual(1, result )


    def save_toggle_like(self, user, art):
        artlikes = ArtLike.objects.filter(user=user, art=art)
        ArtLike(user=user, art=art).save() if len(artlikes) <= 0 else artlikes[0].delete()
    
    def test_like_orm(self):
        owner_user = User.objects.get(username='tester')
        like_user = User.objects.get(username='tester2')
        art = ArtUploadModel.objects.get(id=1)

        self.save_toggle_like(like_user, art)
        self.save_toggle_like(like_user, art)

        images = ArtUploadModel.objects.filter(user=owner_user)

        likeset = ArtLike.objects.filter(art__user=owner_user).filter(user=like_user)
        likeset = [like.art for like in likeset]
        print( likeset ) 

        for img in images:
            if img in likeset:
                print('find like', img)
            else:
                print('not like img')

        print( str(ArtLike.objects.filter(art__user=owner_user).filter(user=like_user).query) )





