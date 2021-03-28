from django.core.files.storage import FileSystemStorage
import os
from commerce import settings


class OverwriteStorage(FileSystemStorage):
    """ Проверяем наличие дуликата добавляемого файла """

    def get_available_name(self, name, max_length=None, ):
        """ Если файл с таким именем существует, удаляем """
        path = os.path.join(settings.MEDIA_ROOT, '/'.join(name.split('/')[:-1]))
        num = name.split('.')[-2]
        try:
            for image_name in os.listdir(path):
                if num in image_name:
                    os.remove(f'{path}/{image_name}')
        except:
            pass

        return name
