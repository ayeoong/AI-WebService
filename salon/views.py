from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from salon.models import ImageUploadModel, MusicUploadModel, KeywordModel, ImageKeywordModel, MusicKeywordModel
import os
import openai
from PIL import Image
import requests
from io import BytesIO
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import time

from django.core.files.storage import default_storage
from .utils import save_storage_img
from . import music

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

# 입력창
def start(request):
    return render(request, 'salon/start.html', {})

# 출력창
def result(request):
    text, image_url = image_generation(request)
    
    # music_file = '/media/musics/' + music.generateMusic()
    music_file = '/media/musics/MuseNet-Composition.mid' #

    save_image(image_url, text)
    img_path = 'https://storage.cloud.google.com/dall-e-2-media/images/'
    
    context = {'text': text, 
                'img_file':img_path + text +'.jpg',
                "music_file":music_file, 
                'img_url':image_url,
                'tn_img':img_path + text +'_tn.jpg',
                "tags": "!!token test!!",#메모리 차지로 nltk 제외 일단 돌아가게 처리
    }

    request.session['test_keyword'] = context

    return render(request, 'salon/result.html', context)

def save_image(image_url, text):
    res = requests.get(image_url)
    img_file = Image.open(BytesIO(res.content)) #url에서 바이트를 가져와 메모리에 올림, 그걸 이미지로 open

    filename = text + '.jpg'
    save_storage_img(img_file, filename)

    img_file.thumbnail((150, 150))  
    filename = text + '_tn' + '.jpg'
    save_storage_img(img_file, filename)

def image_generation(request):
    openai.organization = "org-IHDNUM52y3No3XxvBFRpbIf5"
    openai.api_key = "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"

    text = ''
    if request.method == "POST":
        text = request.POST['title']
        # response = openai.Image.create( prompt=text, #토큰 소비로 주석처리 임시 이미지로 대체
        #                          n=1,
        #                          size="1024x1024")
        # image_url = response['data'][0]['url']
        image_url = 'https://ifh.cc/g/5qCAX2.jpg'
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
