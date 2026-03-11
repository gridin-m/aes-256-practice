import os
import random
import string
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from filemanager import encrypt_file, decrypt_file

KEY_FILE = "files/key.txt"


def load_key():
    key_path = Path(KEY_FILE)

    if key_path.exists():
        with open(key_path, 'r') as f:
            key_str = f.read().strip()

        if len(key_str) == 32:
            print(f"Ключ загружен из {KEY_FILE}")
            return key_str.encode('utf-8')

        print(f"В файле {KEY_FILE} неправильный ключ, создаём новый")

    key_path.parent.mkdir(parents=True, exist_ok=True)

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    key_str = ''.join(random.choice(alphabet) for _ in range(32))

    with open(key_path, 'w') as f:
        f.write(key_str)

    print(f"Новый ключ сохранён в {KEY_FILE}")
    return key_str.encode('utf-8')


def list_files(path="."):
    files = []
    folders = []

    for item in sorted(os.listdir(path)):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            folders.append(item)
        else:
            files.append(item)

    i = 1
    for folder in folders:
        print(f"{i:2d}. {folder}/")
        i += 1

    for file in files:
        print(f"{i:2d}. {file}")
        i += 1

    return folders + files


def select_file():
    print("Выберите файл:")
    current_dir = "."

    while True:
        files = list_files(current_dir)

        choice = input("> ").strip()

        if choice.lower() == 'q':
            current_dir = os.path.dirname(os.path.abspath(current_dir))
            if not current_dir:
                current_dir = "/"
            continue

        if choice == '0':
            return current_dir

        if choice.startswith('/') or choice.startswith('.') or ':' in choice:
            if os.path.exists(choice):
                if os.path.isdir(choice):
                    current_dir = choice
                    continue
                else:
                    return choice
            else:
                print("Путь не найден")
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                selected = files[idx]
                full_path = os.path.join(current_dir, selected)
                if os.path.isdir(full_path):
                    current_dir = full_path
                else:
                    return full_path
            else:
                print("Неправильный номер")
        except ValueError:
            print("Неправильный номер")


def show_info(filename):
    if not os.path.exists(filename):
        return

    size = os.path.getsize(filename)
    print(f"\nФайл: {filename}")
    print(f"Размер: {size} байт")


def main():
    key = load_key()

    while True:
        print("\n1. Зашифровать файл")
        print("2. Расшифровать файл")
        print("3. Выход")

        choice = input("\nВыберите: ").strip()

        if choice == '3':
            print("Завершение работы")
            break

        if choice not in ['1', '2']:
            print("Такой опции нет")
            continue

        in_file = select_file()

        if choice == '1':
            out_file = in_file + ".enc"
        else:
            if in_file.endswith('.enc'):
                out_file = in_file[:-4] + ".dec"
            else:
                out_file = in_file + ".dec"

        try:
            if choice == '1':
                encrypt_file(in_file, out_file, key)
            elif choice == '2':
                decrypt_file(in_file, out_file, key)

            print("\nУспешно")
        except Exception as e:
            print(f"\nОшибка: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()