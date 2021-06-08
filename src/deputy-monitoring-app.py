# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import streamlit as st

from support import Data

deputy_dict = Data.get_deputy_dict()

st.header('Deputy monitoring')
deputy_id = st.selectbox('Selecione o deputado:', list(deputy_dict.keys()))

col1, col2 = st.beta_columns(2)

if deputy_id:
    deputy_info = Data.get_deputy_info(deputy_dict[deputy_id])
    col1.text('Name: {}'.format(deputy_info['ultimoStatus']['nome']))
    col1.text('Party: {}'.format(deputy_info['ultimoStatus']['siglaPartido']))
    col1.text('State: {}'.format(deputy_info['ultimoStatus']['siglaUf']))
    col1.text('E-mail: {}'.format(deputy_info['ultimoStatus']['email']))
    col1.text('Birth date: {}'.format(deputy_info['dataNascimento']))
    col1.text('Education: {}'.format(deputy_info['escolaridade']))

    col2.image(deputy_info['ultimoStatus']['urlFoto'], width=150)