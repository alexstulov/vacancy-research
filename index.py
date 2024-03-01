import requests
from urllib import parse
import time
import os
import math
import pandas as pd
from datetime import datetime

REQUEST_PAUSE = 0.2 # experimental pause not to bump into requests/minute limit

log_file = open('aggregation_errors.log','w+')

class VacancyAggregator:
    baseUrl = 'https://api.hh.ru/vacancies/'
    totalPages = float('inf')
    vacancies = {}
    preparedVacancies = []
    professional_role = 10
    params = {}
    
    def make_a_list(self):
        return []
    
    def make_a_dictionary(self):
        return {}
    
    def __init__(self, role = 10):
        self.professional_role = role
        self.params = {
            'area': 1, # 1 - москва
            'professional_role': role,
                # 10 - аналитик
                # 134 - финансовый аналитик, инвестиционный аналитик
                # 156 - BI-аналитик, аналитик данных
                # 163 - маркетолог-аналитик
                # 164 - продуктовый аналитик
            'per_page': 100
        }
        self.vacancies = self.make_a_dictionary()
        self.preparedVacancies = self.make_a_list()
        print('VacancyAggregator constructed')
        
    def getVacancy(self, url):
        data = dict()
        try:
            1/0
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                print('ok', url)
            else:
                print('not ok', response.status_code, url)
                log_file.write(f'non-200 status code: {response.status_code}, url: {url}, time: {datetime.now()}\n')
            response.close()
        except Exception as exc:
            print(f'{url} made exception: {exc}')
            log_file.write(f'something went wrong: {exc}, url: {url}, time: {datetime.now()}\n')
        return data
    
    def getVacancies(self, url):
        print(f'getting vacancies for {self.professional_role} and params: {self.params}')
        data = {}
        try:
            response = requests.get(url)
            data = response.json()
        except Exception as exc:
            print(f'{url} made exception: {exc}')
            log_file.write(f'something went wrong: {exc}, url: {url}, time: {datetime.now()}\n')
        if (math.isinf(self.totalPages)):
            self.totalPages = data['pages']
        if 'items' not in data:
            print(url, ' failed to load data')
            response.close()
            log_file.write(f'no required items found in response, url: {url}, time: {datetime.now()}\n')
            return    
        for item in data['items']:
            time.sleep(REQUEST_PAUSE)
            details = self.getVacancy(self.baseUrl + item['id'])
            newVacancy = {**item, **details}
            self.vacancies[item['id']] = newVacancy
        response.close()
        
    def prepareVacancy(self, vacancyId, vacancy):
        if vacancy['salary'] != None:
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
        else:
            salary_from = None
            salary_to = None
        if vacancy['address'] != None:
            address_raw = vacancy['address']['raw']
        else:
            address_raw = None
        if 'key_skills' in vacancy and vacancy['key_skills'] != None:
            def getSkillName(skill):
                return skill['name']
            keySkills = ','.join(map(getSkillName, vacancy['key_skills']))
        else:
            keySkills = ''
        if 'description' in vacancy and vacancy['description'] != None:
            description = vacancy['description']
        else:
            description = ''
        self.preparedVacancies.append([
            vacancy['id'],
            vacancy['premium'],
            vacancy['name'],
            vacancy['has_test'],
            vacancy['response_letter_required'],
            vacancy['area']['id'],
            vacancy['area']['name'],
            salary_from, 
            salary_to,
            vacancy['type']['name'],
            address_raw,
            vacancy['response_url'],
            vacancy['sort_point_distance'],
            vacancy['published_at'],
            vacancy['created_at'],
            vacancy['archived'],
            description,
            keySkills,
            vacancy['apply_alternate_url'],
            vacancy['insider_interview'],
            vacancy['url'],
            vacancy['alternate_url'],
            vacancy['relations'],
            vacancy['employer']['name'],
            vacancy['snippet']['requirement'],
            vacancy['snippet']['responsibility'],
            vacancy['contacts'],
            vacancy['schedule']['name'],
            vacancy['working_days'],
            vacancy['working_time_intervals'],
            vacancy['working_time_modes'],
            vacancy['accept_temporary']
        ])
        
    def saveToXlsx(self):
        os.makedirs('./data/', exist_ok=True)

        for vacancyId, vacancy in self.vacancies.items():
            self.prepareVacancy(vacancyId, vacancy)

        vacanciesDF = pd.DataFrame(self.preparedVacancies,
            columns = [
                'id',
                'premium',
                'name',
                'has_test',
                'response_letter_required',
                'area_id',
                'area_name',
                'salary_from', 
                'salary_to',
                'type_name',
                'address_raw',
                'response_url',
                'sort_point_distance',
                'published_at',
                'created_at',
                'archived',
                'description',
                'key_skills',
                'apply_alternate_url',
                'insider_interview',
                'url',
                'alternate_url',
                'relations',
                'employer_name',
                'snippet_requirement',
                'snippet_responsibility',
                'contacts',
                'schedule_name',
                'working_days',
                'working_time_intervals',
                'working_time_modes',
                'accept_temporary'
            ]
        )
        vacanciesDF.to_excel(f'./vacancies/vacancies-{self.professional_role}.xlsx')
    
    def aggregateInfo(self):
        # get totalPages with first request
        self.getVacancies('?'.join([
            self.baseUrl,
            parse.urlencode({
                **self.params,
                'page': 0
            })
        ]))

        urls = []
        for i in range(1, self.totalPages+1):
            urls.append(self.baseUrl + '?' + parse.urlencode({
                **self.params,
                'page': i
            }))
        for url in urls:
            self.getVacancies(url)
