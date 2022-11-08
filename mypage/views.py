from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
# from django.contrib.auth.hashers import check_password


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

def mypage(request):
    return render(request, 'mypage/mypage.html', {})

def setting(request):
    return render(request, 'mypage/setting.html', {})