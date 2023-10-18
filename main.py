#!/venv/bin/python3

from configuration import vk_token, ya_token, version
from yauploader import YaUploader
from tqdm import tqdm
from vk import Vk
import time
import json


HELP = '''
тут будет перечень доступных команд
vk - копирование из Vkontakte
ok - Одноклассники
inst - Instagram
help - справка
exit - выход
'''


def backup_ya(interim, folder_social_network):

    if interim is None:
        pass
    else:
        photos_info = interim[0]
        user_folder = interim[1]
        album_title = interim[-1]
        ya_agent = YaUploader(
            token=ya_token,
            folder_social_network=folder_social_network,
            user_folder=user_folder,
            album_folder=album_title
            )

        try:
            photos_info
        except AttributeError:
            print('Произошла ошибка.')

        else:
            c = 0
            for photo in tqdm(photos_info):
                ya_agent.upload_social_network(
                    file_name=photo['file_name'],
                    link=photo['link']
                    )
                time.sleep(1)
                c += 1

            print(f'Резервное копирование завершено. Сохранено {c} фотографий.')

            photos_info_print = []
            for info in photos_info:
                info.pop('link')
                photos_info_print.append(info)

            date = time.strftime('%d%m%Y_%H%M%S')
            file_name = f'photos_info_{date}.json'

            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(photos_info_print, file, indent=2)


class UserAgent:

    def __init__(self):

        self.commands = {
            'vk': self.vk,
            'ok': self.ok,
            'inst': self.inst
        }

    def user_input(self):
        """Пользовательский ввод данных в консоль"""
        print(HELP)
        run = True
        while run:
            self.command = input('Введите комманду: ').lower()

            if self.command in self.commands:
                self.commands[self.command]()

            elif self.command == 'exit':
                print('До новых встреч!')
                run = False

            elif self.command == 'help':
                print(HELP)

            else:
                print(
                    f'Данная команда {self.command} не обнаружена. Для справки введите help\n'
                    )

    def vk(self):

        vk_agent = Vk(token=vk_token, version=version)
        interim = vk_agent.photos_info()
        folder_social_network = self.command
        backup_ya(interim, folder_social_network)

    def ok(self):

        print(
            'Возможность загрузки из ОК будет реализована в следующих версиях.'
            )

    def inst(self):

        print(
            'Возможность загрузки из Instagram будет реализована в следующих версиях.'
            )


if __name__ == '__main__':
    user_backup = UserAgent()
    user_backup.user_input()    
