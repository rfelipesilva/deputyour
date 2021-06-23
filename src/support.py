# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import requests
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

        # dd = {
        #     "title": {
        #         "media": {
        #         "url": "",
        #         "caption": "check",
        #         "credit": ""
        #         },
        #         "text": {
        #         "headline": "Career",
        #         "text": "<p>Actually, jobs</p>"
        #         }
        #     },
        #     "events": [{
        #         "media": {
        #             "url": "",
        #             "caption": "Evento test"
        #         },
        #         "start_date": {
        #             "year": "2010"
        #         },
        #         "end_date": {
        #             "year": "2012"
        #         },
        #         "text": {
        #             "headline": "Profissão test",
        #             "text": "<br/><p>Trampava bem.</p><br/>"
        #         }
        #         }]
        # }

        # return dd
