import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="AirBnb-Analysis", page_icon=":bar_chart:", layout="wide")

# Page title and styling
st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Sidebar menu
SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data", "Contact"],
    icons=["house", "bar-chart", "at"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }
)

# ----------------- Home Section ----------------- #
if SELECT == "Home":
    st.header("Airbnb Analysis")
    st.subheader("""
    Airbnb is a San Francisco-based online marketplace for short- and long-term homestays and experiences.
    It revolutionized the tourism industry but also faced criticism for increasing rents in tourist hotspots.
    """)
    st.subheader("Skills Takeaway:")
    st.markdown("- Python Scripting\n- Data Preprocessing\n- Visualization\n- EDA\n- Streamlit\n- MongoDB\n- PowerBI/Tableau")
    st.subheader("Domain:")
    st.markdown("Travel Industry, Property Management, and Tourism")

# ----------------- Explore Data Section ----------------- #
elif SELECT == "Explore Data":
    fl = st.file_uploader(":file_folder: Upload a file", type=["csv", "xlsx"])
    if fl is not None:
        try:
            if fl.name.endswith('.csv'):
                df = pd.read_csv(fl, encoding="ISO-8859-1")
            else:
                df = pd.read_excel(fl)

            st.write(f"Loaded file: **{fl.name}**")
        except Exception as e:
            st.error(f"Error loading file: {e}")
            df = None
    else:
        st.info("Please upload a dataset to proceed.")
        df = None

    if df is not None:
        st.sidebar.header("Choose your filter:")

        # Filters
        neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
        neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df["neighbourhood"].unique())

        filtered_df = df.copy()
        if neighbourhood_group:
            filtered_df = filtered_df[filtered_df["neighbourhood_group"].isin(neighbourhood_group)]
        if neighbourhood:
            filtered_df = filtered_df[filtered_df["neighbourhood"].isin(neighbourhood)]

        # Room type visualization
        room_type_df = filtered_df.groupby("room_type", as_index=False)["price"].sum()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Room Type View Data")
            fig = px.bar(room_type_df, x="room_type", y="price", text_auto=True, template="seaborn")
            st.plotly_chart(fig, use_container_width=True)

        # Neighbourhood group visualization
        with col2:
            st.subheader("Neighbourhood Group View Data")
            fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
            st.plotly_chart(fig, use_container_width=True)

        # Scatter plot
        st.subheader("Neighbourhood and Room Type Data")
        scatter_fig = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
        st.plotly_chart(scatter_fig, use_container_width=True)

        # Table and download buttons
        with st.expander("Detailed View"):
            st.dataframe(filtered_df.head(20))
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Filtered Data", data=csv, file_name="filtered_data.csv", mime="text/csv")

# ----------------- Contact Section ----------------- #
elif SELECT == "Contact":
    st.header("Contact Information")
    st.subheader("Name: Dharanikumar K")
    st.subheader("Email: talktodharan@gmail.com")
    st.subheader("Batch: DT1819")
