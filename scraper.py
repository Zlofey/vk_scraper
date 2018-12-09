from bs4 import BeautifulSoup
from pprint import pprint
import vk, os, time
import requests


vk_id = '6755506'

#session = vk.AuthSession(app_id=vk_id, user_login=login,user_password=password , scope='photos')
session = vk.Session(access_token='8319cfce8319cfce8319cfce02837edb7c883198319cfced8e8a202245361d8593ff381')
vkapi = vk.API(session)


url = input("Введите url альбома: ")

# Разбираем ссылку
album_id = url.split('/')[-1].split('_')[1]
owner_id = url.split('/')[-1].split('_')[0].replace('album', '')

counter = 0  # текущий счетчик
prog = 0  # процент загруженных
breaked = 0  # не загружено из-за ошибки
time_now = time.time()  # время старта


albums = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id, v=5.87)  # Получаем имя альбома
album_name = albums['items'][0]['title']
album_size = albums['items'][0]['size']
print(album_name,album_size) #количество фото

# Создадим каталоги

if not os.path.exists('/run/media/zlofey/data/saved'):
    os.mkdir('/run/media/zlofey/data/saved')
photo_folder = '/run/media/zlofey/data/saved/{0}'.format(album_name)

if not os.path.exists(photo_folder):
    os.mkdir(photo_folder)

vk_offset = 0


# pprint(photos['items'][-1]['id'])
# pprint(photos['items'][0]['id'])

album_size_const = album_size
while album_size > 0:
    print(vk_offset)
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=999, offset=vk_offset,
                              v=5.87)  # Получаем массив фото

    for photo in photos['items']:
        url = photos['items'][counter]['sizes'][-1]['url'] #url = photos['items'][counter]['sizes'][-1]['url'] max image
        counter += 1
        print('Загружаю фото № {} из {}. Фото_id: {} Прогресс: {} %'.format(counter + vk_offset, album_size_const,
                                                                            photos['items'][counter-1]['id'], prog))
        prog = round(100 / album_size * counter, 2)
        try:
            #urlretrieve(url, photo_folder + "/" + os.path.split(url)[1])  # Загружаем и сохраняем файл
            photo_folder + "/" + os.path.split(url)[1]
            f = open(photo_folder + "/" + os.path.split(url)[1], "wb")
            ufr = requests.get(url)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            f.close()
        except Exception:
            print('Произошла ошибка, файл пропущен.')
            breaked += 1
            continue
    album_size -= 999
    vk_offset += 999
    counter = 0




time_for_dw = time.time() - time_now
print("\nВ очереди было {} файлов. Из них удачно загружено {} файлов, {} не удалось загрузить. Затрачено времени: {} сек.".
      format(album_size_const, album_size_const-breaked, breaked, round(time_for_dw,1)))
