import json
from django.http import JsonResponse
from django.shortcuts import render
# from .dalle import dalle
from . import music
from mypage.models import Member
from salon.models import ImageUploadModel, KeywordModel, MusicUploadModel
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# import MinDalle
# model = MinDalle(is_mega=True, is_reusable=True)


def index(request):
    return render(request, 'salon/index.html', {})

def main(request):
    return render(request, 'salon/main.html')


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
        #music_file = music.generateMusic()
        music_file = 'MuseGAN'
    # 이미지 파일이 나온다.
    # img = model.generate_image(text, 7, 1) 이곳에 모델 연결
    img = 'img'
    img_file =  text + '.png'
    # img = Image.open('./media/a.png')
    # img.save('./media/' + img_file, 'png')
    #토크나이즈 part
    only_english = re.sub('[^a-zA-Z]', ' ', text)   # 영어만 남기기
    only_english_lower = only_english.lower()       # 대문자 -> 소
    word_tokens =  nltk.word_tokenize(only_english_lower)   # 토큰화
    tokens_pos = nltk.pos_tag(word_tokens)          # 품사 분류
    
    # 명사만 뽑기
    NN_words = [word for word, pos in tokens_pos if 'NN' in pos]

    # 원형 추출S
    wlem = WordNetLemmatizer()
    lemmatized_words = []
    for word in NN_words:
        new_word = wlem.lemmatize(word)
        lemmatized_words.append(new_word)

    # 불용어 제거 - stopwords_list 에 따로 추가 가능
    stopwords_list = set(stopwords.words('english'))
    no_stops = [word for word in lemmatized_words if not word in stopwords_list]
    context = {'text': text, 
                'img':img, 
                "music_file":music_file, 
                "img_file":img_file,
                "tags":no_stops,
                }

    return render(request, 'salon/result.html', context)


def save_result(request):
    if request.method == 'POST':
        # member_id = request.session.get('user') # request.POST.get("member_id")
        # member_id = request.session['user'] # dict로 id 키값을 가져옴
        user = request.user
        selected = request.POST.getlist("selected")
        for filepath in selected:
            if 'mid' == filepath[-3:]:
                musicfile = MusicUploadModel(user=user, name="music", filename=filepath)
                musicfile.save()
            else:
                imgfile = ImageUploadModel(user=user, name="photo", filename=filepath)
                imgfile.save()
        return render(request, 'salon/save_result.html', {'files':selected})
    
    return render(request, 'salon/save_result.html', {})

def result_favorite(request):
    if request.method == 'POST':
        # user_id = request.session.get('user')
        # user = Member.objects.get(id=user_id)
        user = request.user
        json_data = json.loads( request.body )
        favorite = json_data['aa'] # favorite = str( json_data['aa'] ) or # models.py: CharField -> IntegerField 
    

        print("=============================", user.username, favorite)


        # 데이터타입 체크 # if type(favorite) is int
        if isinstance(favorite, int):
            global fv
            fv = str(favorite)
            print("result_code's dtype: ", type(fv))
            for favorite in fv:
                musicfile = MusicUploadModel(user=user, result_favorite=favorite)
                musicfile.save()
                imgfile = ImageUploadModel(user=user, result_favorite=favorite)
                imgfile.save()
        else:
            print("result_code's dtype: ", type(favorite))
            for favorite in favorite:
                musicfile = MusicUploadModel(user=user, result_favorite=favorite)
                musicfile.save()
                imgfile = ImageUploadModel(user=user, result_favorite=favorite)
                imgfile.save()

        # 데이터타입 체크 if문이 없을 때 사용
        # for favorite in favorite:
        #     musicfile = MusicUploadModel(user=user, result_favorite=favorite)
        #     #musicfile.save()
        #     imgfile = ImageUploadModel(user=user, result_favorite=favorite)
        #     #imgfile.save()
        
        data = {'result':'successful', 'result_code': favorite}
        return JsonResponse(data)
    else:
        data = {'result':'kwang'}
        return JsonResponse(data)
