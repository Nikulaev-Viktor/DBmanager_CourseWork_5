import psycopg2


class DBManager:

    """Класс для подключения к БД PostgreSQL."""

    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='hh', **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):

        """Получает список всех компаний и количество вакансий у каждой компании"""

        self.cur.execute(f"SELECT company_name, open_vacancies FROM employers")
        return self.cur.fetchall()

    def get_all_vacancies(self):

        """Получает список всех вакансий с указанием названия компании, названия вакансии и
        зарплаты и ссылки на вакансию"""

        self.cur.execute("""
        SELECT employers.company_name, vacancy_name, salary_from, vacancy_url
        FROM vacancies
        JOIN employers USING (employer_id)
        ORDER BY salary_from desc""")
        return self.cur.fetchall()

    def get_avg_salary(self):

        """Получает среднюю зарплату по вакансиям"""

        self.cur.execute(f"SELECT ROUND(AVG(salary_from)) FROM vacancies")
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):

        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        self.cur.execute(f"SELECT vacancy_name, salary_from FROM vacancies "
                         f"WHERE salary_from > (select avg(salary_from) FROM vacancies)")

        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):

        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""

        query = """SELECT * FROM vacancies
                        WHERE LOWER(vacancy_name) LIKE %s"""
        self.cur.execute(query, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()
