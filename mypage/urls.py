from django.urls import path
from mypage import views
from django.conf import settings
from django.conf.urls.static import static
from mypage import views
from django.contrib.auth import views as auth_views

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage, name='mypage'),  
    path('<str:user_name>/', views.mypage, name='mypage'), # <str:user_name> or <int:user_id>

]
#urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
