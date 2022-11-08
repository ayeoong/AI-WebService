from django.db import models
<<<<<<< HEAD
from django.conf import settings

# # keywords
# class SampleKeyword(models.Model):
#     keyword = models.CharField(max_length=255, blank=True)
#     updated_at = models.DateTimeField(auto_now_add=True)

# # img
# class ImageUploadModel(models.Model):
#     name = models.CharField(max_length=100)
#     filename = models.CharField(max_length=255)
#     thumbnail = models.CharField(max_length=255)
#     input_text = models.CharField(max_length=100)
#     # blank=True : Form에서 빈 채로 저장되는 것을 허용 (views.py에서 활용한 .is_valid() 함수가 검증 진행 시)
#     description = models.CharField(max_length=255, blank=True) 
#     # upload_to : 저장될 파일의 경로를 지정 (ex. ‘images/2020/02/21/test_image.jpg’)
#     document = models.CharField(max_length=255) # 원래코드 'images/%Y/%m/%d'
#     # auto_now_add : 자동으로 저장되는 시점을 기준으로 현재 시간을 세팅
#     user = models.ForeignKey(Member, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#         # Java의 toString
#     def __str__(self):
#         return self.document



# # music
# class MusicUploadModel(models.Model):
#     title = models.CharField(max_length=122, blank=True, null=True, default="No Title")
#     file = models.CharField(max_length=255) # 원래코드 "media/"%Y/%m/%d" 
#     user = models.ForeignKey(Member, on_delete=models.CASCADE)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.file


# keywords
class KeywordModel(models.Model):
    word = models.CharField(max_length=255, blank=True, unique=True)
    input_num = models.IntegerField(default=0)
    admin_mode = models.BooleanField(default=False)


# img
class ImageUploadModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    filename = models.CharField(max_length=255, default='')
    thumbnail = models.CharField(max_length=255, default='')
    input_text = models.CharField(max_length=100, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result_favorite = models.CharField(max_length=255, blank=True)

        # Java의 toString
    def __str__(self):
        return self.name
=======
from mypage.models import Member

# keywords
class SampleKeyword(models.Model):
    keyword = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

# img
class ImageUploadModel(models.Model):
    # blank=True : Form에서 빈 채로 저장되는 것을 허용 (views.py에서 활용한 .is_valid() 함수가 검증 진행 시)
    description = models.CharField(max_length=255, blank=True) 
    # upload_to : 저장될 파일의 경로를 지정 (ex. ‘images/2020/02/21/test_image.jpg’)
    document = models.CharField(max_length=255) # 원래코드 'images/%Y/%m/%d'
    # auto_now_add : 자동으로 저장되는 시점을 기준으로 현재 시간을 세팅
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

        # Java의 toString
    def __str__(self):
        return self.document
>>>>>>> a33a112e685bb6dc4d3439bac1b9ee0dd132d4d1



# music
class MusicUploadModel(models.Model):
<<<<<<< HEAD
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    filename = models.CharField(max_length=255, default='')
    thumbnail = models.CharField(max_length=255, default='')
    input_text = models.CharField(max_length=100, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result_favorite = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class ImageKeywordModel(models.Model):
    image_id = models.ForeignKey(ImageUploadModel, on_delete=models.CASCADE)
    keyword_id = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.image_id + self.keyword_id

class MusicKeywordModel(models.Model):
    music_id = models.ForeignKey(MusicUploadModel, on_delete=models.CASCADE)
    keyword_id = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.music_id + self.keyword_id
=======
    title = models.CharField(max_length=122, blank=True, null=True, default="No Title")
    file = models.CharField(max_length=255) # 원래코드 "media/"%Y/%m/%d" 
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file
>>>>>>> a33a112e685bb6dc4d3439bac1b9ee0dd132d4d1
