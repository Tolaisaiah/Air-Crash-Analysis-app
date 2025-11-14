import streamlit as st

import pandas as pd

import plotly.express  as px
import plotly.graph_objects as go

#--Page configuration---
st.set_page_config(
    page_title="✈️ Global Aircrash Analysis Dashboard (1908–2024)",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)
# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        .main {background-color:#(#1f1f2e;}
        .stMetric {background-color:white; border-radius:15px; padding:10px;}
        h1, h2, h3, h4 {color:#1f3c88;}
    </style>
""", unsafe_allow_html=True)

def load_data():
    df = pd.read_csv("cleaned_aircrashes_2024.csv")
    return df

df = load_data()

# --- HEADER ---
st.title("✈️ Global Aircrash Analysis Dashboard (1908 – 2024)")
st.caption("Analyze aviation accident patterns, fatalities, and historical trends")

st.sidebar.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #D3D3D3;   /* Aviation Dark Slate */
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filter Crashes")
# --- Year Dropdown ---
year = st.sidebar.selectbox(
    "Select Year:",
    options= ["All"] + sorted(df["Year"].dropna().unique())
)
# --- Country Dropdown ---
country = st.sidebar.selectbox(
    "Select Country:",
    options= ["All"] + sorted(df["Country/Region"].dropna().unique())
)
# --- Continent Dropdown ---
continent = st.sidebar.selectbox(
    "Select Continent:",
    options= ["All"] + sorted(df["Continent"].dropna().unique())
)
# --- Quarter Dropdown ---
quarter = st.sidebar.selectbox(
    "Select Quarter:",
    options= ["All"] + sorted(df["Quarter"].dropna().unique())
)
# --- APPLY FILTERS ---
filtered_df = df[
    (df["Country/Region"] == country) &
    (df["Year"] == year) &
    (df["Quarter"] == quarter) &
    (df["Continent"] == continent)
]

# KPI section
# --- KPI SECTION (Overall and Filtered) ---


# --- Overall totals ---
total_aboard_all = int(df["Aboard"].sum())
total_fatalities_all = int(df["Fatalities (air)"].sum())
ground_fatalities_all = int(df["Ground"].sum())
total_crashes_all = len(df)
survivors_all = int(df["Survivors"].sum())

# --- Filtered totals ---
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country/Region"] == country]
if year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == year]
if quarter != "All":
    filtered_df = filtered_df[filtered_df["Quarter"] == quarter]
if continent != "All":
    filtered_df = filtered_df[filtered_df["Continent"] == continent]  

total_aboard_filt = int(filtered_df["Aboard"].sum())
total_fatalities_filt = int(filtered_df["Fatalities (air)"].sum())
ground_fatalities_filt = int(filtered_df["Ground"].sum())
total_crashes_filt = len(filtered_df)
survivors_filt = int(filtered_df["Survivors"].sum())



# KPI data and colors
kpis_overall = [
    {"label":"🧍 Total Aboard", "value": total_aboard_all, "color":"#4CAF50"},
    {"label":"💀 Air Fatalities", "value": total_fatalities_all, "color":"#f44336"},
    {"label":"🏠 Ground Fatalities", "value": ground_fatalities_all, "color":"#FF9800"},
    {"label":"✈️ Total Crashes", "value": total_crashes_all, "color":"#2196F3"},
    {"label":"🕊️ Survivors", "value": survivors_all, "color":"#9C27B0"},
]

kpis_filtered = [
    {"label":"🧍 Total Aboard", "value": total_aboard_filt, "color":"#4CAF50"},
    {"label":"💀 Air Fatalities", "value": total_fatalities_filt, "color":"#f44336"},
    {"label":"🏠 Ground Fatalities", "value": ground_fatalities_filt, "color":"#FF9800"},
    {"label":"✈️ Total Crashes", "value": total_crashes_filt, "color":"#2196F3"},
    {"label":"🕊️ Survivors", "value": survivors_filt, "color":"#9C27B0"},
]


# Overall totals
st.markdown("### 🌍 Overall Totals")
cols = st.columns(5)
for col, kpi in zip(cols, kpis_overall):
    col.markdown(f"""
        <div style="
            background-color:{kpi['color']};
            color:white;
            padding:20px;
            border-radius:10px;
            text-align:center;
            font-size:16px;
            font-weight:bold;">
            {kpi['label']}<br>
            <span style="font-size:24px;font-weight:bold;">{kpi['value']:,}</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Filtered view
st.markdown("### 🎯 Filtered View")
cols = st.columns(5)
for col, kpi in zip(cols, kpis_filtered):
    col.markdown(f"""
        <div style="
            background-color:{kpi['color']};
            color:white;
            padding:20px;
            border-radius:10px;
            text-align:center;
            font-size:16px;
            font-weight:bold;">
            {kpi['label']}<br>
            <span style="font-size:24px;font-weight:bold;">{kpi['value']:,}</span>
        </div>
    """, unsafe_allow_html=True)



# Research questions

st.markdown("## 📘 Research Questions")
st.markdown("### **1. How have global air crashes changed over time (1908–2024)?**")

# Group by Year
yearly_trend = df.groupby("Year").size().reset_index(name="Crash_Count")

# Plot line chart with color
fig = px.line(
    yearly_trend,
    x="Year",
    y="Crash_Count",
    title="✈️ Global Air Crash Trend Over Time",
    markers=True,
    line_shape='linear',
)

# Update line color to crimson/red
fig.update_traces(line=dict(color='crimson', width=3), marker=dict(color='crimson'))

# Style layout
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Year",
    yaxis_title="Number of Crashes",
    title_font_size=20,
)

st.plotly_chart(fig, use_container_width=True)

# Research question 2

st.markdown("### **2. Which years recorded the highest number of air crashes and fatalities?**")

# --- Prepare Data ---
yearly_summary = df.groupby("Year").agg(
    Crash_Count=("Year", "count"),
    Total_Fatalities=("Fatalities (air)", "sum")
).reset_index()

# --- Plotly Combined Bar Chart with colors ---
fig = px.bar(
    yearly_summary,
    x="Year",
    y=["Crash_Count", "Total_Fatalities"],
    barmode="group",  # bars side by side
    labels={"value": "Count", "variable": "Metric"},
    title="📊 Total Crashes and Fatalities Per Year",
    color_discrete_map={
        "Crash_Count": "#2196F3",       
        "Total_Fatalities": "#f44336"    
    }
)

# Layout styling
fig.update_layout(
    title_font_size=20,
    xaxis_title="Year",
    yaxis_title="Count",
    legend_title="Metric",
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


# Research question 3

st.markdown("### 3. Top 10 Aircraft Manufacturers by Air Fatalities")

# Use filtered data
data = filtered_df.copy()

manufacturer_col = "Aircraft Manufacturer"  
fatal_col = "Fatalities (air)"  

# Group by manufacturer and sum fatalities
manufacturer_fatalities = (
    data.groupby(manufacturer_col)[fatal_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
)

# Plot column/bar chart
fig = px.bar(
    manufacturer_fatalities,
    x=manufacturer_col,
    y=fatal_col,
    text=fatal_col,
    color=fatal_col,
    color_continuous_scale="Reds",
    title="✈️ Top 10 Aircraft Manufacturers by Air Fatalities"
)

fig.update_layout(
    xaxis_title="Manufacturer",
    yaxis_title="Total Air Fatalities",
    title_font_size=20
)

fig.update_traces(texttemplate='%{text}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)


# Research question 4

st.markdown("### **4. Which countries have recorded the highest number of air crashes?**")

# Group by country
country_crashes = df.groupby("Country/Region").size().reset_index(name="Crash_Count")
# Sort descending
country_crashes = country_crashes.sort_values(by="Crash_Count", ascending=False)
top_countries = country_crashes.head(10)

# Horizontal bar chart with color
fig = px.bar(
    top_countries,
    x="Crash_Count",
    y="Country/Region",
    orientation='h',
    text="Crash_Count",
    title="🛩️ Top 10 Countries by Air Crashes",
    color="Crash_Count",
    color_continuous_scale="Reds"  # gradient from light to dark red
)
fig.update_layout(
    xaxis_title="Number of Crashes",
    yaxis_title="Country",
    yaxis=dict(autorange="reversed"),  # highest at top
    title_font_size=20,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    coloraxis_colorbar=dict(title="Crash Count")
)
st.plotly_chart(fig, use_container_width=True)

#   RESEARCH QUESTION 5


st.markdown("### **5. How do air crash patterns differ by continent?**")

data = filtered_df  

# --- GROUP BY CONTINENT ---
continent_summary = data.groupby("Continent").agg(
    Crash_Count=("Continent", "count"),
    Total_Fatalities=("Fatalities (air)", "sum")
).reset_index()

fig = px.bar(
    continent_summary,
    x="Continent",
    y=["Crash_Count", "Total_Fatalities"],
    barmode="group",
    labels={"value": "Count", "variable": "Metric"},
    title="🌍 Air Crash Patterns by Continent",
    color_discrete_map={
        "Crash_Count": "#2196F3",        
        "Total_Fatalities": "#f44336"    
    }
)
# Layout styling
fig.update_layout(
    title_font_size=20,
    xaxis_title="Continent",
    yaxis_title="Count",
    legend_title="Metric",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

#   RESEARCH QUESTION 6
st.markdown("### **6. Which aircraft types were most involved in crashes?**")

data = filtered_df     

# --- GROUP BY AIRCRAFT TYPE ---
type_crashes = data.groupby("Aircraft").size().reset_index(name="Crash_Count")

# Sort descending
type_crashes = type_crashes.sort_values(by="Crash_Count", ascending=False)

# Take Top 10 for a cleaner funnel
top_types = type_crashes.head(10)
fig = px.funnel(
    top_types,
    x="Crash_Count",
    y="Aircraft",
    title="✈️ Top Aircraft Types Most Involved in Crashes",
)
# Set all bars to crimson
fig.update_traces(marker=dict(color='crimson'))

# Layout styling
fig.update_layout(
    title_font_size=20,
    xaxis_title="Crash Count",
    yaxis_title="Aircraft",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig, use_container_width=True)


#  RESEARCH QUESTION 7

st.markdown("### **7. What is the trend of air fatalities and survivors by quarter?**")
#  USE FILTERED DATA
data = filtered_df.copy()

#  GROUP DATA BY QUARTER
quarter_summary = (
    data.groupby("Quarter")
        .agg(Fatalities=("Fatalities (air)", "sum"),
             Survivors=("Survivors", "sum"))
        .reset_index()
)

# Ensure quarters are in correct order
quarter_order = ["Qtr 1", "Qtr 2", "Qtr 3", "Qtr 4"]
quarter_summary["Quarter"] = pd.Categorical(quarter_summary["Quarter"], categories=quarter_order, ordered=True)
quarter_summary = quarter_summary.sort_values("Quarter")

#  MELT TO LONG FORM
long_df = quarter_summary.melt(
    id_vars="Quarter",
    value_vars=["Fatalities", "Survivors"],
    var_name="Metric",
    value_name="Count"
)
#  CREATE SCATTER PLOT
fig = px.scatter(
    long_df,
    x="Quarter",
    y="Count",
    color="Metric",
    labels={"Count": "Number of People", "Quarter": "Quarter"},
    title="📊 Trend of Air Fatalities and Survivors by Quarter",
    color_discrete_map={"Fatalities": "red", "Survivors": "green"}
)
fig.update_traces(mode="markers+lines")
fig.update_layout(title_font_size=20, xaxis_title="Quarter", yaxis_title="Count", legend_title="Metric")

st.plotly_chart(fig, use_container_width=True)



#   RESEARCH QUESTION 8

st.markdown("### **8. What share of total survivors came from each continent?**")

#  FILTERED DATA
data = filtered_df.copy()


#  GROUP BY CONTINENT
survivors_by_continent = (
    data.groupby("Continent")["Survivors"]
        .sum()
        .reset_index()
        .sort_values("Survivors", ascending=False)
)


#  CREATE DOUGHNUT CHART
fig_survivors = go.Figure(
    go.Pie(
        labels=survivors_by_continent["Continent"],
        values=survivors_by_continent["Survivors"],
        hole=0.4,  # doughnut effect
        textinfo="percent+label",
        textposition="inside",
        pull=[0.05]*len(survivors_by_continent),
        marker=dict(
            colors=[
                "#1f77b4", "#ff7f0e", "#2ca02c",
                "#d62728", "#9467bd", "#8c564b"
            ],
            line=dict(color="black", width=1)
        )
    )
)

fig_survivors.update_layout(
    title="🌍 Share of Total Survivors by Continent",
    title_font_size=20,
    legend_title_text="Continent",
    height=450,
    width=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_survivors, use_container_width=True)


# Research Question 9

st.markdown("### 9. Moving average of survivors for Top 5 aircraft manufacturers over time")

# Filtered data
data = filtered_df.copy()

manufacturer_col = "Aircraft Manufacturer" 


# --- Select top 10 manufacturers by total survivors ---
top_manufacturers = (
    data.groupby(manufacturer_col)["Survivors"].sum()
        .sort_values(ascending=False)
        .head(5)
        .index
)

data_top5 = data[data[manufacturer_col].isin(top_manufacturers)]

# Sort by date
data_top5 = data_top5.sort_values("Date")

# Group by Date and Manufacturer
daily_summary = (
    data_top5.groupby(["Date", manufacturer_col])["Survivors"]
        .sum()
        .reset_index()
)

# Calculate 7-day moving average
daily_summary["Moving_Avg"] = (
    daily_summary.groupby(manufacturer_col)["Survivors"]
    .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
)


# Define colors for each manufacturer
top5_list = daily_summary[manufacturer_col].unique()
color_map = {
    top5_list[0]: "#1f77b4",
    top5_list[1]: "#ff7f0e",
    top5_list[2]: "#2ca02c",
    top5_list[3]: "#d62728",
    top5_list[4]: "#9467bd"
}
fig = px.line(
    daily_summary,
    x="Date",
    y="Moving_Avg",
    color=manufacturer_col,
    labels={"Moving_Avg": "Survivors (7-day MA)", "Date": "Date"},
    title="📈 Moving Average of Survivors by Top 5 Manufacturers",
    markers=True,
    color_discrete_map=color_map  # assign specific colors
)
# Thicker lines and layout adjustments
fig.update_traces(line=dict(width=4))
fig.update_layout(
    title_font_size=24,
    xaxis_title="Date",
    yaxis_title="Number of Survivors",
    legend_title="Manufacturer",
    hovermode="x unified",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig, use_container_width=True)

# Question 11
st.markdown("### **10. How does the air-crash survival rate vary across countries?**")

data = filtered_df.copy()

# --- Calculate survival rate ---
country_survival = (
    data.groupby("Country/Region")
        .agg(
            Survivors=("Survivors", "sum"),
            Fatalities=("Fatalities (air)", "sum"),
            Aboard=("Aboard", "sum")
        )
        .reset_index()
)

# Avoid division errors
country_survival["Survival_Rate"] = (
    country_survival["Survivors"] / country_survival["Aboard"]
).fillna(0) * 100

# Rename for easier mapping
country_survival.rename(columns={"Country/Region": "Country"}, inplace=True)

# --- Choropleth Map ---
fig = px.choropleth(
    country_survival,
    locations="Country",
    locationmode="country names",
    color="Survival_Rate",
    hover_name="Country",
    hover_data={
        "Survivors": True,
        "Fatalities": True,
        "Aboard": True,
        "Survival_Rate": ":.2f"
    },
    color_continuous_scale="greens",
    title="🌍 Global Air-Crash Survival Rate by Country (%)"
)

fig.update_layout(
    title_font_size=20,
    geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("### 📋 Survival Rate Table")

st.dataframe(
    country_survival[["Country", "Survivors", "Fatalities", "Aboard", "Survival_Rate"]]
        .sort_values(by="Survival_Rate", ascending=False)
)

# --- Findings Section ---
st.markdown("## 📊 Findings")

# Global Air Crash Trends
st.markdown("### 1. ✈️ Global Air Crash Trends")
st.markdown("""
- **Early 1900s–1940s:** Air crashes increased steadily as aviation technology and commercial flights expanded.  
- **1945–1970:** The highest crash frequency occurred, with several years exceeding **70–80 crashes/year**, likely due to rapid growth of commercial aviation and post-war developments.  
- **1970s onward:** Crash numbers began a gradual decline, reflecting improvements in aircraft design, safety regulations, and air traffic control.  
- **2000–2024:** Sharp and consistent decrease in crashes, reaching historically low levels of **fewer than 10 crashes/year**, demonstrating significant advancements in aviation safety.
""")

st.markdown("### 2. Total Crashes and Fatalities Per Year")
st.markdown("""
- **Trend Similarity:** Fatalities follow a similar trend to crashes but show **major spikes** in certain years.
- **Spike Periods:** Late 1950s–1960s, Late 1970s, Early 1980s, Early 1990s
- **High-Fatality Years:** Some years recorded over **2,000–2,800 fatalities**, often due to **one or two large catastrophic accidents**.
- **Recent Decades:** Crashes and fatalities have **dropped significantly**, even as **global air traffic increased** dramatically.
""")

# --- Findings for Top 10 Aircraft Manufacturers ---
st.markdown("### 3. Top 10 Aircraft Manufacturers by Air Fatalities")
st.markdown("""
- **Highest Fatalities:** McDonnell Douglas and Boeing account for the most air fatalities historically (**24,406** and **20,583**, respectively).  
- **Older Manufacturers:** Lockheed, Antonov, Tupolev, Ilyushin show high totals due to older aircraft designs, military use, and less stringent safety regulations during peak production years.  
- **Modern Manufacturers:** Airbus, despite widespread use, has comparatively lower totals, reflecting advances in safety and newer fleet age.
""")

st.markdown("""
### 4. ✈️ Air Crash Patterns by Continent
- **Highest Fatalities:** Europe and Asia lead with totals near or above **30,000 fatalities**. North America and Africa follow with **15,000–20,000 fatalities**.  
- **Crash vs Fatalities:** Across all continents, fatalities far exceed crash counts, indicating many crashes involve large loss of life.  
- **Lowest Counts:** Oceania and South America have the lowest totals, each under **15,000 fatalities**.

### 5. 🌍 Top 10 Countries by Air Crashes
- **Leader:** The United States recorded **844 crashes**, far higher than any other country.  
- **Second Place:** Russia with **256 crashes**.  


### 6.🛩️ Top Aircraft Types Involved in Crashes
- **Most Involved:** The Douglas DC-3 with **549 crashes** dominates the list.  
- **Disparity:** DC-3 crashes are over **six times higher** than the second most involved aircraft, the De Havilland Canada DHC-6 Twin Otter (**90 crashes**).  
- **Manufacturers:** Older aircraft models from **Douglas** and **Boeing** dominate the crash data.
""")

st.markdown("""
### 📉 7. Trend of Air Fatalities and Survivors by Quarter
- **Fatalities consistently exceed survivors** in every quarter.  
- **Quarter 3** shows the highest counts for both fatalities (**~30,000**) and survivors (**~13,000**).  
- **Quarter 2** records the lowest totals (fatalities **~24,000**, survivors **~9,500**).  
- Survivors remain fairly stable from Q1 → Q2 before rising in Q3, while fatalities dip from Q1 → Q2, then sharply spike in Q3.  
- Both metrics decline slightly in **Quarter 4**.


### 🌍 8. Share of Total Survivors by Continent
- **Asia leads** with **30%** of global survivors, followed by **North America (23.6%)** and **Europe (22.1%)**.  
- These three continents account for **~75.7%** of all survivors.  
- **Africa** contributes **15%**, while **South America** is lower at **7.6%**.  
- **Oceania and Unknown** regions represent minimal shares.


### ✈️ 9. Moving Average of Survivors by Top 5 Aircraft Manufacturers
- Before the **1980s**, all manufacturers recorded **low, stable survivor averages** (typically under 50).  
- **Airbus shows a major spike** in the late 1970s–early 1980s, reaching **~250**, the highest moving average among all manufacturers.  
- From the **1990s to early 2010s**, Boeing, McDonnell Douglas, and Airbus show **frequent peaks** between **50–150 survivors**.  
- After **2015**, averages stabilize below **100**, with Boeing showing the most activity (peaks up to **~80**).  
- **Lockheed and Tupolev** maintain relatively **lower survivor averages** across the entire timeline.
        

### 🗺️ 10. Survival Rate by Country
- **Highest Survival Rates:**  
  - **Moldova** leads with a **67.37%** survival rate (223 survivors out of 331 aboard).  
  - **Armenia** follows with **61.43%** (266 survivors out of 433 aboard).  
- **Mid-Range Performers:**  
  - **Singapore (59.06%)**, **Luxembourg (58.87%)**, and **Guadeloupe (57.72%)** maintain strong rates above **55%**.  
- **Major Contributor Example:**  
  - **Japan**, with the highest observed number aboard (**2,895**), achieves a **55.72%** survival rate (1,613 survivors).  
- **Lower Range in Top 10:**  
  - **Ghana** records the lowest visible survival rate at **52.55%** (175 survivors out of 333 aboard).             

""")

st.markdown("""
### 🛠️ Recommendations for Improving Global Aviation Safety (1908–2024)

Based on over a century of air crash data, the following five recommendations represent the most impactful strategies for strengthening global aviation safety:


 **1. Modernize and Replace Aging Aircraft Fleets**
Retire older aircraft models especially legacy types such as DC series, early Boeing models, and aging Soviet era aircraft.  
Invest in modern fleets equipped with advanced avionics, improved structural integrity, and real time safety monitoring systems.


 **2. Strengthen Aviation Oversight in High Risk Regions**
Expand international safety audits and provide technical and regulatory support to regions with historically high crash and fatality rates.  
Enhance ICAO compliance and ensure consistent implementation of global safety standards.

 **3. Improve Pilot Training and Human Factors Programs**
Increase investment in simulator based emergency training, Crew Resource Management (CRM), and updated cockpit communication protocols.  
Human error remains a major cause of crashes, and enhanced training can significantly reduce risk.

 **4. Enhance Emergency Response and Survival Capabilities**
Upgrade airport firefighting systems, rescue readiness, and evacuation procedures.  
Improve cabin safety design, onboard medical tools, and clearer safety briefing materials to increase survival outcomes.

 **5. Expand Adoption of Advanced Technology and Data Systems**
Encourage the use of AI assisted monitoring, predictive maintenance, advanced weather detection tools, and integrated data reporting systems.  
Greater transparency and real time diagnostics help prevent incidents before they occur.

""")




