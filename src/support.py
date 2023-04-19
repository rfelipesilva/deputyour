# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

# import os
import requests
import pandas as pd
from datetime import date
from textblob import TextBlob

def get_translation(string, language_code):
    """Testing textblob

    Args:
        string (str): string to translate
        language_code (str): language code, portuguese -> pt, english -> en

    Returns:
        [type]: [description]
    """
    try:
        blob = TextBlob(string)
        return blob.translate(from_lang='pt', to=language_code)
    except:
        return string

class Data:
    """Class to centralize and provide any kind of data, path or credential
    """
    def get_deputy_dict():
        """This fuction return a dictionary with deputy name + party abbreviation 
           and id to later be used in other calls
        """
        try:
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
        except:
            return False

    def get_deputy_info(deputy_id, language_code):
        """This fuction return dictionary with main information 
           from a specific deputy according to deputy_id parameter
        """
        today = date.today()

        url_call = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}'
        response = requests.get(url_call)
        data = response.json()

        year, month, day = data['dados']['dataNascimento'].split('-')
        birthday = date(int(year), int(month), int(day))
        data['dados']['age'] = round(int((today - birthday).days) // 365.2425)
        data['dados']['escolaridade'] = get_translation(data['dados']['escolaridade'], language_code)

        return data['dados']

    def get_deputy_occupation(deputy_id, language_code):
        """this function returns the occupation from a specific deputy 
           according to deputy_id parameter, if deputy has declared any
        """
        url_call = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{deputy_id}/profissoes'
        response = requests.get(url_call)
        data = response.json()

        occupations = [str(get_translation(occupation['titulo'], language_code)) for occupation in data['dados']]

        if occupations:
            return ' / '.join(occupations)
        else:
            return False

    def get_deputy_jobs(deputy_id, language_code):
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
                    'headline': str(get_translation('Career', language_code)),
                    'text': str(get_translation("Let's check the jobs your deputy has declared?", language_code))
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
                    'headline': str(get_translation(job['titulo'], language_code)),
                    'text': f"<br/><p>Local: {job['entidade']}</p><br/>"
                }
            }
            events.append(event)
        jobs['events'] = events
        
        return jobs

    def get_full_cost():
        """This function returns the full costs per category for all deputies
           for period 2019 up to July 7th, 2021 (2021/06/02)
        """
        #! TO DO: REVIEW LATER
        #! data = pd.read_csv('data/csv/costs_full.csv', encoding='utf-8', delimiter='|')
        #! data_full_grouped = data.groupby(['year','month','cost_type'])['value'].agg(['mean']).reset_index()
        #! data_full_grouped['mean'] = round(data_full_grouped['mean'],2)
        #! data_full_grouped.to_csv('data/costs_deputies_full.csv', encoding='utf-8', sep='|', index=False)

        data = pd.read_csv('data/costs_deputies_full.csv',
                            encoding='utf-8', delimiter='|')
        data.rename(columns={'mean':'value'}, inplace = True)
        data['cost'] = 'mean'
        return data

    def get_deputy_cost(deputy_id):
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

        deputy_costs_df = pd.concat(dfs_to_contact).drop_duplicates()
        deputy_costs_grouped = deputy_costs_df.groupby(['year', 'month', 'cost_type'])['value'].sum().reset_index()
        deputy_costs_grouped['cost'] = 'deputy cost'

        #! TO DO: REVIEW LATER
        #! deputy_costs_grouped.rename(columns={'value':'deputy cost'}, inplace=True)
        #! MERGING MEAN COST WITH SPECIFIC DEPUTY COST
        #! costs_data = deputy_costs_grouped.merge(full_deputies_costs, on=['year', 'month', 'cost_type'], how='left')
        #! costs_df.to_csv('test.csv')
        return deputy_costs_grouped

class Language:
    """Provide dictionary language for English and Portuguese
    """
    def get_lang_dict():
        """Translation to use in the app

        Returns:
            dictionary: for PTBR and EN
        """
        language_dict = {
            'pt': {
                'language': 'pt',
                'sidebar': {
                    'about': {
                        'header': 'Sobre',
                        'text': '''
                            **Deputyour** é um aplicativo desenvolvido por *Renan Silva* que busca facilitar o acesso aos dados dos deputados federais do Brasil.
                            \nGostaria de sugerir melhorias ou comentar sobre o aplicativo? Esses são os canais onde você pode entrar em contato:
                            \n![LinkedIn](https://raw.githubusercontent.com/paulrobertlloyd/socialmediaicons/main/linkedin-16x16.png) [LinkedIn perfil](https://www.linkedin.com/in/renan-silva-16960313a/?locale=en_US)
                            \n![GitHub](https://raw.githubusercontent.com/paulrobertlloyd/socialmediaicons/main/github-16x16.png) TO DO
                        '''
                    }
                },
                'first_section': {
                    'header': 'Você realmente conhece seu deputado?',
                    'desc': 'Comece selecionando seu deputado abaixo, você pode digitar se preferir:'
                },
                'general_info_section': {
                    'header': 'Informações gerais',
                    'name': 'Nome',
                    'party': 'Partido',
                    'state': 'Estado',
                    'email': 'E-mail',
                    'age': 'Idade',
                    'education': 'Grau de escolaridade'
                },
                'career_section': {
                    'header': 'Informações de carreira',
                    'profession': 'Profissão',
                    'error_message': """Parece que o(a) deputado(a) não reportou informações de carreira, 
                                        que tal solicitar essas informações diretamente pelo email?"""
                },
                'cost_section': {
                    'header': 'Análise de custo',
                    'desc': 'Nesta seção, é possível analisar o quanto o deputado está gastando em comparação ao custo médio por tipo de despesa de todos os deputados.',
                    'cost_type_filter': 'Selecione o tipo de despesa',
                    'year_filter': 'Selecione o ano'
                }
            },
            'en': {
                'language': 'en',
                'sidebar': {
                    'about': {
                        'header': 'About',
                        'text': '''
                            **Deputyour** is an app developed by *Renan Silva* that aims to facilitate access to data from federal deputies in Brazil.
                            \nWould you like to share your comments or suggest improvements? Here are the channels to contact:
                            \n![LinkedIn](https://raw.githubusercontent.com/paulrobertlloyd/socialmediaicons/main/linkedin-16x16.png) [LinkedIn profile](https://www.linkedin.com/in/renan-silva-16960313a/?locale=en_US)
                            \n![GitHub](https://raw.githubusercontent.com/paulrobertlloyd/socialmediaicons/main/github-16x16.png) TO DO
                        '''
                    }
                },
                'first_section': {
                    'header': 'Do you really know your deputy?',
                    'desc': "Let's start finding your deputy below, you can type the name if you want:"
                },
                'general_info_section': {
                    'header': 'General information',
                    'name': 'Name',
                    'party': 'Party',
                    'state': 'State',
                    'email': 'E-mail',
                    'age': 'Age',
                    'education': 'Education'
                },
                'career_section': {
                    'header': 'Career information',
                    'profession': 'Profession',
                    'error_message': 'It seems that the deputy did not provide any career information, how about you get in touch via email?'
                },
                'cost_section': {
                    'header': 'Cost analysis',
                    'desc': "Here it's possible to analyze how much the deputy is spending compared to the average cost of the expense type for all deputies",
                    'cost_type_filter': 'Select the cost type',
                    'year_filter': 'Select the year'
                }
            }
        }

        return language_dict

#? USED TO FORMAT FILES
#? Data.get_full_costs()