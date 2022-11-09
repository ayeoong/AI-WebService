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
    path('result_favorite/', views.result_favorite, name='result_favorite'),
    path('result_model/', views.result_model, name='result_model'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)