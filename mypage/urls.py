from django.urls import path
from mypage import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

app_name = 'mypage'

urlpatterns = [
    path('<str:user_name>/', views.mypage, name='mypage'), # <str:user_name> or <int:user_id>
    path('', views.mypage, name='mypage'),
    

]
#urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
