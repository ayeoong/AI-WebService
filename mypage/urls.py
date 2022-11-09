from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mypage import views
from django.urls import path, include

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage, name='mypage'),
    
    
    
    
    
    path('', views.mypage, name='month'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
