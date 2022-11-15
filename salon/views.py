from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
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
from . import music
from salon.models import ImageUploadModel, MusicUploadModel
from salon.utils import uuid_name_upload_to
from salon.music import generateMusic


def home(request):
    return render(request, 'salon/index.html', {})

def main(request):
    return render(request, 'salon/main.html')


def index(request):
    keywords = ['가장 재미있는','추천이 많은', 'Best 작품', '회원님이 좋아할만한 작품', "Today's Favorite"]
    image = ImageUploadModel.objects.all()[:10]
    return render(request, 'salon/home.html', {'keywords':keywords, 'image':image})

def search(request):
    if request.method == 'POST':
        search_word = request.POST['search']
        search_token_list = search_word.split(' ')
        search_user_list=[]
        search_result_list=[]
        search_imagekeys_list=[ImageKeywordModel]
        for search_token in search_token_list:
            search_user_list.extend(User.objects.filter(username__contains=search_token))
            search_result_list.extend(KeywordModel.objects.filter(word__contains=search_token))
            search_imagekeys_list.extend(ImageKeywordModel.objects.filter(keyword__word__contains=search_token))
        del search_imagekeys_list[0]
        search_img_list = [imgkey.image for imgkey in search_imagekeys_list]
        search_img_set = set(search_img_list)
        context = {
            'search_user_list':search_user_list,
            'search_result_list':search_result_list, 
            'search_img_set':search_img_set,
        }
        return render(request, 'salon/search.html', context)
    else:
        return render(request, 'salon/search.html', {})

def image_generation(text):
    openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
    openai.api_key = "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"

    response = openai.Image.create( prompt=text,
                            n=1,
                            size="1024x1024")
    image_url = response['data'][0]['url']
    return image_url

def image_generation_beta(text):
    image_url = 'https://ifh.cc/g/5qCAX2.jpg'
    return image_url

def generateMusic_beta():
    mus_filename = 'MuseNet-Composition.mid'
    return mus_filename


# 입력창
def start(request):
    return render(request, 'salon/start.html', {})

# 모델 호출 함수
def result_model(request):
    json_data = json.loads( request.body )
    text = json_data['text']

    # mock model process
    time.sleep(5)

    image_url = image_generation_beta(text) #image_generation(text) # https://~~~.jpg 형식
    img_filename = uuid_name_upload_to(None, image_url)

    res = requests.get(image_url)
    _, img_tn_file = save_img_and_thumbnail(res.content, img_filename)


    music_file = generateMusic_beta() #generateMusic() # '~~~.mid' 형식
    # mus_filename = uuid_name_upload_to(None, music_file)
    mus_filename = music_file

    img_filename = '/media/images/' + img_filename
    img_tn_file = '/media/images/' + img_tn_file
    mus_filename = '/media/musics/' + mus_filename

    data = {'result':'successful', 'result_code': '1', 'img_file':img_filename, 'img_tn_file':img_tn_file, 'mus_file':mus_filename}
    print('====================', data)
    return JsonResponse(data)


def save_img_and_thumbnail(content, img_filename):
    img_tn_filename = "_tn.".join(img_filename.split('.')) # 섬네일명: 이미지파일명_tn.jpg 

    img_file = Image.open(BytesIO(content))
    save_img(img_file, img_filename)

    img_file.thumbnail((300, 300))
    save_img(img_file, img_tn_filename)  # 섬네일저장

    return img_filename, img_tn_filename


def save_img(image, filename):
    img_storage_path = 'media/images/' #setting.media_images
    img_filepath = img_storage_path + filename
    image.save(img_filepath, 'PNG')


# 출력창
def result(request):
    text = request.POST.get('input_text')
    mus_filename = request.POST.get('mus_file')
    img_filename = request.POST.get('img_file')
    img_tn_filename = request.POST.get('img_tn_file')

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
                'img_file':img_filename, 
                "music_file":mus_filename, 
                # 'img_url':image_url,
                'img_tn_file':img_tn_filename,
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
        user = request.user
        selected = request.POST.getlist("selected")
        text = request.POST.get("input_text")
        favorite = request.POST.get("favorite")

        print('=================>', favorite)
 
        for filepath in selected:
            # 유저 정보와 같이 저장 필요
            if 'mid' == filepath[-3:]:
                # musicfile = MusicUploadModel(user=user, name=text+"_music", filename=filepath, input_text=text)
                musicfile = MusicUploadModel(user=user, name=text+"_music", filename=filepath, input_text=text, result_favorite=favorite)
                musicfile.save()
                print("-------------------->", text, filepath, favorite)
                # MusicKeywordModel(music=musicfile, keyword=keyword).save()
            else:
                # filename = filepath.split(' ')[0]
                # thumbnail = filepath.split(' ')[1]
                filename = context['img_file']
                thumbnail = context['img_tn_file']
                # imgfile = ImageUploadModel(user=user, name=text+"_image", filename=filename, thumbnail=thumbnail, input_text=text)
                imgfile = ImageUploadModel(user=user, name=text, filename=filename, thumbnail=thumbnail, input_text=text, result_favorite=favorite)
                imgfile.save()
                print("-------------------->", text, filename, thumbnail, favorite)
        return render(request, 'salon/save_result.html', {'files':selected})
    
    return render(request, 'salon/save_result.html', {})
