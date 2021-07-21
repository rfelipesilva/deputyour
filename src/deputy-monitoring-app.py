# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from streamlit_timeline import timeline

from support import Data

st.set_page_config(page_title="My App",layout='wide')

deputy_dict = Data.get_deputy_dict()

def get_bar_chart(dataframe):
    fig = px.line(dataframe, x='month', y='value', color='cost', width=1350)
    return fig

def get_cost_charts(deputy_id):

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
    cost_selected = cost_col1.selectbox('Select the cost type to analyze:',
                                        list(target_deputy_cost.cost_type.unique()))
    year_selected = cost_col2.selectbox('Select the year to analyze:', 
                                        list(target_deputy_cost.year.unique()))
    costs_df_filtered = cost_data.loc[(cost_data.cost_type == cost_selected) 
                                       & (cost_data.year == year_selected)]
    st.write(costs_df_filtered)
    st.plotly_chart(get_bar_chart(costs_df_filtered))

st.header('Deputy monitoring')
deputy_id = st.selectbox('Selecione o deputado:', list(deputy_dict.keys()))

st.markdown("""***""")

col1, col2 = st.beta_columns(2)

if deputy_id:
    deputy_info = Data.get_deputy_info(deputy_dict[deputy_id])
    col1.header('Main information')
    col1.text('Name: {}'.format(deputy_info['ultimoStatus']['nome']))
    col1.text('Party: {}'.format(deputy_info['ultimoStatus']['siglaPartido']))
    col1.text('State: {}'.format(deputy_info['ultimoStatus']['siglaUf']))
    col1.text('E-mail: {}'.format(deputy_info['ultimoStatus']['email']))
    # col1.text('Birth date: {}'.format(deputy_info['dataNascimento']))
    col1.text('Age: {}'.format(deputy_info['age']))
    #col1.text('Today date: {}'.format(deputy_info['age']))
    col1.text('Education: {}'.format(deputy_info['escolaridade']))

    col2.header('  ')
    col2.image(deputy_info['ultimoStatus']['urlFoto'], width=180)

    st.markdown("""***""")
    st.header('Career information')
    deputy_occupation = Data.get_deputy_occupation(deputy_dict[deputy_id])
    st.text('Profession: {}'.format(deputy_occupation))

    # st.write(Data.get_deputy_jobs(deputy_dict[deputy_id]))

    deputy_timeline = Data.get_deputy_jobs(deputy_dict[deputy_id])
    timeline(deputy_timeline, height=400)

    st.markdown("""***""")
    st.header('Cost analysis')
    # deputy_costs = Data.get_deputy_costs(deputy_dict[deputy_id])
    get_cost_charts(deputy_dict[deputy_id])
    # st.write(deputy_costs)
