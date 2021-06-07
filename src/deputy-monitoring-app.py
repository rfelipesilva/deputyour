# @author: Renan Silva
#? @github: https://github.com/rfelipesilva
#! Python3.8

import streamlit as st

from support import Data

deputy_list = list(Data.get_deputy_dict().keys())

st.header('Deputy monitoring')
st.selectbox('Selecione o deputado:', deputy_list)