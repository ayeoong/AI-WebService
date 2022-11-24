from django.shortcuts import render
import json
from urllib.request import urlopen
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from salon.models import KeywordModel, ArtKeywordModel, ArtUploadModel
import openai
from PIL import Image
import requests
from io import BytesIO
import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
from django.conf import settings
import time
from . import music
from salon.utils import uuid_name_upload_to
from django.core.files.storage import default_storage
from googletrans import Translator

if settings.DEV_MODE or settings.TEST_MODE:
    img_path = '/media/images/'
    mus_path = '/media/musics/'
else:
    img_path = 'https://storage.googleapis.com/dall-e-2-contents/images/'
    mus_path = 'https://storage.googleapis.com/dall-e-2-contents/musics/'

def home(request):
    return render(request, 'salon/index.html', {})

def main(request):
    return render(request, 'salon/main.html')


def index(request):
    keywords = ['가장 많이 검색된 키워드', 'Best 작품']
    best_kw_list = KeywordModel.objects.all().order_by('-input_num')[:10]
    art_kw_list = []
    for best_kw in best_kw_list:
        art_kw_list.extend(ArtKeywordModel.objects.filter(keyword=best_kw))
    print(art_kw_list)
    image = set([imgkey.art for imgkey in art_kw_list])
    return render(request, 'salon/home.html', {'keywords':keywords, 'image':image})

def search(request):
    if request.method == 'POST':
        search_word = request.POST['search']
        search_token_list = search_word.split(' ')
        search_user_list=[]
        search_result_list=[]
        search_imagekeys_list=[ArtKeywordModel]
        for search_token in search_token_list:
            search_user_list.extend(User.objects.filter(username__contains=search_token))
            search_result_list.extend(KeywordModel.objects.filter(word__contains=search_token))
            search_imagekeys_list.extend(ArtKeywordModel.objects.filter(keyword__word__contains=search_token))
        del search_imagekeys_list[0]
        search_img_list = [imgkey.art for imgkey in search_imagekeys_list]
        search_img_set = set(search_img_list)
        context = {
            'search_user_list':search_user_list,
            'search_result_list':search_result_list, 
            'search_img_set':search_img_set,
        }
        return render(request, 'salon/search.html', context)
    else:
        return render(request, 'salon/search.html', {})

def image_generation(text): #실제 배포용 말고는 더미 이미지 사용
    if settings.REAL_LIVE_MODE:
        openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
        openai.api_key = "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"

        response = openai.Image.create( prompt=text,
                                n=1,
                                size="1024x1024")
        image_url = response['data'][0]['url']
    else:
        time.sleep(5)
        image_url = 'https://ifh.cc/g/5qCAX2.jpg'        
    return image_url

def music_generateMusic():
    if settings.REAL_LIVE_MODE:
       music.generateMusic() #실제 배포용만 음악 생성
    else:
        mus_filename = 'MuseNet-Composition.mid'
    return mus_filename

def translate(prompt):
    translator = Translator()
    which_lang = translator.detect(prompt).lang
    if which_lang != 'en':
        return translator.translate(text=prompt, dest='en', src='auto').text
    else:
        return prompt



# 입력창
def start(request):
    return render(request, 'salon/start.html', {})

# 모델 호출 함수
def result_model(request):
    json_data = json.loads( request.body )

    text = translate(json_data['text'])

    image_url = image_generation(text) #image_generation(text) # https://~~~.jpg 형식
    
    if settings.REAL_LIVE_MODE:
        img_filename = uuid_name_upload_to(None, image_url) + '.jpg'
    else:
        img_filename = uuid_name_upload_to(None, image_url)

    res = requests.get(image_url)
    _, img_tn_file = save_img_and_thumbnail(res.content, img_filename)



    music_file = music_generateMusic() #generateMusic() # '~~~.mid' 형식
    #mus_filename = uuid_name_upload_to(None, music_file)
    mus_filename = music_file
    img_filename = img_path + img_filename
    img_tn_file = img_path + img_tn_file
    mus_filename = mus_path + mus_filename
    data = {'result':'successful', 'result_code': '1', 'img_file':img_filename, 'img_tn_file':img_tn_file, 'mus_file':mus_filename}
    return JsonResponse(data)


def save_img_and_thumbnail(content, img_filename):
    img_tn_filename = "_tn.".join(img_filename.split('.')) # 섬네일명: 이미지파일명_tn.jpg 

    img_file = Image.open(BytesIO(content))
    save_img(img_file, img_filename)

    img_file = Image.open(BytesIO(content))
    img_file.thumbnail((300, 300))
    save_img(img_file, img_tn_filename)  # 섬네일저장

    return img_filename, img_tn_filename


def save_img(image_file, filename):
    if settings.DEV_MODE or settings.TEST_MODE:
        img_storage_path = img_path #setting.media_images
        img_filepath = img_storage_path + filename
        image_file.save(img_filepath, 'PNG')
    else:
        with BytesIO() as output:  
            image_file.save(output, 'PNG')
            with default_storage.open('/images/' + filename, 'w') as f:
                f.write(output.getvalue())

#공사중
def save_mus(music_file, filename):
    if settings.DEV_MODE or settings.TEST_MODE:
        mus_filepath = mus_path + filename

    else:
        with BytesIO() as output:  
            music.save(output, 'WAV')
            with default_storage.open('/musics/' + filename, 'w') as f:
                f.write(output.getvalue())
#midi파일이 오면 컨버젼해서 저장


# 출력창
def result(request):
    text = translate(request.POST.get('input_text'))
    mus_filename = request.POST.get('mus_file')
    img_filename = request.POST.get('img_file')
    img_tn_filename = request.POST.get('img_tn_file')

    # 텍스트 -> 태그화 리스트
    no_stops = get_taglist(text)
    
    context = {'text': text, 
                'img_file': img_filename, 
                "music_file":mus_filename, 
                # 'img_url':image_url,
                'img_tn_file':img_tn_filename,
                "tags":no_stops,
    }

    request.session['test_keyword'] = context

    return render(request, 'salon/result.html', context)

def get_taglist(text):
    nltk_url = 'https://silken-oxygen-369215.de.r.appspot.com/'   # 배포 주소
    text_spapce = text.replace(' ', '%20')
    url_req = nltk_url + text_spapce

    f = urlopen(url_req)
    with f as url:
        data = json.loads(url.read().decode())['tokens']
    return data


def save_result(request):
    context = request.session['test_keyword']
    keywords = context['tags']
    keyword_list = []
    art_dict = {'jpg':'1', 'mid':'2', 'both':'3'}
    for keyword in keywords:
        try:
            exist_word = KeywordModel.objects.get(word=keyword)
            exist_word.input_num += 1
            exist_word.save()
            keyword_list.append(exist_word)
        except:
            word = KeywordModel(word=keyword)
            word.input_num += 1
            word.save()
            keyword_list.append(word)
    if request.method == 'POST':
        user = request.user
        selected = request.POST.getlist("selected")
        text = request.POST.get("input_text")
        favorite = request.POST.get("favorite")
        thumbnail = context['img_tn_file']
 
        for filepath in selected:
            art = ArtUploadModel(kind=art_dict[filepath[-3:]], user=user, name=text, filename=filepath, input_text=text)
            art.save()
            print(favorite)
            if 'mid' == filepath[-3:]:
                print("this1")
                if favorite == 'mid' or favorite == 'both':
                    print("this2")
                    art.result_favorite = '1'
                    art.save()
            else:
                print("this3")
                art.thumbnail = thumbnail
                art.save()
                if favorite == 'jpg' or favorite == 'both':
                    print("this4")
                    art.result_favorite = '1'
                    art.save()

            akms = [ArtKeywordModel(art=art, keyword=km) for km in keyword_list]
            ArtKeywordModel.objects.bulk_create(akms)
        return render(request, 'salon/save_result.html', {'files':selected})
    
    return render(request, 'salon/save_result.html', {})
