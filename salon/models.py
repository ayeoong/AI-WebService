from django.db import models
from django.conf import settings

# keywords
class KeywordModel(models.Model):
    word = models.CharField(max_length=255, blank=True, unique=True)
    input_num = models.IntegerField(default=0)
    admin_mode = models.BooleanField(default=False)

    def __str__(self):
        return self.word


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

# music
class MusicUploadModel(models.Model):
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
    image = models.ForeignKey(ImageUploadModel, related_name="image_set", on_delete=models.CASCADE)
    keyword = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name + " " + self.keyword.word

class MusicKeywordModel(models.Model):
    music = models.ForeignKey(MusicUploadModel, on_delete=models.CASCADE)
    keyword = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.music.name + " " + self.keyword.word
