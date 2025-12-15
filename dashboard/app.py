import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------
# PAGE SETTINGS
# ----------------------------------------------------
st.set_page_config(
    page_title="Uber Trips Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
           
# ----------------------------------------------------
# CUSTOM CSS STYLING
# ----------------------------------------------------
st.markdown("""
<style>
.block-container{
    padding-top: 1rem !important;
}


h1, h2, h3 {
    color: #FFD700 !important;       /* Golden headings */
    font-weight: 900 !important;
}

.stMetric {
    background-color: #111111 !important;
    padding: 20px !important;
    border-radius: 12px !important;
    border: 1px solid #333333 !important;
}

.sidebar .sidebar-content {
    background-color: #101010 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
df = pd.read_csv("uber_cleaned_data.csv")

df["date"] = pd.to_datetime(df["date"])

# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------
st.sidebar.title("🧊 Filters")

month_filter = st.sidebar.multiselect(
    "Select Month",
    sorted(df["month"].unique()),
    default=sorted(df["month"].unique())
)

weekday_filter = st.sidebar.multiselect(
    "Select Weekday",
    sorted(df["weekday"].unique()),
    default=sorted(df["weekday"].unique())
)

base_filter = st.sidebar.multiselect(
    "Select Base",
    sorted(df["dispatching_base_number"].unique()),
    default=sorted(df["dispatching_base_number"].unique())
)

date_filter = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()]
)

# ----------------------------------------------------
# APPLY FILTERS
# ----------------------------------------------------
df_filtered = df[
    (df["month"].isin(month_filter)) &
    (df["weekday"].isin(weekday_filter)) &
    (df["dispatching_base_number"].isin(base_filter)) &
    (df["date"] >= pd.to_datetime(date_filter[0])) &
    (df["date"] <= pd.to_datetime(date_filter[1]))
]

# ----------------------------------------------------
# KPI CALCULATIONS
# ----------------------------------------------------
total_trips = df_filtered["trips"].sum()
busiest_day = df_filtered.loc[df_filtered["trips"].idxmax()]["date"].date()
trips_on_busiest_day = df_filtered["trips"].max()
least_busy_day = df_filtered.loc[df_filtered["trips"].idxmin()]["date"].date()
trips_on_least_busy_day = df_filtered["trips"].min()
most_active_base = df_filtered["dispatching_base_number"].mode()[0]

st.markdown("---")
# ----------------------------------------------------
# KPI DISPLAY
# ----------------------------------------------------
st.title("🚕 Uber Trips Analysis Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Trips", f"{total_trips:,}")
col2.metric("Busiest Day", f"{busiest_day}", f"{trips_on_busiest_day:,}")
col3.metric("Least Busy Day", f"{least_busy_day}", f"{trips_on_least_busy_day:,}")
col4.metric("Most Active Base", most_active_base)

st.markdown("---")

# ----------------------------------------------------
tab1, tab2 = st.tabs(["📊 Charts", "📁 Data"])
# CHARTS
# ----------------------------------------------------

# TRIPS OVER TIME
with tab1: 
   st.subheader("📈 Uber Trips Over Time")
fig1 = px.line(df_filtered, x="date", y="trips", title="", markers=False)
st.plotly_chart(fig1, use_container_width=True)

# TRIPS BY WEEKDAY
st.subheader("📊 Trips per Weekday")
fig2 = px.bar(df_filtered, x="weekday", y="trips")
st.plotly_chart(fig2, use_container_width=True)

# TRIPS PER MONTH
st.subheader("🗓 Trips per Month")
fig3 = px.bar(df_filtered, x="month", y="trips")
st.plotly_chart(fig3, use_container_width=True)

# PIE CHART (TRIPS % BY WEEKDAY)
st.subheader("🍕 Trips Percentage by Weekday")
fig4 = px.pie(df_filtered, names="weekday", values="trips")
st.plotly_chart(fig4, use_container_width=True)
## TAB 2:  DATA PREVIEW
with tab2:
    st.subheader("📁 Filtered Dataset")
    st.dataframe(df_filtered)
    st.download_button(
        label="  download Filtered Data",
    data=df_filtered.to_csv(index=False),
    file_name="uber_filtered_data.csv",mime="text/csv"
    )


