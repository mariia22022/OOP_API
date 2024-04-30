import requests
import json
from tqdm import tqdm
import save_photos_YD
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
access_token = config.get('Token_VK','token_VK')

VK_user_id = input('Введите id пользователя VK')

# вызываем метод класса YD_client для создания папки  на ЯД
save_photos_YD.yd_client.create_folder_YD()

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



def upload_photos_YD():
    "сохранение полученных  файлов на ЯД"

    parsed_photos = []
    for i in range(len(vk.get_photos().json()['response']['items'])):
        count_likes = vk.get_photos().json()['response']['items'][i]['likes']['count']
        name_photo = f"VK-photo{i + 1}_{count_likes}_likes.jpg"
        photo_copies_diff_sizes = vk.get_photos().json()['response']['items'][i]['sizes']
        for image in tqdm(photo_copies_diff_sizes, desc=f"сохранение фото {i + 1}", ncols=100):
            if image['type'] == 'z':
                url_photo = image['url']

                save_photos_YD.yd_client.add_photos_to_YD(url_photo,name_photo)
                parsed_photos.append({'file_name': name_photo, 'size': image['type']})

    # сохраняем результат в json файл
    with open('parsed_photos.json', 'w') as f:
        json.dump(parsed_photos, f)


vk = VK(access_token, VK_user_id)



# вызываем функцию для сохранения файлов на ЯД
upload_photos_YD()