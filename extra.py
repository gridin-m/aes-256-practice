import os
from key import key_expansion
from utils import *


# дополнение до 16 байт
def pad_pkcs7(data):
    need = 16 - (len(data) % 16)

    # если данных ровно 16, добавляем целый блок из 16
    if need == 0:
        need = 16

    padding = []
    for i in range(need):
        padding.append(need)

    # превращаем в байты и добавляем к данным
    padding_bytes = bytes(padding)
    return data + padding_bytes


def unpad_pkcs7(data):
    # последний байт показывает, сколько добавили, теперь убавляем
    pad_len = data[-1]
    return data[:-pad_len]

# складываем два набора байт по XOR
def xor_bytes(a, b):
    result = []
    for i in range(len(a)):
        result.append(a[i] ^ b[i])
    return bytes(result)


# широфвание в режиме CBC
def encrypt_cbc(plaintext, key, iv=None):
    # если не дали IV, создаём случайный
    if iv is None:
        iv = os.urandom(16)

    # разворачиваем ключ
    round_keys = key_expansion(key)

    # добавляем дополнение
    plaintext = pad_pkcs7(plaintext)

    # шифруем по блокам
    ciphertext = b""
    previous = iv

    i = 0
    while i < len(plaintext):
        # берём блок
        block = plaintext[i:i + 16]

        # XOR с предыдущим шифротекстом (или с IV для первого блока)
        xored = xor_bytes(block, previous)

        # шифруем
        encrypted = encrypt_block(xored, round_keys)

        # добавляем к результату
        ciphertext = ciphertext + encrypted

        # этот блок становится предыдущим для следующего
        previous = encrypted

        i = i + 16

    return ciphertext, iv

# дешифрование в режиме CBC
def decrypt_cbc(ciphertext, key, iv):
    round_keys = key_expansion(key)

    plaintext = b""
    previous = iv

    i = 0
    while i < len(ciphertext):
        block = ciphertext[i:i + 16]

        # расшифровываем блок
        decrypted = decrypt_block(block, round_keys)

        # XOR с предыдущим шифротекстом
        plain_block = xor_bytes(decrypted, previous)

        # добавляем к результату
        plaintext = plaintext + plain_block

        # текущий блок становится предыдущим
        previous = block

        i = i + 16

    # убираем дополнение
    return unpad_pkcs7(plaintext)