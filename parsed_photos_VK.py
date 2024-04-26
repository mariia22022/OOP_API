import requests
from pprint import pprint
import json
from tqdm import tqdm

# токен VK полученный из инструкции
access_token = input('Ведите Ваш access-token VK')

VK_user_id = input('Введите id пользователя VK')


class VK:
    def __init__(self, access_token, user_id, version='5.199'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'wall', 'extended': '1', 'count': 5}

        response = requests.get(url, params={**self.params, **params})
        return response


vk = VK(access_token, VK_user_id)
pprint(vk.get_photos().json())

# сохраняем в файл для удлбства чтения
# with open('photos_vk.json', 'w') as f:
#     f.write(vk.get_photos().text)

# создаем папку на ЯД
token_YD = input('Ведите Ваш токен для Яндекс-диска')
url_yandex = "https://cloud-api.yandex.net/v1/disk/resources"
params = {'path': 'VK_photos'}
headers = {'Authorization': token_YD}
response = requests.put(url_yandex, headers=headers, params=params)
if response.status_code == 201:
    print('Папка создана')
else:
    print(response)

parsed_photos = []
for i in range(len(vk.get_photos().json()['response']['items'])):  # либо сразу написать 5 шт
    count_likes = vk.get_photos().json()['response']['items'][i]['likes']['count']
    name_photo = f"VK-photo{i + 1}_{count_likes}_likes.jpg"
    photo_copies_diff_sizes = vk.get_photos().json()['response']['items'][i]['sizes']
    for image in tqdm(photo_copies_diff_sizes, desc=f"сохранение фото {i + 1}", ncols=100):
        if image['type'] == 'z':
            url_photo = image['url']
            response = requests.get(url_photo)

            # сохранить фото в папке
            with open(name_photo, 'wb') as f:
                f.write(response.content)

            #  запрос пути  ЯД для сохранения фала
            params = {'path': f'VK_photos/{name_photo}'}
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers,
                                    params=params)

            # путь для сохранения файла
            url_for_upload = (response.json()['href'])

            # второй этап открываем файл сохраненный с VK отправляем его на ЯД
            with open(name_photo, 'rb') as f:
                requests.put(url_for_upload, files={'file': f})

            parsed_photos.append({'file_name': name_photo, 'size': image['type']})

# сохраняем результат в json файл
with open('parsed_photos.json', 'w') as f:
    json.dump(parsed_photos, f)
