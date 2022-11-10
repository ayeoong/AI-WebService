from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib import auth
from salon.models import ImageUploadModel, MusicUploadModel, KeywordModel, ImageKeywordModel, MusicKeywordModel
import os
import openai
from PIL import Image
import requests
from io import BytesIO
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import time


def index(request):
    return render(request, 'salon/index.html', {})

def main(request):
    return render(request, 'salon/main.html')


def home(request):
    keywords = ['가장 재미있는','추천이 많은', 'Best 작품', '회원님이 좋아할만한 작품', "Today's Favorite"]
    image = ImageUploadModel.objects.all()[:10]
    return render(request, 'salon/home.html', {'keywords':keywords, 'image':image})

def search(request):
    if request.method == 'POST':
        search_word = request.POST['search']
        search_result_list = KeywordModel.objects.filter(word__contains=search_word)
        search_imagekeys_list = ImageKeywordModel.objects.filter(keyword__word__contains=search_word)        
        search_img_list = [imgkey.image for imgkey in search_imagekeys_list]
        return render(request, 'salon/search.html', {'search_result_list':search_result_list, 'search_img_list':search_img_list})
    else:
        search_result_list = []
        return render(request, 'salon/search.html', {'search_result_list':search_result_list})

# 입력창
def start(request):
    return render(request, 'salon/start.html', {})

# 출력창
def result(request):
    text, image_url = image_generation(request)
    
    # music_file = '/media/musics/' + music.generateMusic()
    # image_url = 'https://ifh.cc/g/5qCAX2.jpg'
    music_file = '/media/musics/MuseNet-Composition.mid'

    # 이미지 & 섬네일 media에 저장
    res = requests.get(image_url)
    img_file = Image.open(BytesIO(res.content))
    img_file.save('media/images/'+text+'.jpg')
    img_file.thumbnail((300, 300))
    img_file.save('media/images/'+text+'_tn.jpg')


    # 텍스트 -> 태그화 리스트
    only_english = re.sub('[^a-zA-Z]', ' ', text)   # 영어만 남기기
    only_english_lower = only_english.lower()       # 대문자 -> 소
    word_tokens =  nltk.word_tokenize(only_english_lower)   # 토큰화
    tokens_pos = nltk.pos_tag(word_tokens)          # 품사 분류
    
    # 명사만 뽑기
    NN_words = [word for word, pos in tokens_pos if 'NN' in pos]

    # 원형 추출
    wlem = WordNetLemmatizer()
    lemmatized_words = []
    for word in NN_words:
        new_word = wlem.lemmatize(word)
        lemmatized_words.append(new_word)

    # 불용어 제거 - stopwords_list 에 따로 추가 가능
    stopwords_list = set(stopwords.words('english'))
    no_stops = [word for word in lemmatized_words if not word in stopwords_list]
    
    context = {'text': text, 
                'img_file':'/media/images/'+text+'.jpg', 
                "music_file":music_file, 
                # 'img_url':image_url,
                'tn_img':'/media/images/'+text+'_tn.jpg',
                "tags":no_stops,
    }

    request.session['test_keyword'] = context

    return render(request, 'salon/result.html', context)

def image_generation(request):
    openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
    openai.api_key = "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"

    text = ''
    if request.method == "POST":
        text = request.POST['title']
        response = openai.Image.create( prompt=text,
                                n=1,
                                size="1024x1024")
        image_url = response['data'][0]['url']
    return text,image_url


def save_result(request):
    context = request.session['test_keyword']
    keywords = context['tags']
    kw_model_list = []
    for keyword in keywords:
        try:
            exist_word = KeywordModel.objects.get(word=keyword)
            exist_word.input_num += 1
            exist_word.save()
            kw_model_list.append(exist_word)
        except:
            word = KeywordModel(word=keyword)
            word.input_num += 1
            word.save()
            kw_model_list.append(word)
    if request.method == 'POST':
        user = request.user
        selected = request.POST.getlist("selected")
        text = request.POST.get("input_text")
 
        for filepath in selected:
            # 유저 정보와 같이 저장 필요
            if 'mid' == filepath[-3:]:
                musicfile = MusicUploadModel(user=user, name=text+"_music", filename=filepath, input_text=text)
                musicfile.save()
                mkms = [MusicKeywordModel(music=musicfile, keyword=km) for km in kw_model_list]
                MusicKeywordModel.objects.bulk_create(mkms)
            else:
                filename = filepath.split(',')[0]
                thumbnail = filepath.split(',')[1]
                imgfile = ImageUploadModel(user=user, name=text+"_image", filename=filename, thumbnail=thumbnail, input_text=text)
                imgfile.save()
                ikms = [ImageKeywordModel(image=imgfile, keyword=km) for km in kw_model_list]
                ImageKeywordModel.objects.bulk_create(ikms)
        return render(request, 'salon/save_result.html', {'files':selected})
    
    return render(request, 'salon/save_result.html', {})

@csrf_exempt
def result_favorite(request):
    if request.method == 'POST':
        user = request.user
        json_data = json.loads( request.body )
        favorite = json_data['aa'] # favorite = str( json_data['aa'] ) or # models.py: CharField -> IntegerField 
    

        print("=============================", user.username, json_data)


        # 데이터타입 체크 # if type(favorite) is int
        if isinstance(favorite, int):
            global fv
            fv = str(favorite)
            print("result_code's dtype: ", type(fv))
            for favorite in fv:
                musicfile = MusicUploadModel(user=user, result_favorite=favorite)
                # musicfile.save()
                imgfile = ImageUploadModel(user=user, result_favorite=favorite)
                # imgfile.save()
        else:
            print("result_code's dtype: ", type(favorite))
            for favorite in favorite:
                musicfile = MusicUploadModel(user=user, result_favorite=favorite)
                # musicfile.save()
                imgfile = ImageUploadModel(user=user, result_favorite=favorite)
                # imgfile.save()

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

def result_model(request):
    json_data = json.loads( request.body )
    text = json_data['aa']
    # model process
    time.sleep(30)
    music_file = 'aa.mid' 
    img_file = 'aa.png'
    data = {'result':'successful', 'result_code': '1', 'imgfile':img_file, 'musfile':music_file}
    return JsonResponse(data)
