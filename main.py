from src.config import config
from src.dbmanager import DBManager
from src.hh_api import get_employee
from src.utils import create_database, save_data_to_database_emp, save_data_to_database_vac


def main():
    """Функция взаимодействия с пользователем"""

    company_ids = [
        '5779602',
        '4496',
        '4934',
        '78638',
        '3127',
        '139',
        '1057',
        '3529',
        '8550',
        '2381',
        '5060211',
        '1993194'
    ]

    params = config()
    data = get_employee(company_ids)
    create_database('hh', params)
    save_data_to_database_emp(data, 'hh', params)
    save_data_to_database_vac(data, 'hh', params)

    db_manager = DBManager(params)
    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n")
    while True:
        user_input = input('Введите номер запроса\n')
        if user_input == "1":
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}\n")

        elif user_input == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print(
                f"Cписок всех вакансий с указанием названия компании,"
                f" названия вакансии и зарплаты и ссылки на вакансию: {all_vacancies}\n")

        elif user_input == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary} руб.\n")

        elif user_input == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(
                f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: {vacancies_with_higher_salary}\n")

        elif user_input == "5":
            user_input = input('Введите  слово ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово: {vacancies_with_keyword}")

        else:
            print("Введен неверный запрос")
        break


if __name__ == '__main__':
    main()
