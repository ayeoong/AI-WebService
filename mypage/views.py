from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json
from django.conf import settings
import os
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from salon.models import ArtUploadModel, ArtKeywordModel
from django.core.mail.message import EmailMessage
from .models import ArtLike
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

class UserPasswordResetView(PasswordResetView):
    template_name = 'mypage/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'mypage/password_reset_done_fail.html')
            
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'mypage/password_reset_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력

from django.core.files.storage import default_storage
from salon.utils import delete_img, delete_mus 

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'mypage/signup.html', {'form':form})


def check_id(request):
    try:
        user = User.objects.get(username=request.GET['username'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        'data' : "not exist" if user is None else "exist"
    }
    print(result)
    return JsonResponse(result)


def check_email(request):
    # subject = "DALLE에 가입하신 것을 환영합니다."
    # from_email = "dalle@gmail.com"
    # email_ok = False
    try:
        email_addr = request.GET['email']
        user = User.objects.get(email=email_addr)
    except Exception as e:
        user = None
        # to = [email_addr]
        # message = "DALLE로 바로가기"
        # email_ok =  EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
    
    result = {
        'result':'success',
        'data' : "not exist" if user is None else "exist",
        # 'email_ok' : email_ok
    }
    print(result)
    return JsonResponse(result)


# 로그인 # auth
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'mypage/login.html', {'form': form})


# 로그아웃 # auth
def logout(request):
    auth.logout(request)
    return redirect('index')

def send_email(request):
    subject = "message2"
    to = ["ohns1994@gmail.com"]
    from_email = "ohns1994@gmail.com"
    message = "메지시 테스트22"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
    return render(request, 'mypage/send_email.html')

### user name으로 구현
# 타인 접속 or 로그인 하지 않았을 때, opage.html 화면 보여줌
# current_user 현재 로그인한 유저, exist_user = 존재하는 유저 네임
def mypage(request, user_name, kind):
    current_user = request.user
    print(user_name)
    try:
        exist_user = User.objects.get(username=user_name)

        if kind == 'image':
            images = ArtUploadModel.objects.filter(user=exist_user, kind=1).order_by('-uploaded_at')
            if current_user.is_authenticated:
                likeset = ArtLike.objects.filter(art__user=exist_user, art__kind=1).filter(user=current_user)
                likeset = [like.art for like in likeset]
                print( '==========likeset :', likeset ) 

                image_likes = []
                for img in images:
                    if img in likeset:
                        image_likes.append(True)  # find like
                    else:
                        image_likes.append(False) # not like img
            else:
                image_likes = []
                for img in images:
                    image_likes.append(False)
            context = {'userid':exist_user.username, 'images':zip(images, image_likes)}
            print(context)
            return render(request, 'mypage/mypage.html', context)

        elif kind == 'music':
            musics = ArtUploadModel.objects.filter(user=exist_user, kind=2).order_by('-uploaded_at')
            if current_user.is_authenticated:
                likeset = ArtLike.objects.filter(art__user=exist_user, art__kind=2).filter(user=current_user)
                likeset = [like.art for like in likeset]
                print( '==========likeset :', likeset ) 

                music_likes = []
                for mus in musics:
                    if mus in likeset:
                        music_likes.append(True)  # find like
                    else:
                        music_likes.append(False) # not like img
            else:
                music_likes = []
                for mus in musics:
                    music_likes.append(False)

            context = {'userid':exist_user.username, 'musics':zip(musics, music_likes)}
            print(context)
            return render(request, 'mypage/mypage_music.html', context)
        else:
            return HttpResponse("error 405")
    except Exception as e:
        # exist_user = None
        print(e)
        return HttpResponse("error 404")
    

def delete_item(request, user_name):
    json_data = json.loads( request.body )
    art_id = json_data['del_item']
    del_conf = json_data['del_conf']
    if del_conf:
        try:
            del_item = ArtUploadModel.objects.get(pk=art_id)
            print(del_item)

            # media/images 폴더 안의 이미지 삭제
            filename = del_item.filename
            thumbnail = del_item.thumbnail
            print(filename, thumbnail)

            delete_img(filename)
            delete_img(thumbnail)

            ArtLike.objects.filter(art=del_item).delete()
            ArtKeywordModel.objects.filter(art=del_item).delete()

            del_item.delete()
            print("deleted")
            data = {'result':'successful'}
        except Exception as e:
            print(e)
            print("not deleted")
            data = {'result':'failed'}
    return JsonResponse(data)


def setting(request):
    return render(request, 'mypage/setting.html', {})


def find_id(request):
    subject = "DALLE에 가입하신 정보입니다."
    from_email = "dalle@gmail.com"
    error_msg = []
    email_ok = False
    if request.method == "POST":
        signed_email = request.POST.get('signed-email')
        try:
            user_id = User.objects.get(email=signed_email).username
            to = [signed_email]
            message = "DALLE에 가입하신 아이디는 [ " + user_id + " ] 입니다."
            email_ok =  EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        except:
            error_msg = ["이메일이 바르게 입력되지 않았거나 가입된 정보가 없습니다."]

    return render(request, 'mypage/find_id.html', {'error_msg':error_msg, 'email_ok':email_ok})



@csrf_exempt
def art_like(request):
    if request.method == 'POST':
        current_user = request.user; print('==========', current_user)
        json_data = json.loads( request.body )
        print(json_data)
        # username = json_data['username']
        art_id = json_data['artid']

        # user = User.objects.get(username=username)
        art = ArtUploadModel.objects.get(id=art_id)
        print(current_user, art)

        is_like = False
        artlikes = ArtLike.objects.filter(user=current_user, art=art)
        if len(artlikes) <= 0:
            ArtLike(user=current_user, art=art).save()
            is_like = True
        else:
            artlikes[0].delete()

        like_count = ArtLike.objects.filter(art=art).count()
        art.like_count = like_count
        art.save()
        print( like_count )

        data = {'result':'successful', 'like_count': like_count, 'is_like':is_like}
        print(data)
        return JsonResponse(data)
    
    data = {'result':'kwang'}
    return JsonResponse(data)


