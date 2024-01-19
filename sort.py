import sys
import re
import shutil
from pathlib import Path


JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEOS = []
MP4_VIDEOS = []
MOV_VIDEOS = []
MKV_VIDEOS = []

DOC = []
DOCX = []
TXT = []
PDF = []
XLSX = []
PPTX = []

MP3_AUDIOS = []
OGG_AUDIOS = []
WAV_AUDIOS = []
AMR_AUDIOS = []

ZIP_ARCHIVES = []
GZ_ARCHIVES = []
RAR_ARCHIVES = []

OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'AVI': AVI_VIDEOS,
    'MP4': MP4_VIDEOS,
    'MOV': MOV_VIDEOS,
    'MKV': MKV_VIDEOS,
    'DOC': DOC,
    'DOCX': DOCX,
    'TXT': TXT,
    'PDF': PDF,
    'XLSX': XLSX,
    'PPTX': PPTX,
    'MP3': MP3_AUDIOS,
    'OGG': OGG_AUDIOS,
    'WAV': WAV_AUDIOS,
    'AMR': AMR_AUDIOS,
    'ZIP': ZIP_ARCHIVES,
    'GZ': GZ_ARCHIVES,
    'RAR': RAR_ARCHIVES,
    'OTHER': OTHER,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()

def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue

        extension = get_extension(item.name)
        full_name = folder / item.name
        print(full_name)
        if not extension:
            OTHER.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)
                OTHER.append(full_name)


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    translate_word = str(re.sub(r'\W', '_', name.translate(TRANS)))
    # first version
    translate_word = change_name(translate_word)

    # second version
    # translate_word = re.sub(r'_'+Path(name).suffix[1:], '.'+Path(name).suffix[1:], translate_word)

    return translate_word

def change_name(translate_word):
    index_str = translate_word.rfind('_')
    result = translate_word.replace(translate_word[index_str:], '.'+translate_word[index_str+1:])
    return result




def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')
    for file in MP3_AUDIOS:
        handle_media(file, folder / 'audio' / 'MP3_AUDIOS')
    for file in OGG_AUDIOS:
        handle_media(file, folder / 'audio' / 'OGG_AUDIOS')
    for file in WAV_AUDIOS:
        handle_media(file, folder / 'audio' / 'WAV_AUDIOS')
    for file in AMR_AUDIOS:
        handle_media(file, folder / 'audio' / 'AMR_AUDIOS')
    for file in AVI_VIDEOS:
        handle_media(file, folder / 'audio' / 'AVI_VIDEOS')
    for file in MP4_VIDEOS:
        handle_media(file, folder / 'audio' / 'MP4_VIDEOS')
    for file in MOV_VIDEOS:
        handle_media(file, folder / 'audio' / 'MOV_VIDEOS')
    for file in MKV_VIDEOS:
        handle_media(file, folder / 'audio' / 'MKV_VIDEOS')
    for file in DOC:
        handle_media(file, folder / 'audio' / 'DOC')
    for file in DOCX:
        handle_media(file, folder / 'audio' / 'DOCX')
    for file in TXT:
        handle_media(file, folder / 'audio' / 'TXT')
    for file in PDF:
        handle_media(file, folder / 'audio' / 'PDF')
    for file in XLSX:
        handle_media(file, folder / 'audio' / 'XLSX')
    for file in PPTX:
        handle_media(file, folder / 'audio' / 'PPTX')
    for file in RAR_ARCHIVES:
        handle_media(file, folder / 'audio' / 'RAR_ARCHIVES')
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / 'ZIP_ARCHIVES')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / 'GZ_ARCHIVES')
    for file in OTHER:
        handle_media(file, folder / 'OTHER')
    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

def begin():
    if sys.argv[1]:
        folder_process = Path(sys.argv[1])
        main(folder_process)

# from abc import ABC, abstractmethod
# from pathlib import Path
# from moviepy.editor import VideoFileClip
# from PIL import Image
#
# class Media(ABC):
#     @abstractmethod
#     def handle_media(self, file_path, output_folder):
#         pass
#
# class Image(Media):
#     def handle_media(self, file_path, output_folder):
#       pass
#
# class Video(Media):
#     def handle_media(self, file_path, output_folder):
#         pass
#
# class MediaProcessor:
#     def __init__(self, handler: MediaHandler):
#         self.handler = handler
#
#     def process(self, file_path, output_folder):
#         self.handler.handle_media(file_path, output_folder)
#
# def main():
#     if len(sys.argv) > 1:
#         folder_process = Path(sys.argv[1])
#         main(folder_process)


#
# if __name__ == "__main__":
#     image_handler = Image()
#     video_handler = Video()
#     processor = MediaProcessor(image_handler)
#     main()
