from django.shortcuts import render
# from .dalle import dalle
from . import music
from mypage.models import Member
from salon.models import ImageUploadModel, MusicUploadModel, KeywordModel, Img_Mon
# import MinDalle
# model = MinDalle(is_mega=True, is_reusable=True)
import re
import nltk
from nltk.corpus import stopwords
from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    return render(request, 'salon/index.html', {})


def home(request):
    keywords = ['가장 재미있는','추천이 많은', 'Best 작품', '회원님이 좋아할만한 작품', "Today's Favorite"]   
    return render(request, 'salon/home.html', {'keywords':keywords})

def search(request):
    if request.method == 'POST':
        search_word = request.POST['search']
        search_result_list = KeywordModel.objects.filter(word__contains=search_word)
        return render(request, 'salon/search.html', {'search_result_list':search_result_list})
    else:
        search_result_list = []
        return render(request, 'salon/search.html', {'search_result_list':search_result_list})

# 입력창
def start(request):
    return render(request, 'salon/start.html', {})

# 출력창
def result(request):
    text = ''
    if request.method == "POST":
        text = request.POST['title']
        # music_file = music.generateMusic()
        music_file = 'MuseGAN'
    # 이미지 파일이 나온다.
    # img = model.generate_image(text, 7, 1) 이곳에 모델 연결
    img = 'img'
    img_file =  text + '.png'
    # img = Image.open('./media/a.png')
    # img.save('./media/' + img_file, 'png')

    # 텍스트 -> 태그화 리스트
    only_english = re.sub('[^a-zA-Z]', ' ', text)   # 영어만 남기기
    no_capitals = only_english.lower().split()      # 대문자 -> 소
    stops = set(stopwords.words('english'))         # 불용어 제거
    no_stops = [word for word in no_capitals if not word in stops]

    stemmer = nltk.stem.SnowballStemmer('english')  # 어간 추출
    tags = [stemmer.stem(word) for word in no_stops]


    # 유저 정보와 같이 저장 필요
    for tag in tags:
        try:
            exist_word = KeywordModel.objects.get(word=tag)
            exist_word.input_num += 1
            exist_word.save()
        except:
            word = KeywordModel(word=tag)
            word.input_num += 1
            word.save()

    context = {'text': text, 
                'img':img, 
                "music_file":music_file, 
                "img_file":img_file,
                "tags":tags}

    return render(request, 'salon/result.html', context)


def save_result(request):
    if request.method == 'POST':
        # member_id = request.session.get('user') # request.POST.get("member_id")
        member_id = request.session['user'] # dict로 id 키값을 가져옴
        selected = request.POST.getlist("selected")
        print("=============================", member_id, selected)
        user = Member.objects.get(id=member_id) # id=member_id
        for filepath in selected:
            if 'mid' == filepath[-3:]:
                musicfile = MusicUploadModel(user=user, title="music", file=filepath)
                musicfile.save()
            else:
                imgfile = ImageUploadModel(user=user, description="photo", document=filepath)
                imgfile.save()
        return render(request, 'salon/save_result.html', {'files':selected})
    
    return render(request, 'salon/save_result.html', {})
#DB에서 이미지업로드모델파일 가져오기시도. 
def si(request):
    save_img_in_admin_km=[ImageUploadModel]
    
    print("Hello")
    save_img_in_admin_km.save()
    return render(request, 'salon/img_m.html', {'save_img_in_admin_km':save_img_in_admin_km})
#test_img_month
def sia(request):
    siamonth=['link=salon/img_month/*']
    num=3
    return render(request, save_result, 'salon/img_m.html', {'siamonth':siamonth})

#.format 및 HttpResponse시도
def num_format(request):
    num_test="month{{img_month.id}}".__format__
    return HttpResponse(request,"num_1=숫자",num_test)
# Hello World 출력시도
def HelloWork(request):
    return HttpResponse('Hello world')
# upload.
def upload(request):
    return render(request, 'salon/img_m.html')

# create
def upload_create(request):
    form = Img_Mon()
    form.title=request.POST['title']
    try:
        form.image=request.FILES['image']
    except: #이미지가 없어도 지나가도록
        pass
    form.save()
    return redirect('/salon/static/salon/images') 

#결과화면 보이는 img_m.html
def profile(request):
    profile = Img_Mon.objects.all().order_by('pub_date') #  날짜별 정렬 
    #profile = Img_Mon.objects.filter(user=login_user).order_by('pub_date') #  날짜별 정렬 
     
    return render(request, 'test.html',{'profile':profile})  

def im(request):
    o = Img_Mon.objects.all().order_by('-pub_date')
    
    return render(request, 'test.html', {'o':o})



