from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from salon.models import ArtUploadModel


# Create your models here.

class ArtLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    art = models.ForeignKey(ArtUploadModel, on_delete=models.CASCADE, related_name='like_art')
    created_at = models.DateTimeField(auto_now_add=True)
    kind = models.IntegerField(default=0) #  # 0:None, 1:image, 2:music, 
    like_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.art.name} {self.user.username}'
     
