from django.contrib import admin
from .models import KeywordModel, ArtKeywordModel, ArtUploadModel

# Register your models here.
admin.site.register(KeywordModel)
admin.site.register(ArtUploadModel)
admin.site.register(ArtKeywordModel)
