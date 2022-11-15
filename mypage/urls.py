from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mypage import views
from django.contrib.auth import views as auth_views

app_name = 'mypage'

urlpatterns = [
    path('', views.mypage, name='mypage'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('send_email/', views.send_email, name='send_email'),    
    path('<str:user_name>/', views.mypage, name='mypage'), # <str:user_name> or <int:user_id>

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
