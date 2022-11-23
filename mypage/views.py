from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
# from django.contrib.auth.hashers import check_password
from .models import Member
from salon.models import ArtUploadModel, ArtKeywordModel, KeywordModel
from django.core.mail.message import EmailMessage
import smtplib
import json
from email.mime.text import MIMEText
from .models import ArtLike

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
        # if request.POST['password1'] == request.POST['password2']:
        #     user = User.objects.create_user(
    	# 		username=request.POST['username'],
    	# 		password=request.POST['password1'],
    	# 		email=request.POST['email'],
        #     )
        #     user.save()
            return redirect('login')
        # return render(request, 'mypage/signup.html')

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
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : "not exist" if user is None else "exist"
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
# current_user 현재 사용하고 있는 유저, exist_user = 존재하는 유저 네임
def mypage(request, user_name):
    current_user = request.user
    print(user_name)
    try:
        exist_user = User.objects.get(username=user_name)
        images = ArtUploadModel.objects.filter(user=exist_user, kind=1)
        context = {'userid':exist_user.username, 'images':images}
        return render(request, 'mypage/mypage.html', context)
    
    except Exception as e:
        exist_user = None
        print(e)
        return HttpResponse("error 404")
    
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
        user = request.user; print('==========', user)

        json_data = json.loads( request.body )
        print(json_data)
        # username = json_data['username']
        art_id = json_data['artid']

        # user = User.objects.get(username=username)
        art = ArtUploadModel.objects.get(id=art_id)
        print(user, art)

        is_like = False
        artlikes = ArtLike.objects.filter(user=user, art=art)
        if len(artlikes) <= 0:
            ArtLike(user=user, art=art).save()
            is_like = True
        else:
            artlikes[0].delete()
            
        like_count = ArtLike.objects.filter(art=art).count()
        print( like_count )

        data = {'result':'successful', 'like_count': like_count, 'is_like':is_like}
        print(data)
        return JsonResponse(data)
    
    data = {'result':'kwang'}
    return JsonResponse(data)

