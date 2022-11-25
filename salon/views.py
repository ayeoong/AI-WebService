from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from salon.models import KeywordModel, ArtKeywordModel, ArtUploadModel, AutoArtUploadModel
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
from salon.utils import uuid_name_upload_to
from salon.music import generateMusic
from googletrans import Translator
from datetime import timedelta
from django.utils import timezone


def home(request):
    return render(request, 'salon/index.html', {})

def main(request):
    return render(request, 'salon/main.html')


def index(request):
    keywords = ['가장 많이 검색된 키워드', 'Best 작품']
    best_kw_list = KeywordModel.objects.all().order_by('-input_num')[:10]
    art_kw_img_list = []
    art_kw_mus_list = []
    for best_kw in best_kw_list:
        art_kw_img_list.extend(ArtKeywordModel.objects.filter(keyword=best_kw).filter(art__kind=1))
        art_kw_mus_list.extend(ArtKeywordModel.objects.filter(keyword=best_kw).filter(art__kind=2))
    print(art_kw_img_list, art_kw_mus_list)
    images = set([artkey.art for artkey in art_kw_img_list])
    musics = set([artkey.art for artkey in art_kw_mus_list])
    return render(request, 'salon/home.html', {'keywords':keywords, 'arts':zip(images, musics)})

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

def image_generation(text):
    openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
    openai.api_key = "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"

    response = openai.Image.create( prompt=text,
                            n=1,
                            size="1024x1024")
    image_url = response['data'][0]['url']
    return image_url

def image_generation_beta(text):
    time.sleep(5)
    image_url = 'https://ifh.cc/g/5qCAX2.jpg'
    return image_url

def music_generateMusic_beta():
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

    image_url = image_generation_beta(text) #image_generation(text) # https://~~~.jpg 형식
    img_filename = uuid_name_upload_to(None, image_url)

    res = requests.get(image_url)
    _, img_tn_file = save_img_and_thumbnail(res.content, img_filename)

    mus_filename = generateMusic()
    # music_file = music_generateMusic_beta() #generateMusic() # '~~~.mid' 형식

    data = {'result':'successful', 'result_code': '1', 'img_file':img_filename, 'img_tn_file':img_tn_file, 'mus_file':mus_filename}
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
    if request.session.get('auto_save'):
        context = request.session['test_keyword']
        return render(request, 'salon/result.html', context)
    
    text = translate(request.POST.get('input_text'))
    mus_filename = request.POST.get('mus_file')
    img_filename = request.POST.get('img_file')
    img_tn_filename = request.POST.get('img_tn_file')

    # 텍스트 -> 태그화 리스트
    no_stops = get_taglist(text)

    auto_save_art_id_list = []

    art = AutoArtUploadModel(kind=1, name=text, filename=img_filename, thumbnail=img_tn_filename, input_text=text)
    art.save()
    auto_save_art_id_list.append(art.id)

    art = AutoArtUploadModel(kind=2, name=text+"_music", filename=mus_filename, input_text=text)
    art.save()
    auto_save_art_id_list.append(art.id)
    print( auto_save_art_id_list )

    context = {'text': text, 
                'img_file':img_filename, 
                "music_file":mus_filename, 
                'img_tn_file':img_tn_filename,
                "tags":no_stops,
    }

    request.session['test_keyword'] = context
    request.session['auto_save'] = auto_save_art_id_list

    return render(request, 'salon/result.html', context)

def get_taglist(text):
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
    return no_stops


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

        # fav_ind_img = {}
        # fav_ind_img['1'] = "1"
        # fav_ind_img['2'] = "0"
        # fav_ind_img['3'] = "3"

        # fav_ind_mus = {}
        # fav_ind_mus['1'] = "0"
        # fav_ind_mus['2'] = "2"
        # fav_ind_mus['3'] = "3"
 
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


def delete_autoart(self):
    minutes = 1
    queryset = AutoArtUploadModel.objects.filter(uploaded_at__lte=(timezone.now() - timedelta(minutes=minutes)))
    delete_filename = list(queryset.values_list('filename'))
    delete_thumbnail = list(queryset.values_list('thumbnail'))
    queryset.delete() # DB 삭제

    delete_filename = [file for (file,) in delete_filename]
    delete_thumbnail = [tn for (tn,) in delete_thumbnail]
    delete_filename.extend(delete_thumbnail)
    for file in delete_filename:

        if file[-3:] == 'jpg':
            images_path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'images'), file)
            print(images_path)
            os.remove(images_path) # 파일 삭제

        elif file[-3:] == 'mid':
            musics_path = os.path.join(os.path.join(settings.MEDIA_ROOT, 'musics'), file) # /media/musics/MusenetComposition.mid
            print(musics_path)
            os.remove(musics_path)
    
    result = {'delete_count':len(delete_filename) + len(delete_thumbnail), 'filenames':delete_filename + delete_thumbnail}
    return JsonResponse(result, safe=False)
