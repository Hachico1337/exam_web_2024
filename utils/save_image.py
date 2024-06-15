import os
import hashlib


def save_image(filename, file_data):
    file_path = os.getcwd() + '/uploads/' + filename
    with open(file_path, 'wb') as f:
        f.write(file_data)


def hash_file(file_data):
    """
    хеширование картинки
    """
    md5_hash = hashlib.md5(file_data).hexdigest()
    return md5_hash
