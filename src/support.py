# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import requests
from datetime import date

class Data:

    """Class to centralize and provide any kind of data, path or credential
    """

    def get_deputy_dict():
        """This fuction return a dictionary with deputy name + party abbreviation and id to later be used in other calls
        """

        deputy_url_call = 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome'
        response = requests.get(deputy_url_call)
        data = response.json()

        deputy_dict = {}
        for response_data in data['dados']:
            deputy_name = response_data['nome']
            deputy_party = response_data['siglaPartido']
            deputy_id = response_data['id']
            deputy_dict[deputy_name + ' - ' + deputy_party] = deputy_id
        
        return deputy_dict

    def get_deputy_info(deputy_id):
        """This fuction return dictionary with main information from a specific deputy according to deputy_id parameter
        """
        today = date.today()

        deputy_info_url_call = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}'.format(deputy_id)
        response = requests.get(deputy_info_url_call)
        data = response.json()

        year, month, day = data['dados']['dataNascimento'].split('-')

        birthday = date(int(year), int(month), int(day))

        # data['dados']['age'] = round(int((today - birthday).days) / 365)
        data['dados']['age'] = round(int((today - birthday).days) // 365.2425)

        return data['dados']

    def get_deputy_career(deputy_id):
        """This fuction return dictionary with main career information from a specific deputy according to deputy_id parameter
        """
        # deputy_info_url_call = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}/ocupacoes'.format(deputy_id)
        # response = requests.get(deputy_info_url_call)
        # data = response.json()

        dd = {
            "title": {
                "media": {
                "url": "",
                "caption": "check",
                "credit": ""
                },
                "text": {
                "headline": "Career",
                "text": "<p>Actually, jobs</p>"
                }
            },
            "events": [
                {
                "media": {
                    "url": "",
                    "caption": "Evento test"
                },
                "start_date": {
                    "year": "2010"
                },
                "text": {
                    "headline": "Profissão test",
                    "text": "<br/><p>Trampava bem.</p><br/>"
                }
                }            ]
            }

        return dd
