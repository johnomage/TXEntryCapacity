# import packages
import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import download_data, preprocess_df, extract_last_date_updated, get_date_range
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


# Fetch data
@st.cache_data
def load_data():
    return preprocess_df(download_data())

raw_data = load_data()

# set page title
st.title(f":bulb: NESO Transmission Entry Capacity Register Dashboard: {get_date_range(raw_data)}\nData Last Updated: {extract_last_date_updated()}")




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


# +++++++++++++++++++++++++++++++ CARDS ++++++++++++++++++++++++++++++++++++++

"---"
def format_MW_GW(capacity: float, feature: str, is_capacity=True):
    """
    Format and display capacity in KW or MW using based on capacity's value.

    Converts the input value to MW if it's 1000 or greater,
    otherwise displays it in KW. Uses Streamlit to render
    the formatted capacity with HTML styling.

    Args:
        value (float): Capacity value in KW
        feature (string): Name of capacity feature to convert
    """
    st.markdown(f"<h3 style='text-align: center;'>{feature}</h3>", unsafe_allow_html=True)
    if is_capacity:
        cap_value = capacity / 1000
        if cap_value < 1:  # Display in MW
            st.markdown(f"<h3 style='text-align: center;'>{capacity:.2f} MW</h3>", unsafe_allow_html=True,)
        else:  # Display in GW
            st.markdown(f"<h3 style='text-align: center;'>{cap_value:.4f} GW</h3>", unsafe_allow_html=True)
    else:
         st.markdown(f"<h3 style='text-align: center;'>{capacity}</h3>", unsafe_allow_html=True)


project_count_card, to_count_card, mw_change_card, connect_cap_card = st.columns(4)
with project_count_card:
    format_MW_GW(data.shape[0], 'Total Projects', False)
with to_count_card:
    format_MW_GW(data['HOST TO'].nunique(), 'Network Owners', False)
with mw_change_card:
    format_MW_GW(data['MW Change'].sum(), 'Capacity Change')
with connect_cap_card:
    format_MW_GW(data['Connection Cap (MW)'].sum(), 'Total Capacity')

"---"

def add_sub_title(title: str, desciption: str=None):
    st.markdown(f"<h3 style='text-align: center;'>{title}</h3>", unsafe_allow_html=True)
    if desciption:
        st.markdown(desciption, unsafe_allow_html=True)
    
    
#                                        +++++++++++++++++++++++++++++++ ALL CHARTS +++++++++++++++++++++++++++++++++++

# Bar Chart for Connection Capacity by Plant Type and Network Owner
plant_type_description = "CCGT (Combined Cycle Gas Turbine) plants, including various configurations, account for a total of approximately 36.93GW connected primarily to NGET. \
                         Energy Storage Systems dominate with an impressive total of 134.54GW, showcasing their critical role in stabilizing the grid and integrating renewable \
                         energy sources.  Wind Offshore plants show a substantial capacity of 127.28GW, indicating their pivotal role in the current energy mix. They are \
                         well-represented across all connections, especially NGET and SHET. Wind Onshore contributes a capacity of 28.95 GW, reinforcing the importance of both \
                         offshore and onshore wind in the renewable sector. Conventional sources like Coal, Oil & AGT, and Gas Reciprocating show relatively low contributions (e.g., 2.05GW, 61.5 MW, and 661.78 MW respectively).\
                         This trend reflects a broader shift towards cleaner energy sources. Nuclear Power provides a significant capacity of 19.09 GW, still an essential \
                         component of the low-carbon energy landscape."


add_sub_title('Connection Capacity by Plant Type and Network Owner', plant_type_description)
st.plotly_chart(artist.plot_plant_type_cap(data), use_container_width=True)
"---"


# Sunburst Chart for Connection Capacity by Host TO, Plant Type, and Project Status
sun_title = "Connection Capacity by Host TO, Plant Type, and Project Status"
add_sub_title(sun_title)
st.plotly_chart(artist.plot_sunburst(data), use_container_width=True)
"---"


# Doughtnut Chart for Connection Capacity distribution by Project Status and by HOST TO
doughtnut_title = "Connection Capacity distribution by Project Status and by HOST TO"
doughtnut_description = "The analysis of energy projects by connection capacity reveals \
                         a substantial pipeline, particularly in the scoping phase with 459.84 GW \
                         across 1,254 projects, indicating significant future generation potential. \
                         In contrast, built projects contribute 76.58 GW (312 projects), while 58.67 GW \
                         (157 projects) are awaiting consents, highlighting potential delays in capacity \
                         addition. With consents approved for 38.34 GW (148 projects) and just 11.42 GW \
                         (25 projects) under construction, the data suggests a pressing need to expedite \
                         projects through approvals and construction to meet future energy demands effectively."
add_sub_title(doughtnut_title, doughtnut_description)
st.plotly_chart(artist.plot_conn_capa_dist_by_status_host(data), use_container_width=True)
"---"


# Grouping the data by 'Connection Date'
line_title = "Timeline of Connection Capacity, Projects, Plant Types, and MW Change"
line_description = "The dataset provides a comprehensive overview of energy projects and their connection details from 2019 to 2038, \
                    showcasing a diverse range of initiatives across various plant types and host transmission systems including NGET, \
                    SHET, and SPT. It reveals significant capacity changes, with notable increases in megawatt capacity, particularly \
                    from 2023 onwards. The data indicates peak connection activities around the end of financial quarters, suggesting \
                    strategic planning aligned with fiscal year ends. Large capacity connections, especially in late 2024 and early 2026, \
                    point to substantial expansions in energy infrastructure. The dataset projects continued growth in energy capacity \
                    through 2028, reflecting robust plans to meet increasing energy demands and suggesting a strong commitment to enhancing \
                    and diversifying the energy landscape in the coming years."
add_sub_title(line_title, line_description)
st.plotly_chart(artist.plot_timelines(data), use_container_width=True)
"---"



# +++++++++++++++++++++++++++++++ ALL DATA and CELEBRATE +++++++++++++++++++++++++++++++++++

st.write(f"Table Showing {data.shape[0]} Projects")
st.dataframe(data)
# celebrate = lambda : st.balloons()
left, middle, right = st.columns([1, 6, 1])

#right column for the button
with right:
    # CSS to align the button to the right
    st.markdown(
        """
        <style>
        div.stButton > button {
            float: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    if st.button('Celebrate'):
        st.balloons()
