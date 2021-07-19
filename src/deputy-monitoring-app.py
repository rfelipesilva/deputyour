# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import streamlit as st
import plotly.express as px

from streamlit_timeline import timeline

from support import Data

st.set_page_config(page_title="My App",layout='wide')

deputy_dict = Data().get_deputy_dict()

def get_bar_chart(dataframe):
    fig = px.bar(dataframe, x='month', y='value', width=800)
    return fig
    #st.plotly_chart(fig)

def get_cost_charts(deputy_id):

    deputy_costs = Data().get_deputy_costs(deputy_id)
    st.write(deputy_costs)
    # deputies_full_costs = Data.get_full_costs()

    cost_col1, cost_col2 = st.beta_columns(2)

    cost_selected = cost_col1.selectbox('Select the cost type to analyze:', list(deputy_costs.cost_type.unique()))
    year_selected = cost_col2.selectbox('Select the year to analyze:', list(deputy_costs.year.unique()))
    costs_filtered = deputy_costs.loc[(deputy_costs.cost_type == cost_selected) & (deputy_costs.year == year_selected)]
    cost_col1.write(costs_filtered)
    # cost_col1.plotly_chart(get_bar_chart(costs_filtered))
    # cost_col2.write(deputies_full_costs)

st.header('Deputy monitoring')
deputy_id = st.selectbox('Selecione o deputado:', list(deputy_dict.keys()))

st.markdown("""***""")

col1, col2 = st.beta_columns(2)

if deputy_id:
    deputy_info = Data().get_deputy_info(deputy_dict[deputy_id])
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
    deputy_occupation = Data().get_deputy_occupation(deputy_dict[deputy_id])
    st.text('Profession: {}'.format(deputy_occupation))

    # st.write(Data.get_deputy_jobs(deputy_dict[deputy_id]))

    deputy_timeline = Data().get_deputy_jobs(deputy_dict[deputy_id])
    timeline(deputy_timeline, height=400)

    st.markdown("""***""")
    st.header('Cost analysis')
    # deputy_costs = Data.get_deputy_costs(deputy_dict[deputy_id])
    get_cost_charts(deputy_dict[deputy_id])
    # st.write(deputy_costs)
