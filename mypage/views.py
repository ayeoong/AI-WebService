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
from django.contrib.auth import login, authenticate
# from django.contrib.auth.hashers import check_password
from .models import Member

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

# # 로그인 # Session
# def login(request):
#     if request.method == 'POST': # 사용자가 보내는 데이터와 데이터베이스의 정보 일치여부 확인
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#     # 로그인 페이지 요청
#     else:
#         form = LoginForm()
#         return render(request, 'mypage/login.html', {'form': form})


#     # 응답 데이터
#     res_date = {}

#     # 모든 값을 채우지 않았을 경우
#     if not (username and password):
#         res_date['error'] = "모든 값을 입력하세요."
#     # 모든 값을 채웠을 경우
#     else:
#         try: 
#             user = Member.objects.get(username=username) # User 테이블에서 조건에 맞는 행 추출
#             # if check_password(password, user.password): # 입력받은 password에서 DB내에 있는 password 비교
#             if password == user.password:
#                 request.session['user'] = user.id # 해당 클라이언트 Session 객체 생성 후 상태정보 저장
#                 print("===============success login---------------")
#                 return redirect('/') # 홈페이지로 이동
#             else:
#                 res_date['error'] = "비밀번호가 일치하지 않습니다."
#         except Member.DoesNotExist:
#             res_date['error'] = username + " 아이디가 없습니다."

#     # 로그인 실패 및 오류메세지와 함께 응답
#     return render(request, 'mypage/login.html', res_date)

# 로그인 Session 유지
def home(request):
    user_id = request.session.get('user')
    if user_id:
        user = Member.objects.get(id=user_id)
        return HttpResponse(f'{user} login seccess')

    return HttpResponse('Home')

# 로그아웃
def logout(request):
	
    # session_data에서 로그인 세션과 관련된 내용을 변경, 삭제
    if request.session.get('user'):
        del(request.session['user'])
	
    # 로그아웃 후 127.0.0.1:8000/ 이동   
    return redirect('/')

# user id로 url 구현하는 법
# def mypage(request, user_id):
#     user = request.user

#     result_str = f'{user_id} user={user.id}'
#     print('===========================/', result_str)

#     images = []
#     try:
#         images = ImageUploadModel.objects.filter(user=user)
#         print( images )
#     except Exception as e:
#         print(e)

#     context = {'userid':user, 'images':images}

#     if user_id == user.id:
#         return render(request, 'mypage/mypage.html', context)

#     user = User.objects.get(pk=user_id)
#     context = {'userid':user, 'images':images}
#     return render(request, 'mypage/opage.html', context) 

### user name으로 구현
def mypage(request, user_name):
    user = request.user

    result_str = f'{user_name} user={user.username}'
    print('===========================/', result_str)

    images = []
    try:
        images = ImageUploadModel.objects.filter(user=user)
        print( images )
    except Exception as e:
        print(e)

    context = {'userid':user, 'images':images}

    if user_name == user.username:
        return render(request, 'mypage/mypage.html', context)

    user = None
    try:
        user = User.objects.get(username=user_name, default=None)
    except Exception as e:
        print(e)

    context = {'userid':user, 'images':images}
    return render(request, 'mypage/opage.html', context)

def mypage(request):
    return render(request, 'mypage/mypage.html', {})

def setting(request):
    return render(request, 'mypage/setting.html', {})