from django.shortcuts import render
from urllib.request import urlopen
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from salon.models import KeywordModel, ArtKeywordModel, ArtUploadModel, AutoArtUploadModel
import os
import openai
from PIL import Image
import requests
from io import BytesIO
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import time
from salon.utils import uuid_name_upload_to
from salon.music import generateMusic
from googletrans import Translator
from datetime import timedelta
from django.utils import timezone




if settings.DEV_MODE or settings.TEST_MODE:
    img_path = '/media/images/'
    music_path = '/media/musics/'
else:
    img_path = 'https://storage.googleapis.com/dall-e-2-contents/images/'
    music_path = 'https://storage.googleapis.com/dall-e-2-contents/musics/'


def home(request):
    return render(request, 'salon/index.html', {})

def main(request):
    return render(request, 'salon/main.html')


def index(request):
    keywords = ['가장 많이 검색된 키워드', 'Best 작품']
    best_kw_list = KeywordModel.objects.all().order_by('-input_num')
    print('best_kw_list:', best_kw_list)
    kw_imgs = []
    kw_muss = []
    for best_kw in best_kw_list:
        kw_imgs.extend( artkey.art for artkey in ArtKeywordModel.objects.filter(art__kind=1, keyword=best_kw))
        kw_muss.extend( artkey.art for artkey in ArtKeywordModel.objects.filter(art__kind=2, keyword=best_kw))
    kw_imgs = list(set(kw_imgs))[:10]
    kw_muss = list(set(kw_muss))[:10]
    return render(request, 'salon/home.html', {'images': kw_imgs, 'musics': kw_muss })

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
    if request.session.get('auto_save'):
        del request.session['auto_save']

    return render(request, 'salon/start.html', {})

# 모델 호출 함수
def result_model(request):
    json_data = json.loads( request.body )

    text = translate(json_data['text'])
    tags = get_taglist(text)

    image_url = image_generation_beta(text) #image_generation(text) # https://~~~.jpg 형식
    music_file = generateMusic(tags)
    
    img_filename = uuid_name_upload_to(None, image_url)
    mus_filename = img_filename.replace('.jpg','.mid')

    res = requests.get(image_url)
    _, img_tn_file = save_img_and_thumbnail(res.content, img_filename)
    save_music(music_file, mus_filename)

    # music_file = music_generateMusic_beta() #generateMusic() # '~~~.mid' 형식

    data = {'result':'successful', 'result_code': '1', 'img_file':img_filename, 'img_tn_file':img_tn_file, 'mus_file':mus_filename}
    print('result_model:', data)
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


def save_music(music_file, music_filename):
    if settings.DEV_MODE or settings.TEST_MODE:
        with open('media/musics/'+ music_filename, 'wb') as f:
            f.write(music_file)
    music_filename = music_path + music_filename



# 출력창
def result(request):
    if request.session.get('auto_save'):
        text = request.session['test_keyword']['text']
        auto_save_art_id_list = request.session['auto_save']
        art_img = AutoArtUploadModel.objects.filter(kind=1, id__in=auto_save_art_id_list)[0]
        art_mus = AutoArtUploadModel.objects.filter(kind=2, id__in=auto_save_art_id_list)[0]
        context = {'text': text, 'img_file':art_img, "music_file":art_mus }
        return render(request, 'salon/result.html', context)
    
    text = translate(request.POST.get('input_text'))
    mus_filename = request.POST.get('mus_file')
    img_filename = request.POST.get('img_file')
    img_tn_filename = request.POST.get('img_tn_file')

    # 텍스트 -> 태그화 리스트
    no_stops = get_taglist(text)

    auto_save_art_id_list = []

    art_img = AutoArtUploadModel(kind=1, name=text, filename=img_filename, thumbnail=img_tn_filename, input_text=text)
    art_img.save()
    auto_save_art_id_list.append(art_img.id)

    art_mus = AutoArtUploadModel(kind=2, name=text+"_music", filename=mus_filename, input_text=text)
    art_mus.save()
    auto_save_art_id_list.append(art_mus.id)
    print( auto_save_art_id_list )

    request.session['test_keyword'] = {'text': text, "tags":no_stops }
    request.session['auto_save'] = auto_save_art_id_list

    context = {'text': text, 
                'img_file':art_img, 
                "music_file":art_mus, 
    }

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
    files = []

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

        auto_save_art_id_list = request.session['auto_save']

        favorite_dict = {}
        favorite_dict['image'] = int( favorite == 'jpg' or favorite == 'both' )
        favorite_dict['music'] = int( favorite == 'mid' or favorite == 'both' )

        selected_value_kind = {'image':1, 'music':2}

        for intype in selected:
            art_kind = selected_value_kind[intype]
            queryset = AutoArtUploadModel.objects.filter(kind=art_kind, id__in=auto_save_art_id_list)
            if len(queryset) > 0:
                auto_art = queryset[0]
                art = ArtUploadModel(kind=art_kind, user=user, name=text, filename=auto_art.filename,
                                        thumbnail=auto_art.thumbnail, input_text=text, result_favorite=favorite_dict[intype])
                art.save()
                files.append(art)

            akms = [ArtKeywordModel(art=art, keyword=km) for km in keyword_list]
            ArtKeywordModel.objects.bulk_create(akms)
        del request.session['auto_save']
            
        return render(request, 'salon/save_result.html', {'files':files})
    
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
