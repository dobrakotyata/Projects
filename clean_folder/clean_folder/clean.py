import os
import shutil
import re

if __name__ == "__main__":

    def delete_empty_folders(path):
            for foldername, subfolders, filenames in os.walk(path, topdown=False):
                # Игнорируем папки, которые не нужно удалять
                if foldername.endswith('archives') or foldername.endswith('video') \
                        or foldername.endswith('audio') or foldername.endswith('documents') \
                        or foldername.endswith('images'):
                    continue
                
                # Проверяем, является ли папка пустой
                if not os.listdir(foldername):
                    os.rmdir(foldername)
                    print(f"Folder {foldername} has been deleted.")

    def normalize(name):
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
            'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
            'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y',
            'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
            'Х': 'H', 'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA'
        }

        name = name.lower()  # Приводим к нижнему регистру

        transliterated_name = ''
        for char in name:
            if char in translit_map:
                transliterated_name += translit_map[char]
            elif re.match(r'[a-zA-Z0-9.]', char):
                transliterated_name += char
            else:
                transliterated_name += '_'
        
        return transliterated_name


    # Словарь с расширениями файлов и соответствующими папками
    extensions = {
        'JPEG': 'images',
        'JPG': 'images',
        'PNG': 'images',
        'SVG': 'images',
        'AVI': 'videos',
        'MP4': 'videos',
        'MOV': 'videos',
        'MKV': 'videos',
        'DOC': 'documents',
        'DOCX': 'documents',
        'TXT': 'documents',
        'PDF': 'documents',
        'XLSX': 'documents',
        'PPTX': 'documents',
        'MP3': 'music',
        'OGG': 'music',
        'WAV': 'music',
        'AMR': 'music',
        'ZIP': 'archives',
        'GZ': 'archives',
        'RAR': 'archives',
        'TAR': 'archives'
    }


    # Папка, которую нужно просканировать
    folder_path = input("Введите путь к папке: ")

    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        file_extension = filename.split('.')[-1].upper()  # Получаем расширение файла и переводим в верхний регистр
        if file_extension in extensions:
            folder_name = extensions[file_extension]  # Находим имя папки, куда нужно переместить файл
            destination_folder = os.path.join(folder_path, folder_name)  # Формируем путь к папке
            if not os.path.exists(destination_folder):  # Если папка не существует, создаем ее
                os.makedirs(destination_folder)
            source_path = os.path.join(folder_path, filename)  # Формируем путь к исходному файлу
            normalized_filename = normalize(filename)  # Нормализуем имя файла
            destination_path = os.path.join(destination_folder, normalized_filename)  # Формируем путь к целевому файлу
            shutil.move(source_path, destination_path)  # Перемещаем файл в целевую папку
        else:
            unknown_folder = os.path.join(folder_path, 'unknown')  # Если расширение файла неизвестно, перемещаем его в папку unknown
            if not os.path.exists(unknown_folder):
                os.makedirs(unknown_folder)
            source_path = os.path.join(folder_path, filename)
            normalized_filename = normalize(filename)  # Нормализуем имя файла
            destination_path = os.path.join(unknown_folder, normalized_filename)
            if destination_path.startswith(source_path + os.sep):
                continue
            shutil.move(source_path, destination_path)
