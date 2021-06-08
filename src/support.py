# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import requests

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

        deputy_info_url_call = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}'.format(deputy_id)
        response = requests.get(deputy_info_url_call)
        data = response.json()

        return data['dados']
