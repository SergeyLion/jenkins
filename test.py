import allure
import requests

BASE_URL = "https://qa-mesto.praktikum-services.ru"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NzZjNGJiYjA4NmViMjAwMzU1NzUxNjYiLCJpYXQiOjE3NDMwMTAzMjcsImV4cCI6MTc0MzYxNTEyN30.QzU0KRmGqtlrxPpWDP0BkaKXT3xutr5WQM4LE__Fw6k"

@allure.step("Добавление новой фотографии")
def add_new_photo():
    url = f"{BASE_URL}/api/cards"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": "Москва",
        "link": "https://code.s3.yandex.net/qa-automation-engineer/java/files/paid-track/sprint1/photoSelenium.jpg"
    }
    response = requests.post(url, json=data, headers=headers)
    assert response.status_code == 201, f"Ошибка: {response.text}"

@allure.step("Получение ID первой фотографии")
def get_first_photo_id():
    url = f"{BASE_URL}/api/cards"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "Не удалось получить список фото"
    return response.json()['data'][0]['_id']

@allure.step("Поставить лайк фото")
def like_photo(photo_id):
    url = f"{BASE_URL}/api/cards/{photo_id}/likes"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.put(url, headers=headers)
    assert response.status_code == 200, "Ошибка при лайке фото"

@allure.step("Снять лайк с фото")
def delete_like(photo_id):
    url = f"{BASE_URL}/api/cards/{photo_id}/likes"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200, "Ошибка при удалении лайка"

@allure.title("Лайк и удаление лайка на первую фотографию")
def test_like_and_unlike_photo():
    photo_id = get_first_photo_id()
    like_photo(photo_id)
    delete_like(photo_id)

@allure.title("Проверка имени пользователя")
def test_check_username():
    url = f"{BASE_URL}/api/users/me"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    assert response.json()["data"]["name"] == "Николай Пржевальский", "Имя пользователя не совпадает"