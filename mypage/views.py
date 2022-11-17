from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from .forms import UserForm
from django.contrib.auth.models import User
from .forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
# from django.contrib.auth.hashers import check_password
from .models import Member
from salon.models import ArtUploadModel, ArtKeywordModel
from django.core.mail.message import EmailMessage
import smtplib
from email.mime.text import MIMEText

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


def art_like(request, pk):

    if request.user.is_authenticated:
        like = get_object_or_404(like, pk=pk)

        if like.like_users.filter(pk=request.pk):
            like.like_users.remove(request.user)
        
        else:
            like.like_users.add(request.user)
            return render(request, 'mypage/mypage.html', {})