from django.contrib import admin
<<<<<<< HEAD
from .models import ImageKeywordModel, KeywordModel, ImageUploadModel, MusicKeywordModel, MusicUploadModel
from mypage.models import Member

# Register your models here.
admin.site.register(Member)
admin.site.register(KeywordModel)
admin.site.register(ImageUploadModel)
admin.site.register(MusicUploadModel)
admin.site.register(ImageKeywordModel)
admin.site.register(MusicKeywordModel)
=======
from .models import SampleKeyword, ImageUploadModel, MusicUploadModel, Member

# Register your models here.
admin.site.register(Member)
admin.site.register(SampleKeyword)
admin.site.register(ImageUploadModel)
admin.site.register(MusicUploadModel)
>>>>>>> a33a112e685bb6dc4d3439bac1b9ee0dd132d4d1
