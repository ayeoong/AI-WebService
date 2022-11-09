from django.contrib import admin
from .models import SampleKeyword, ImageUploadModel, MusicUploadModel, Member, Img_Mon, KeywordModel

# Register your models here.
admin.site.register(Member)
admin.site.register(SampleKeyword)
admin.site.register(ImageUploadModel)
admin.site.register(MusicUploadModel)
#model 하나 등록
admin.site.register(Img_Mon)
#mediafile모델 등록



