import os
import re
from io import BytesIO

import matplotlib.pyplot as plt
# import nltk
# import openai
import requests
from django.shortcuts import render
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
from PIL import Image
from pilkit.processors import Thumbnail

from urllib.request import urlopen
import json

from mypage.models import Member
from salon.models import ImageUploadModel, MusicUploadModel

from . import music
# from .dalle import dalle
from .models import SampleKeyword

# import MinDalle
# model = MinDalle(is_mega=True, is_reusable=True)


def index(request):
    return render(request, 'salon/index.html', {})


def home(request):
    keywords = ['가장 재미있는','추천이 많은', 'Best 작품', '회원님이 좋아할만한 작품',"Today's Favorite"]
    if SampleKeyword.objects.all():
        keywords = SampleKeyword.objects.all()
    
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

    # openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
    # openai.api_key = "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"

    text = ''
    if request.method == "POST":
        text = request.POST['title']
        # response = openai.Image.create( prompt=text,
        #                         n=1,
        #                         size="1024x1024")
        # image_url = response['data'][0]['url']
        # music_file = music.generateMusic()
    image_url = 'https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F2603884A5433A7F434'

    # urlopen을 이용
    nltk_url = 'http://127.0.0.1:5000/'     # nltk_api 배포 주소
    text_space = text.replace(' ', '%20')   # 띄어쓰기 대신 입력
    url_req = nltk_url + text_space

    f = urlopen(url_req)
    
    with f as url:
        data = json.loads(url.read().decode())['tokens']

    # # 섬네일
    # res = requests.get(image_url)
    # img_file = Image.open(BytesIO(res.content))
    # processor = Thumbnail(width=100)
    # tn_img = processor.process(img_file)
    # tn_img.save(f'salon/media/{text}_tn.png')

    # # 텍스트 -> 태그화 리스트
    # only_english = re.sub('[^a-zA-Z]', ' ', text)   # 영어만 남기기
    # only_english_lower = only_english.lower()       # 대문자 -> 소
    # word_tokens =  nltk.word_tokenize(only_english_lower)   # 토큰화
    # tokens_pos = nltk.pos_tag(word_tokens)          # 품사 분류
    
    # # 명사만 뽑기
    # NN_words = [word for word, pos in tokens_pos if 'NN' in pos]

    # # 원형 추출
    # wlem = WordNetLemmatizer()
    # lemmatized_words = []
    # for word in NN_words:
    #     new_word = wlem.lemmatize(word)
    #     lemmatized_words.append(new_word)

    # # 불용어 제거 - stopwords_list 에 따로 추가 가능
    # stopwords_list = set(stopwords.words('english'))
    # no_stops = [word for word in lemmatized_words if not word in stopwords_list]

    img='img'
    context = {'text': text, 
                'img':img, 
                'img_url':image_url,
                # "music_file":music_file, 
                # 'tn_img':tn_img,
                "tags":data}

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

