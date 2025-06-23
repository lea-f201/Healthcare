import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("malaria_age_cleaned.csv")

st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title("🌍 Global Malaria Mortality Dashboard")

# -------- Sidebar Filters --------
with st.sidebar:
    st.header("Chart Filters")

    # Filters for Age Group Donut
    st.subheader("🧒 Deaths by Age Group")
    country_age = st.selectbox("Country", sorted(df["location"].unique()), index=sorted(df["location"].unique()).index("Chad"), key="country_age")
    year_age = st.selectbox("Year (Age)", sorted(df["year"].unique()), key="year_age")

    # Filters for Sex Donut
    st.subheader("⚥ Deaths by Sex")
    country_sex = st.selectbox("Country", sorted(df["location"].unique()), index=sorted(df["location"].unique()).index("Chad"), key="country_sex")
    year_sex = st.selectbox("Year (Sex)", sorted(df["year"].unique()), key="year_sex")

    # Filters for Bar Chart
    st.subheader("📊 Age-Sex Bar Chart")
    country_bar = st.selectbox("Country", sorted(df["location"].unique()), index=sorted(df["location"].unique()).index("Chad"), key="country_bar")
    year_bar = st.selectbox("Year (Bar)", sorted(df["year"].unique()), key="year_bar")

    # Filters for Map
    st.subheader("🗺️ Map")
    year_map = st.selectbox("Year (Map)", sorted(df["year"].unique()), key="year_map")

    # Filters for Line Chart
    st.subheader("📈 Trend Line")
    country_line = st.selectbox("Country", sorted(df["location"].unique()), index=sorted(df["location"].unique()).index("Chad"), key="country_line")


# -------- Layout (Ultra Compact Version) --------
left_col, right_col = st.columns([1, 2])

# 🔧 Tighter spacing and smaller chart heights
st.markdown("""
    <style>
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        .element-container {
            margin-bottom: 0.2rem;
        }
        .css-1kyxreq {
            padding: 0rem 0rem 0rem 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- LEFT COLUMN (3 stacked compact charts) ---
with left_col:
    # Deaths by Age Group
    filtered_age = df[(df["location"] == country_age) & (df["year"] == year_age)]
    fig_age = px.pie(filtered_age, names="age", values="val", title=f"Deaths by Age Group – {country_age} ({year_age})", hole=0.4)
    fig_age.update_layout(height=200, margin=dict(t=30, b=10))
    st.plotly_chart(fig_age, use_container_width=True)

    # Deaths by Sex
    filtered_sex = df[(df["location"] == country_sex) & (df["year"] == year_sex)]
    grouped_sex = filtered_sex.groupby("sex")["val"].sum().reset_index()
    fig_sex = px.pie(grouped_sex, names="sex", values="val", title=f"Deaths by Sex – {country_sex} ({year_sex})", hole=0.4)
    fig_sex.update_layout(height=200, margin=dict(t=30, b=10))
    st.plotly_chart(fig_sex, use_container_width=True)

    # Deaths by Age and Sex (Bar)
    filtered_bar = df[(df["location"] == country_bar) & (df["year"] == year_bar)]
    fig_bar = px.bar(filtered_bar, x="age", y="val", color="sex", barmode="group",
                     title=f"Deaths by Age and Sex – {country_bar} ({year_bar})")
    fig_bar.update_layout(height=200, margin=dict(t=30, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

# --- RIGHT COLUMN (2 charts vertically aligned with left) ---
with right_col:
    # Choropleth Map
    map_data = df[df["year"] == year_map].groupby("location")["val"].sum().reset_index()
    fig_map = px.choropleth(map_data, locations="location", locationmode="country names",
                            color="val", color_continuous_scale="Blues",
                            title=f"Malaria Deaths by Country – {year_map}", labels={"val": "Deaths"})
    fig_map.update_layout(height=400, margin=dict(t=30, b=10))
    st.plotly_chart(fig_map, use_container_width=True)

    # Trend Line
    line_data = df[df["location"] == country_line].groupby("year")["val"].sum().reset_index()
    fig_line = px.line(line_data, x="year", y="val",
                       title=f"Trend of Malaria Deaths in {country_line}",
                       markers=True, labels={"val": "Deaths"})
    fig_line.update_layout(height=200, margin=dict(t=30, b=10))
    st.plotly_chart(fig_line, use_container_width=True)
