from django.db import models
from django.conf import settings

# keywords
class KeywordModel(models.Model):
    word = models.CharField(max_length=255, blank=True, unique=True, default='')
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
    result_favorite = models.CharField(max_length=255, blank=True, default='')
    kind = models.IntegerField(default=0)    # 0:None, 1:image, 2:music, 
    like_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def fileurl(self):
        if self.kind == 1:
            return settings.IMG_PATH + self.filename
        else:
            return settings.MUSIC_PATH + self.filename
    
    def thumbnailurl(self):
        if self.kind == 1:
            return settings.IMG_PATH + self.thumbnail
        else:
            return settings.MUSIC_PATH + self.thumbnail
        

class ArtKeywordModel(models.Model):
    art = models.ForeignKey(ArtUploadModel, on_delete=models.CASCADE)
    keyword = models.ForeignKey(KeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "-" + self.art.name + "-" + self.keyword.word

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

    def fileurl(self):
        if self.kind == 1:
            return settings.IMG_PATH + self.filename
        else:
            return settings.MUSIC_PATH + self.filename
    
    def thumbnailurl(self):
        if self.kind == 1:
            return settings.IMG_PATH + self.thumbnail
        else:
            return settings.MUSIC_PATH + self.thumbnail

    # def delete(self, *args, **kargs):
    #     # if self.filename:
    #     #     os.remove(os.path.join(settings.MEDIA_ROOT, self.filename.path)) # FileField일 때 사용가능

    #     minutes = 5
    #     del_autoart = self.uploaded_at__lte=(datetime.now() - timedelta(minutes=minutes))
    #     del_autoart_path = self.filename # '/media/이미지or뮤직/파일명.확장자명'
    #     if os.path.exists(del_autoart):
    #         os.remove(os.path.join(settings.MEDIA_ROOT, del_autoart_path))
    #     super(AutoArtUploadModel, self).delete(*args, **kargs)
        