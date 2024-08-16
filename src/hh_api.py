import requests
from typing import List, Dict, Any


def get_employee(company_ids: List[str]) -> List[Dict[str, Any]]:

    """ Получаем данные о работодателях и вакансиях с использованием API HH.ru."""

    params = {
        'page': 0,
        'per_page': 100,
        "only_with_salary": True,
        "area": 113,
        "only_with_vacancies": True
    }
    data = []
    vacancies = []
    employers = []
    for employer_id in company_ids:
        url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url_emp, ).json()
        employers.append(employer_info)

        url_vac = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        vacancies_info = requests.get(url_vac, params=params).json()
        vacancies.extend(vacancies_info['items'])
    data.append({
        'employers': employers,
        'vacancies': vacancies
    })
    return data
