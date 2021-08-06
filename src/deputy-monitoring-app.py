# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from streamlit_timeline import timeline
from support import Data, Language

st.set_page_config(page_title='Your Deputy', layout='wide', page_icon='🔍')

language = Language.get_lang_dict()
deputy_dict = Data.get_deputy_dict()

# #SETTING OWN THEME COLLOR
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # file_dir = '{}\\style.css'.format(os.path.abspath(os.getcwd()))
# local_css('style.css')

def get_bar_chart(dataframe):
    fig = px.line(dataframe, x='month', y='value', color='cost', width=1350)
    return fig

def get_cost_charts(deputy_id, language_dict):
    target_deputy_cost = Data.get_deputy_cost(deputy_id)
    full_deputies_cost = Data.get_full_cost()

    #? USED TO VALIDATE VALUES
    #? st.write(target_deputy_cost)
    #? st.write(full_deputies_cost)

    #! TO DO: REVIEW THIS BLOCK OF CODE, USED TO ROUND VALUES
    #! cost_data = target_deputy_cost.merge(full_deputies_cost, on=['year', 'month', 'cost_type'], how='left')
    #! cost_data['deputy cost'] = np.round(cost_data['deputy cost'],decimals=2).astype(str)
    #! cost_data['mean'] = np.round(cost_data['mean'],decimals=2).astype(str)

    cost_data = pd.concat([target_deputy_cost, full_deputies_cost])
    cost_col1, cost_col2 = st.beta_columns(2)
    cost_selected = cost_col1.selectbox('{}:'.format(language_dict['cost_section']['cost_type_filter']),
                                        list(target_deputy_cost.cost_type.unique()))

    year_selected = cost_col2.selectbox('{}:'.format(language_dict['cost_section']['year_filter']), 
                                        list(target_deputy_cost.year.unique()))

    costs_df_filtered = cost_data.loc[(cost_data.cost_type == cost_selected) 
                                       & (cost_data.year == year_selected)]

    st.plotly_chart(get_bar_chart(costs_df_filtered))

# @st.cache
def update_page(language_dict):
    """Update app according with specific language

    Args: 
        language_dict (dictionary): Radio button option comingo from "selected_language" variable

    Returns: updated page according with user language selected
    """
    st.sidebar.header(language_dict['sidebar']['about']['header'])
    st.sidebar.info(language_dict['sidebar']['about']['text'])

    st.title('Your Deputy')
    st.subheader(language_dict['first_section']['header'])
    deputy_id = st.selectbox(language_dict['first_section']['desc'], list(deputy_dict.keys()))

    st.markdown("""***""")

    col1, col2 = st.beta_columns(2)

    if deputy_id:
        deputy_info = Data.get_deputy_info(deputy_dict[deputy_id])
        col1.header('{}'.format(language_dict['general_info_section']['header']))
        col1.text('{}: {}'.format(language_dict['general_info_section']['name'],
                                  deputy_info['ultimoStatus']['nome']))

        col1.text('{}: {}'.format(language_dict['general_info_section']['party'],
                                  deputy_info['ultimoStatus']['siglaPartido']))

        col1.text('{}: {}'.format(language_dict['general_info_section']['state'],
                                  deputy_info['ultimoStatus']['siglaUf']))

        col1.text('E-mail: {}'.format(deputy_info['ultimoStatus']['email'])) #NO NEED TO USE DICT HERE

        col1.text('{}: {}'.format(language_dict['general_info_section']['age'],
                                   deputy_info['age']))

        col1.text('{}: {}'.format(language_dict['general_info_section']['education'],
                                         deputy_info['escolaridade']))

        col2.header('  ')
        col2.image(deputy_info['ultimoStatus']['urlFoto'], width=180)

        st.markdown("""***""")
        st.header('{}'.format(language_dict['career_section']['header']))
        st.info('TO DO')
        deputy_occupation = Data.get_deputy_occupation(deputy_dict[deputy_id])
        st.text('{}: {}'.format(language_dict['career_section']['profession'],
                                deputy_occupation))

        deputy_timeline = Data.get_deputy_jobs(deputy_dict[deputy_id])
        timeline(deputy_timeline, height=400)

        st.markdown("""***""")
        st.header('{}'.format(language_dict['cost_section']['header']))
        st.info('TO DO MESSAGE')
        st.text('{}'.format(language_dict['cost_section']['desc']))
        get_cost_charts(deputy_dict[deputy_id], language_dict)

st.sidebar.header('Language/Idioma')
selected_language = st.sidebar.radio('', ['Portuguese/Português', 'English/Inglês'])

if selected_language == 'Portuguese/Português':
    update_page(language['pt'])
else:
    update_page(language['en'])