from django.contrib import admin
from .models import SampleKeyword, ImageUploadModel, MusicUploadModel, Member

# Register your models here.
admin.site.register(Member)
admin.site.register(SampleKeyword)
admin.site.register(ImageUploadModel)
admin.site.register(MusicUploadModel)