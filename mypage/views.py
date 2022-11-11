from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
# from django.contrib.auth.hashers import check_password
from .models import Member
from salon.models import ImageUploadModel, ImageKeywordModel, KeywordModel


# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
    			username=request.POST['username'],
    			password=request.POST['password1'],
    			email=request.POST['email'],
            )
            user.save()
            return redirect('login')
        return render(request, 'mypage/signup.html')

    else:
        form = UserCreationForm()
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

### user name으로 구현
# 타인 접속 or 로그인 하지 않았을 때, opage.html 화면 보여줌
# current_user 현재 사용하고 있는 유저, exist_user = 존재하는 유저 네임
def mypage(request, user_name):
    current_user = request.user
    print(user_name)
    try:
        exist_user = User.objects.get(username=user_name)
    except Exception as e:
        exist_user = None
        print(e)
        return HttpResponse("error 404")
    # return render(request, 'mypage/404.html', {})
    
    images = []

    try:
        images = ImageUploadModel.objects.filter(user=exist_user)
        print( images )
    except Exception as e:
        print(e)

    if current_user == exist_user:
        context = {'userid':current_user.username, 'images':images}
        return render(request, 'mypage/mypage.html', context)

    else:
        context = {'userid':user_name, 'images':images}
        return render(request, 'mypage/opage.html', context)
    
def setting(request):
    return render(request, 'mypage/setting.html', {})