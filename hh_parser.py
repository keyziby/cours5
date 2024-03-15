import json
import time

import requests


class HeadHunter:
    URL = 'https://api.hh.ru/vacancies'

    def __init__(self, search_keyword):
        self.params = {'text': search_keyword,
                       'page': 0,
                       'per_page': 100}

    def get_request(self):
        """Запрос к API HH"""
        response = requests.get(self.URL, params=self.params)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_request_company(self):
        """
        Парсим компании с ресурса HeadHunter
        """
        url = 'https://api.hh.ru/vacancies'
        company_id = set()
        for _ in range(15):
            request_hh = requests.get(url, params={"text": search_keyword}).json()['items']
            time.sleep(0.5)
            for item in request_hh:
                if len(company_id) == 15:
                    break
                company_id.add(item['employer']['id'])
        return list(company_id)

    def get_employers(self):
        """Получает список компаний и их id"""
        employers = []
        data = self.get_request()
        items = data.get('items')
        for item in items[:15]:
            employer = item.get('employer')
            if employer and employer.get('id') and employer.get('name'):
                employers.append((employer['id'], employer['name']))
        unique_employers = list(set(employers))
        with open('employers.json', 'w', encoding="UTF-8") as file:
            json.dump(unique_employers, file, indent=4, ensure_ascii=False)
        return unique_employers

    def get_info(self, data):
        """Структурирует получаемые из API данные"""
        vacancy_id = data.get('id')
        name = data.get('name')
        employer_id = data.get('employer').get('id')
        city = data.get('area').get('name')
        url = data.get('alternate_url')

        salary = None
        if 'salary' in data:
            salary_data = data.get('salary')
            if salary_data and 'from' in salary_data:
                salary = salary_data.get('from')

        return vacancy_id, name, employer_id, city, salary, url

    def get_vacancies(self):
        vacancies = []
        page = 0
        while True:
            self.params['page'] = page
            data = self.get_request()
            for vacancy in data.get('items'):
                salary = vacancy.get('salary')
                if salary and salary.get('currency') == "RUR":
                    vacancies.append(self.get_info(vacancy))

            page += 1
            time.sleep(0.2)

            if data.get('pages') == page:
                break

        with open('vacancies.json', 'w', encoding="UTF-8") as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False)

        return vacancies


if __name__ == '__main__':
    search_keyword = 'Python'
    hh = HeadHunter(search_keyword)
    # o = hh.get_request_company()
    # print(o)
    k = hh.get_request()
    print(k)
    # print(type(k))
    # m = hh.get_vacancies()
    # print(m)
    # print(type(m))
    # with open('data1.json', 'r', encoding="utf8") as f:
    # data = json.load(f)

    # l = hh.get_employers()
    # print(l)


