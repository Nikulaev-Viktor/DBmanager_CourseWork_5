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
        employer_info = requests.get(url_emp).json()
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


def create_db(database_name: str, params: dict) -> None:
    """Создание базы данных для вакансий и компаний"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies(
            company_id INTEGER PRIMARY KEY,
            company_name VARCHAR(50) NOT NULL,
            company_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies(
            vacancy_id INTEGER PRIMARY KEY,
            company_id INTEGER REFERENCES companies(company_id),
            vacancy_name VARCHAR (100) NOT NULL,
            requirement VARCHAR(255),
            salary_from INTEGER,
            salary_to INTEGER,
            vacancy_url TEXT
            )
        """)


def save_to_db_companies(companies_data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях в базу данных."""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for company in companies_data:
            company_id = company['company_id']
            company_name = company['company_name']
            company_url = company['company_url']
            cur.execute("""
                    INSERT INTO companies (company_id, company_name, company_url)
                    VALUES (%s, %s, %s)
                """, (company_id, company_name, company_url))
    conn.commit()
    conn.close()


def save_to_db_vacancies(vacancies_data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о вакансиях в базу данных."""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in vacancies_data:
            vacancy_id = vacancy['id']
            company_id = vacancy['employer']['id']
            vacancy_name = vacancy['name']
            requirement = vacancy['snippet'].get('requirement', None)
            salary = vacancy['salary']
            salary_from = salary.get('from') if salary else None
            salary_to = salary.get('to') if salary else None
            vacancy_url = vacancy['alternate_url']
            cur.execute("""
                INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, requirement, salary_from, salary_to, 
                vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (vacancy_id, company_id, vacancy_name, requirement, salary_from, salary_to,
                  vacancy_url))
    conn.commit()
    conn.close()
