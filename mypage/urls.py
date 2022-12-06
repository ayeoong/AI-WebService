from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mypage import views
from django.contrib.auth import views as auth_views

app_name = 'mypage'

urlpatterns = [
    # path('', views.mypage, name='mypage'),  
    path('art_like/', views.art_like, name='art_like'),
    path('<str:user_name>/delete_item/', views.delete_item, name='delete_item'),
    path('<str:user_name>/<str:kind>/', views.mypage, name='mypage'), # <str:user_name> or <int:user_id>
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
