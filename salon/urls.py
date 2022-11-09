from django.urls import path
from salon import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'salon'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('start/', views.start, name='start'),
    path('result/', views.result, name='result'),
    path('save_result/', views.save_result, name='save_result'),
    path('search/', views.search, name='search'),
    path('img_m/', views.si, name='img_m'),
    path('img_m1/', views.sia, name='siamonth'),
    path('img_m2/', views.num_format, name='num_f'),
    path('img_m3/', views.HelloWork, name='HW'),
    path('myprofile/upload/', views.upload,name="upload"),
    path('salon/static/salon/images', views.upload_create,name="upload_create"),
    path('myprofile/profile/', views.profile,name="profile"),
    path('myprofile/profile/', views.im, name="im"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)