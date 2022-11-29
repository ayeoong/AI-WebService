from django.contrib import admin
from .models import KeywordModel, ArtKeywordModel, ArtUploadModel, AutoArtUploadModel

# Register your models here.
admin.site.register(KeywordModel)
admin.site.register(ArtUploadModel)
admin.site.register(ArtKeywordModel)

class AutoArtAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'filename', 'thumbnail', 'uploaded_at' ]

admin.site.register(AutoArtUploadModel, AutoArtAdmin)
