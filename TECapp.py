# import packages
import streamlit as st
import pandas as pd
from datetime import datetime
import data_loader
import artist



# ++++++++++++++++++++++++++++++++++++++++++ Configure page and Properties +++++++++++++++++++++++++++++++++++++++++
st.set_page_config(
    page_title="📊TEC Register Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "mailto:john.e.omage@gmail.com",
        "Report a bug": "mailto:john.e.omage@gmail.com",
        "About": "# Want to reach out?!",
    },
)


# set page title
st.title(f":bulb: NGET Transmission Entry Capacity Register Dashboard: 2019 - 2038\nData Last Updated: {data_loader.extract_last_date_updated()}")


# Fetch data
@st.cache_data
def load_data():
    return data_loader.download_data()

raw_data = load_data()



# +++++++++++++++++++++++++++++++ SIDE BAR FILTERS and DATA +++++++++++++++++++++++++++++++++++
def create_sidebar_filter(label, feature, placeholder):
    return st.sidebar.multiselect(
                                label=label,
                                options=raw_data[feature].unique(),
                                default=raw_data[feature].unique(),
                                placeholder=placeholder)

to_filter = create_sidebar_filter(label='Trasmission Owner',
                            feature='HOST TO',
                            placeholder='Choose TO')
project_status_filter = create_sidebar_filter(label='Project Status',
                                              feature='Project Status',
                                              placeholder='Choose Project Status')
agreement_filter = create_sidebar_filter(label='Agreement Type',
                                         feature='Agreement Type',
                                         placeholder='Choose Agreement Type')


data = raw_data[raw_data['HOST TO'].isin(to_filter)
                & raw_data['Project Status'].isin(project_status_filter)
                & raw_data['Agreement Type'].isin(agreement_filter)]



# +++++++++++++++++++++++++++++++ ALL DATA +++++++++++++++++++++++++++++++++++

st.write(f"Showing {data.shape[0]} Projects")
st.dataframe(data)
# st.plotly_chart