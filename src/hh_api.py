import requests
import json
import psycopg2
from typing import Any

employer_ids = {'Авито Тех': '5779602',
                'Мтс Банк': '4496',
                'Билайн': '4934',
                'Т-Банк': '78638',
                'Мегафон': '3127',
                'IBS': '139',
                'Лаборатория Касперского': '1057',
                'СБЕР': '3529',
                'Центр финансовых технологий': '8550',
                'OZON': '2180'
                }


def get_employee():
    """
    Функция для получения данных о компаниях с сайта HH.ru
    """
    employers = []
    for employer_id in employer_ids:
        url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url_emp, ).json()
        employers.append(employer_info)

    return employers


def get_vacancies():
    """
    Функция для получения данных о вакансиях с сайта HH.ru
    """
    vacancy = []
    for vacancies_id in employer_ids:
        url_vac = f"https://api.hh.ru/vacancies?employer_id={vacancies_id}"
        vacancy_info = requests.get(url_vac, params={'page': 0, 'per_page': 100}).json()
        vacancy.extend(vacancy_info['items'])
    return vacancy



