import requests
import configparser
config = configparser.ConfigParser()


config.read('config.ini')
access_token = config.get('Token_YD', 'token_YD')
token_YD = config.get('Token_YD', 'token_YD')


class YD_client:

    def __init__(self, token):
        self.token = token

    def create_folder_YD(self):
        "создаем папку на ЯД"

        headers = {'Authorization': self.token}
        url_yandex = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': 'VK_photos'}
        response = requests.put(url_yandex, headers=headers, params=params)
        if response.status_code == 201:
            print('Папка создана')
        else:
            print("Папка уже существует")

    def add_photos_to_YD(self, url_photo, name_photo):
        "сохранение фото папку на ЯД"

        url_yandex = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Authorization': self.token}
        try:

            # проверка на наличие уже сохраненной копии с тем же именем
            params = {'path': f'VK_photos/{name_photo}', 'fields': 'overwrite'}
            response1 = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers,
                                     params=params)

            if 'error' not in dict(response1.json()):
                try:
                    params = {'url': url_photo, 'path': f'VK_photos/{name_photo}'}
                    requests.post(url_yandex, headers=headers, params=params)
                except KeyError:
                    pass


        except KeyError:
            pass

yd_client = YD_client(token_YD)
