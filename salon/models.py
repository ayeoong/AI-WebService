from django.db import models
from django.conf import settings

# keywords
class KeywordModel(models.Model):
    word = models.CharField(max_length=255, blank=True, unique=True)
    input_num = models.IntegerField(default=0)
    admin_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.word

# image, music etc
class ArtUploadModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    filename = models.CharField(max_length=255, default='')
    thumbnail = models.CharField(max_length=255, default='')
    input_text = models.CharField(max_length=100, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result_favorite = models.CharField(max_length=255, blank=True)
    kind = models.IntegerField(default=0)    # 0:None, 1:image, 2:music, 

    def __str__(self):
        return self.name

class ArtKeywordModel(models.Model):
    art = models.ForeignKey(ArtUploadModel, on_delete=models.CASCADE)
    keyword = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.art.name + " " + self.keyword.word

# auto save, temp image, music etc
class AutoArtUploadModel(models.Model):
    name = models.CharField(max_length=100, default='')
    filename = models.CharField(max_length=255, default='')
    thumbnail = models.CharField(max_length=255, default='')
    input_text = models.CharField(max_length=100, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    kind = models.IntegerField(default=0)    # 0:None, 1:image, 2:music, 

    def __str__(self):
        return self.name
