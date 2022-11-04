from django.shortcuts import render
# from .dalle import dalle
from . import music
from django.contrib import auth
from mypage.models import Member
from salon.models import ImageUploadModel, MusicUploadModel, KeywordModel
# import MinDalle
# model = MinDalle(is_mega=True, is_reusable=True)
import re
import nltk
from nltk.corpus import stopwords


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
        music_file = 'MuseNet-Composition.mid'
    # 이미지 파일이 나온다.
    # img = model.generate_image(text, 7, 1) 이곳에 모델 연결
    img = 'img'
    img_file =  text + '.jpg'
    # img = Image.open('./media/a.png')
    # img.save('./media/' + img_file, 'png')

    # 텍스트 -> 태그화 리스트
    only_english = re.sub('[^a-zA-Z]', ' ', text)   # 영어만 남기기
    no_capitals = only_english.lower().split()      # 대문자 -> 소
    stops = set(stopwords.words('english'))         # 불용어 제거
    no_stops = [word for word in no_capitals if not word in stops]

    stemmer = nltk.stem.SnowballStemmer('english')  # 어간 추출
    tags = [stemmer.stem(word) for word in no_stops]


    context = {'text': text, 
                'img':img, 
                "music_file":music_file, 
                "img_file":img_file,
                "tags":tags}

    request.session['test_keyword'] = context

    return render(request, 'salon/result.html', context)


def save_result(request):
    context = request.session['test_keyword']
    keywords = context['tags']
    for keyword in keywords:
        try:
            exist_word = KeywordModel.objects.get(word=keyword)
            exist_word.input_num += 1
            exist_word.save()
        except:
            word = KeywordModel(word=keyword)
            word.input_num += 1
            word.save()
    if request.method == 'POST':
        user = auth.get_user(request)
        selected = request.POST.getlist("selected")
        text = request.POST.get("input_text")
 
        for filepath in selected:
            # 유저 정보와 같이 저장 필요
            if 'mid' == filepath[-3:]:
                musicfile = MusicUploadModel(user=user, name="music", filename=filepath, input_text=text)
                musicfile.save()
            else:
                imgfile = ImageUploadModel(user=user, name="photo", filename=filepath, input_text=text)
                imgfile.save()
        return render(request, 'salon/save_result.html', {'files':selected})
    
    print("=============================", keywords)
    return render(request, 'salon/save_result.html', {})

