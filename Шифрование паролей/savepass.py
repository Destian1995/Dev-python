# -*- coding: utf-8 -*-
import json
import base64
import os
import hashlib
import subprocess
import sys


def generate_key():
    secret_phrase = "my_secret_phrase"
    return hashlib.sha256(secret_phrase.encode()).digest()


def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    return open("secret.key", "rb").read()


def xor_encrypt_decrypt(data, key):
    return bytes(a ^ b for a, b in zip(data, key))


def encrypt_password(password, key):
    encrypted_data = xor_encrypt_decrypt(password.encode(), key)
    return base64.urlsafe_b64encode(encrypted_data).decode()


def decrypt_password(encrypted_password, key):
    encrypted_data = base64.urlsafe_b64decode(encrypted_password.encode())
    decrypted_data = xor_encrypt_decrypt(encrypted_data, key)
    return decrypted_data.decode()


def save_password(account, password, filename='passwords.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[account] = password

    with open(filename, 'w') as file:
        json.dump(data, file)


def get_password(account, filename='passwords.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get(account, None)
    except FileNotFoundError:
        return None


def get_all_accounts(filename='passwords.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return list(data.keys())
    except FileNotFoundError:
        return []


def change_password(account, new_password, key, filename='passwords.json'):
    encrypted_password = encrypt_password(new_password, key)
    save_password(account, encrypted_password, filename)
    print(f"Пароль для {account} успешно изменён.")


def copy_to_clipboard(text):
    if sys.platform == 'win32':
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        process.communicate(input=text.encode())
    elif sys.platform == 'darwin':
        process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
        process.communicate(input=text.encode())
    elif sys.platform == 'linux':
        try:
            process = subprocess.Popen('xclip -selection clipboard', stdin=subprocess.PIPE, shell=True)
            process.communicate(input=text.encode())
        except FileNotFoundError:
            try:
                process = subprocess.Popen('xsel --clipboard --input', stdin=subprocess.PIPE, shell=True)
                process.communicate(input=text.encode())
            except FileNotFoundError:
                print("Ошибка: Не удалось найти утилиту для работы с буфером обмена. Установите xclip или xsel.")
    else:
        print("Копирование в буфер обмена не поддерживается для этой ОС.")


def display_menu():
    print("\nДоступные команды:")
    print("1. Добавить новую УЗ и пароль")
    print("2. Получить сохранённый пароль")
    print("3. Изменить существующий пароль")
    print("4. Просмотреть список всех учётных записей")
    print("5. Выйти из программы")


def main():
    try:
        key = load_key()
    except FileNotFoundError:
        print("Ключ шифрования не найден. Создается новый ключ.")
        key = generate_key()
        save_key(key)

    while True:
        display_menu()  # Выводим меню команд каждый раз перед вводом
        action = input("\nВыберите команду (1-5): ").strip()

        if action == '1':  # Добавить новый пароль
            account = input("Введите учетную запись: ")
            password = input("Введите пароль: ")
            encrypted_password = encrypt_password(password, key)
            save_password(account, encrypted_password)
            print("Пароль успешно сохранен.")

        elif action == '2':  # Получить сохранённый пароль
            accounts = get_all_accounts()
            if accounts:
                print("Доступные учетные записи:")
                for i, acc in enumerate(accounts, 1):
                    print(f"{i}. {acc}")
                account_choice = input("Введите номер учетной записи: ")
                try:
                    account_index = int(account_choice) - 1
                    account = accounts[account_index]
                    encrypted_password = get_password(account)
                    if encrypted_password:
                        decrypted_password = decrypt_password(encrypted_password, key)
                        print(f"Зашифрованный пароль для {account}: {encrypted_password}")
                        copy_choice = input("Хотите скопировать расшифрованный пароль в буфер обмена? (y/n): ").strip().lower()
                        if copy_choice == 'y':
                            copy_to_clipboard(decrypted_password)
                            print("Пароль скопирован в буфер обмена.")
                        else:
                            print(f"Пароль для {account}: {decrypted_password}")
                    else:
                        print("Пароль не найден.")
                except (ValueError, IndexError):
                    print("Неверный выбор учетной записи.")
            else:
                print("Нет сохраненных учетных записей.")

        elif action == '3':  # Изменить существующий пароль
            accounts = get_all_accounts()
            if accounts:
                print("Доступные учетные записи:")
                for i, acc in enumerate(accounts, 1):
                    print(f"{i}. {acc}")
                account_choice = input("Введите номер учетной записи для изменения пароля: ")
                try:
                    account_index = int(account_choice) - 1
                    account = accounts[account_index]
                    new_password = input(f"Введите новый пароль для {account}: ")
                    change_password(account, new_password, key)
                except (ValueError, IndexError):
                    print("Неверный выбор учетной записи.")
            else:
                print("Нет сохраненных учетных записей.")

        elif action == '4':  # Просмотреть список всех учётных записей
            accounts = get_all_accounts()
            if accounts:
                print("Доступные учетные записи:")
                for i, acc in enumerate(accounts, 1):
                    print(f"{i}. {acc}")
            else:
                print("Нет доступных учетных записей.")

        elif action == '5':  # Выйти
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите число от 1 до 5.")


if __name__ == "__main__":
    main()
