from django.contrib import admin
from .models import ImageKeywordModel, KeywordModel, ImageUploadModel, MusicKeywordModel, MusicUploadModel
from mypage.models import Member

# Register your models here.
admin.site.register(Member)
admin.site.register(KeywordModel)
admin.site.register(ImageUploadModel)
admin.site.register(MusicUploadModel)
admin.site.register(ImageKeywordModel)
admin.site.register(MusicKeywordModel)
