# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import requests
import pandas as pd
from datetime import date

class Data:

    """Class to centralize and provide any kind of data, path or credential
    """

    def get_deputy_dict():
        """This fuction return a dictionary with deputy name + party abbreviation 
           and id to later be used in other calls
        """

        url_call = 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome'
        response = requests.get(url_call)
        data = response.json()

        deputy_dict = {}
        for response_data in data['dados']:
            deputy_name = response_data['nome']
            deputy_party = response_data['siglaPartido']
            deputy_id = response_data['id']
            deputy_dict[deputy_name + ' - ' + deputy_party] = deputy_id
        
        return deputy_dict

    def get_deputy_info(deputy_id):
        """This fuction return dictionary with main information 
           from a specific deputy according to deputy_id parameter
        """
        today = date.today()

        url_call = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}'
        response = requests.get(url_call)
        data = response.json()

        year, month, day = data['dados']['dataNascimento'].split('-')
        birthday = date(int(year), int(month), int(day))
        # data['dados']['age'] = round(int((today - birthday).days) / 365)
        data['dados']['age'] = round(int((today - birthday).days) // 365.2425)

        return data['dados']

    def get_deputy_occupation(deputy_id):
        """this function returns the occupation from a specific deputy 
           according to deputy_id parameter, if deputy has declared any
        """
        url_call = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/profissoes'
        response = requests.get(url_call)
        data = response.json()

        occupations = [occupation['titulo'] for occupation in data['dados']]

        if occupations:
            return ' / '.join(occupations)
        else:
            return False

    def get_deputy_jobs(deputy_id):
        """this function returns a dictionary with information for each job performed 
           by the deputy according to deputy_id parameter, if deputy has declared any
        """
        url_call = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/ocupacoes'
        response = requests.get(url_call)
        data = response.json()

        jobs = {
            'title':{
                "media": {
                    "url": "",
                    "caption": "check",
                    "credit": ""
                },
                'text': {
                    'headline': 'Career',
                    'text': "Let's check the jobs your deputy has declared?"
                }
            }
        }

        events = []

        for job in data['dados']:
            event = {
                'media': {
                    'url': '',
                    'caption': ''
                },
                'start_date': {
                    'year': job['anoInicio']
                },
                'end_date': {
                    'year': job['anoFim']
                },
                'text': {
                    'headline': job['titulo'],
                    'text': f"<br/><p>Entidade: {job['entidade']}</p><br/>"
                }
            }
            events.append(event)
        jobs['events'] = events
        
        return jobs

    def get_deputy_costs(deputy_id):
        """this function returns the costs from a specific deputy 
           according to deputy_id parameter
        """
        api = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/'
        years = [2019, 2020, 2021]

        dfs_to_contact = []
        
        for year in years:
            method = f'despesas?ano={year}&ordem=ASC&ordenarPor=ano'
            url_call = api + method
            response = requests.get(url_call)
            
            data = response.json()

            cost_year, cost_month, cost_type, cost_value, cost_code = [], [], [], [], []

            for costs in data['dados']:
                cost_year.append(costs['ano'])
                cost_month.append(costs['mes'])
                cost_type.append(costs['tipoDespesa'])
                cost_value.append(costs['valorDocumento'])
                cost_code.append(costs['codDocumento'])

                df = pd.DataFrame({'year': cost_year, 'month': cost_month, 'cost_type': cost_type, 
                                   'value': cost_value, 'cost_code': cost_code})
                dfs_to_contact.append(df)

        costs_df = pd.concat(dfs_to_contact).drop_duplicates()

        return costs_df