from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mypage import views

app_name = 'mypage'

urlpatterns = [
    path('<str:user_name>/', views.mypage, name='mypage'), # <str:user_name> or <int:user_id>
    path('', views.mypage, name='mypage'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
