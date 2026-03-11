from utils import *


# применяем S-Box к каждому байту в слове
def sub_word(word):
    result = [0, 0, 0, 0]
    for i in range(4):
        result[i] = S_BOX[word[i]]
    return result

# циклический сдвиг влево на 1 байт
# было [b0, b1, b2, b3] -> стало [b1, b2, b3, b0]
def rot_word(word):
    return [word[1], word[2], word[3], word[0]]

# для AES-256 нужно 60 слов (15 раундовых ключей по 4 слова)
# создаём список из 60 слов, каждое слово - список из 4 байт
def key_expansion(key):
    w = []
    for _ in range(60):
        w.append([0, 0, 0, 0])

    # первые 8 слов - сам ключ
    # ключ 32 байта, разбиваем на 8 частей по 4 байта
    for i in range(8):
        for j in range(4):
            w[i][j] = key[i * 4 + j]

    # генерируем остальные слова
    for i in range(8, 60):
        # берём предыдущее слово
        temp = []
        for j in range(4):
            temp.append(w[i - 1][j])

        # каждые 8 слов делаем преобразования rotWord и subWord
        if i % 8 == 0:

            temp = rot_word(temp)
            temp = sub_word(temp)

            # XOR с константой раунда
            rcon_val = RCON[i // 8]
            temp[0] = temp[0] ^ rcon_val
        elif i % 8 == 4:
            # для AES-256 на каждом 4-м слове делаем SubWord
            temp = sub_word(temp)

        # XOR со словом на 8 позиций назад
        for j in range(4):
            w[i][j] = w[i - 8][j] ^ temp[j]

    # собираем раундовые ключи (по 4 слова на ключ)
    round_keys = []
    for i in range(0, 60, 4):
        round_key = []
        for j in range(4):
            round_key.append(w[i + j])
        round_keys.append(round_key)

    return round_keys