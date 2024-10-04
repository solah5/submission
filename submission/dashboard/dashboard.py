import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
day_df = pd.read_csv('https://raw.githubusercontent.com/solah5/submission/refs/heads/main/submission/data/day.csv')
hour_df = pd.read_csv('https://raw.githubusercontent.com/solah5/submission/refs/heads/main/submission/data/hour.csv')

# Convert 'dteday' to datetime in both datasets
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# -- Streamlit Dashboard --

# Title of the Dashboard
st.title('Bike Rentals Dashboard')

# Display general data information
st.header('Dataset Overview')
st.write("### Data Harian")
st.write(day_df.head())
st.write("### Data Perjam")
st.write(hour_df.head())

# Section 1: Analysis of bike rentals by weather
st.header('Analysis: Influence of Weather on Bike Rentals')

# Group data by weather situation for daily analysis
weather_grouped = day_df.groupby('weathersit').agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean'
}).reset_index()

# Mapping 'weathersit' to descriptive labels
weather_grouped['weathersit'] = weather_grouped['weathersit'].map({
    1: 'Clear/Few clouds',
    2: 'Mist/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Ice Pellets'
})

# Display the table
st.write("### Average Rentals by Weather")
st.dataframe(weather_grouped)

# Visualization for weather influence
plt.figure(figsize=(10,6))
sns.barplot(x='weathersit', y='cnt', data=weather_grouped, palette='Blues_d')
plt.title('Average Total Bike Rentals by Weather Condition')
plt.xlabel('Weather Condition')
plt.ylabel('Average Total Rentals')

# Display the chart in Streamlit
st.pyplot(plt)

# Section 2: Analysis of bike rentals by working and non-working hours
st.header('Analysis: Bike Rentals during Working and Non-Working Hours')

# Define working hours (9 AM to 5 PM)
hour_df['is_working_hour'] = hour_df['hr'].apply(lambda x: 1 if 9 <= x <= 17 else 0)

# Group by working hours
working_hour_grouped = hour_df.groupby('is_working_hour').agg({
    'casual': 'mean',
    'registered': 'mean',
    'cnt': 'mean'
}).reset_index()

# Map working hour categories to descriptive labels
working_hour_grouped['is_working_hour'] = working_hour_grouped['is_working_hour'].map({
    1: 'Working Hours (9-17)',
    0: 'Outside Working Hours'
})

# Display the table
st.write("### Average Rentals during Working and Non-Working Hours")
st.dataframe(working_hour_grouped)

# Visualization for working hours influence
plt.figure(figsize=(10,6))
sns.barplot(x='is_working_hour', y='cnt', data=working_hour_grouped, palette='Oranges_d')
plt.title('Average Bike Rentals during Working vs. Non-Working Hours')
plt.xlabel('Time Period')
plt.ylabel('Average Total Rentals')

# Display the chart in Streamlit
st.pyplot(plt)

# Conclusion section
st.header('Conclusion')
st.write("""
- **Cuaca**: Jumlah peminjaman sepeda tertinggi terjadi saat cuaca cerah atau sedikit berawan. Peminjaman menurun secara signifikan saat cuaca buruk.
- **Jam kerja**: Terdapat lebih banyak peminjaman sepeda selama jam kerja, terutama oleh pengguna terdaftar. Pengguna kasual lebih banyak meminjam sepeda di luar jam kerja.
""")