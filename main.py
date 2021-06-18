#!/venv/bin/python3

from configuration import vk_token, ya_token, version
from yauploader import YaUploader
from tqdm import tqdm
from vk import Vk
import time


HELP = '''
тут будет перечень доступных команд
vk - копирование из Vkontakte
ok - Одноклассники
inst - Instagram
help - справка
exit - выход
'''


class BackupPhotoVk:

    def __init__(self, ya_token, vk_token, version, folder_social_network):

        self.vk_agent = Vk(token=vk_token, version=version)
        interim = self.vk_agent.photos_info()
        
        if interim is None:
            pass
        else:
            self.photos_info = interim[0]
            self.user_folder = interim[1]
            self.album_title = interim[-1]
            self.ya_agent = YaUploader(
                token=ya_token,
                folder_social_network=folder_social_network,
                user_folder=self.user_folder,
                album_folder=self.album_title
                )

    def backup(self):

        try:
            self.photos_info
        except AttributeError:
            print('Произошла ошибка.')

        else:
            c = 0
            for photo in tqdm(self.photos_info):
                self.ya_agent.upload_social_network(
                    file_name=photo['file_name'],
                    link=photo['link']
                    )
                time.sleep(1)
                c += 1

            print(f'Резервное копирование завершено. Сохранено {c} фотографий.')


class BackupPhotoOk:

    def __init__(self):
        print(
            'Возможность загрузки из ОК будет реализована в следующих версиях.'
            )


class BackupPhotoInst:

    def __init__(self):
        print(
            'Возможность загрузки из Instagram будет реализована в следующих версиях.'
            )


class UserAgent:

    def __init__(self):

        self.commands = {
            'vk': self.vk,
            'ok': self.ok,
            'inst': self.inst
        }

    def user_input(self):

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

        backup_vk = BackupPhotoVk(
            ya_token=ya_token,
            vk_token=vk_token, 
            version=version,
            folder_social_network=self.command
            )
        backup_vk.backup()

    def ok(self):

        BackupPhotoOk()

    def inst(self):

        BackupPhotoInst()


if __name__ == '__main__':
    user_backup = UserAgent()
    user_backup.user_input()    
