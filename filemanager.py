# функция для чтения и шифрования файла
from extra import encrypt_cbc, decrypt_cbc


def encrypt_file(input_filename, output_filename, key):
    with open(input_filename, 'rb') as f:
        data = f.read()

    print(f"прочитано {len(data)} байт из {input_filename}")

    # шифруем
    ciphertext, iv = encrypt_cbc(data, key)

    # сохраняем сначала IV (16 байт), потом шифротекст
    with open(output_filename, 'wb') as f:
        f.write(iv)
        f.write(ciphertext)

    print(f"зашифровано в {output_filename}")
    print(f"вектор инициализации (IV): ", end="")
    for b in iv:
        print(f"{b:02x}", end="")
    print()


# расшифровка файла
def decrypt_file(input_filename, output_filename, key):
    with open(input_filename, 'rb') as f:
        data = f.read()

    # первые 16 байт - это IV
    iv = data[:16]
    # остальное - шифротекст
    ciphertext = data[16:]

    print(f"IV из файла: ", end="")
    for b in iv:
        print(f"{b:02x}", end="")
    print()
    print(f"шифротекст: {len(ciphertext)} байт")

    # расшифровываем
    plaintext = decrypt_cbc(ciphertext, key, iv)

    # сохраняем
    with open(output_filename, 'wb') as f:
        f.write(plaintext)

    print(f"расшифровано в {output_filename}")