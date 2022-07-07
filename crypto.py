import data
import telegram

from re import findall
from random import randint
from hashlib import sha256
from os import remove, replace
from PIL import Image, ImageDraw
from Cryptodome.Cipher import AES

data_password0 = data.password0
data_password1 = data.password1
file_password = data.file_password
api_id = data.api_id
api_hash = data.api_hash


def get_hash(password):
    return sha256(password.encode('UTF-8')).hexdigest()


def vereficate_password(password, dpass0=data_password0, dpass1=data_password1):
    if get_hash(password) == dpass0:
        return 0
    elif get_hash(password) == dpass1:
        return 1
    else:
        return -1


def crypt(file, mode):
    file_in = open(file, 'rb')
    file_data = file_in.read()
    file_in.close()

    key = file_password.encode('UTF-8')
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)

    file_out = open(f'./TEMP/{file.split("/")[-1]}', "wb")
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()

    telegram.send_file(f'./TEMP/{file.split("/")[-1]}', mode)
    remove(f'./TEMP/{file.split("/")[-1]}')


def decrypt(file_patch, file_name):
    key = file_password.encode('UTF-8')

    file_in = open(f'./TEMP/{file_name}', "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    file_data = cipher.decrypt_and_verify(ciphertext, tag)

    file_out = open(f'{file_patch}/{file_name}', 'wb')
    file_out.write(file_data)
    file_out.close()



def stega_encrypt(path_to_image, message, key_patch):
    keys = []
    img = Image.open(path_to_image)
    draw = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pix = img.load()
    with open(f'{key_patch}/{path_to_image.split("/")[-1].split(".")[0]}.key', 'w') as f:
        for elem in ([ord(elem) for elem in message]):
            key = (randint(1, width - 10), randint(1, height - 10))
            g, b = pix[key][1:3]
            draw.point(key, (elem, g, b))
            f.write(str(key) + '\n')
    img.save(f'./TEMP/{path_to_image.split("/")[-1].replace("jpg", "")}png', "PNG")


def stega_decrypt(patch_im, patch_keys):
    a = []
    keys = []
    img = Image.open(patch_im)
    pix = img.load()
    f = open(patch_keys, 'r')
    y = str([line.strip() for line in f])

    for i in range(len(findall(r'\((\d+)\,', y))):
        keys.append((int(findall(r'\((\d+)\,', y)[i]), int(findall(r'\,\s(\d+)\)', y)[i])))
    for key in keys:
        a.append(pix[tuple(key)][0])
    return ''.join([chr(elem) for elem in a])