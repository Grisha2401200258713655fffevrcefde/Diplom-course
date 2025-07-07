import os
import requests
import shodan
from PIL import Image
from PIL.ExifTags import TAGS

# Убираем необходимость API-ключей
SHODAN_API_KEY = None
HIBP_API_KEY = None


def search_ip(ip):
    try:
        print(f"Ищем информацию об IP: {ip}")
        result = requests.get(f"https://api.shodan.io/shodan/host/{ip}?key=free")
        if result.status_code == 200:
            data = result.json()
            print(f"IP: {data['ip_str']}")
            print(f"Организация: {data.get('org', 'Неизвестно')}")
            print(f"Операционная система: {data.get('os', 'Неизвестно')}")
            for item in data.get('data', []):
                print(f"Порт: {item['port']}")
                print(f"Баннер: {item['data']}")
        else:
            print(f"Ошибка: {result.status_code} - {result.text}")
        print(f"IP: {result['ip_str']}")
        print(f"Организация: {result.get('org', 'Неизвестно')}")
        print(f"Операционная система: {result.get('os', 'Неизвестно')}")
        for item in result['data']:
            print(f"Порт: {item['port']}")
            print(f"Баннер: {item['data']}")
    except shodan.APIError as e:
        print(f"Ошибка: {e}")


def check_email_leak(email):
    url = f"https://emailrep.io/{email}"
    headers = {
        "User-Agent": "Python script"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Адрес {email} был найден в следующих утечках:")
        for breach in response.json():
            print(f"- {breach['Name']}")
    elif response.status_code == 404:
        print("Адрес не был найден в известных утечках.")
    else:
        print(f"Ошибка: {response.status_code}")


def get_exif_data(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                print(f"{tag_name}: {value}")
        else:
            print("Метаданные не найдены.")
    except Exception as e:
        print(f"Ошибка: {e}")


def main():
    print("Выберите действие:")
    print("1. Поиск информации по IP-адресу")
    print("2. Проверка утечек данных по e-mail")
    print("3. Анализ метаданных изображений")
    choice = input("Введите номер действия: ")

    if choice == "1":
        ip_address = input("Введите IP-адрес: ")
        search_ip(ip_address)
    elif choice == "2":
        email = input("Введите адрес электронной почты: ")
        check_email_leak(email)
    elif choice == "3":
        image_path = input("Введите путь к изображению: ")
        get_exif_data(image_path)
    else:
        print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
