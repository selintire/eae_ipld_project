# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities (with some cleaning and modifications).")


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/cities_temperatures.csv"

    temps_df = pd.read_csv(data_path, index_col="City")  # TODO: Ex 3.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id"

    if temps_df is not None:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date

    return temps_df  # a Pandas DataFrame


temps_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----

# TODO: Ex 3.2: Create a new column called `AvgTemperatureCelsius` that contains the temperature in Celsius degrees.
temps_df["AvgTemperatureCelsius"] = (temps_df["AvgTemperatureFahrenheit"] - 32) * 5 / 9      # uncomment this line to complete it


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 3.3: How many different cities are there? Provide a list of them.
# Get the list of unique cities
temps_df = pd.read_csv("data/cities_temperatures.csv")
unique_countries_list = temps_df['City'].unique()  # Replace 'city' with the appropriate column if needed


# TODO: Ex 3.4: Which are the minimum and maximum dates?
min_date = temps_df['Date'].min()
max_date = temps_df["Date"].max()

# TODO:  Ex 3.5: What are the global minimum and maximum temperatures? Find the city and the date of each of them.
min_temp = temps_df['AvgTemperatureFahrenheit'].min()
max_temp = temps_df['AvgTemperatureFahrenheit'].max()

min_temp_city = None
min_temp_date = None

max_temp_city = None
max_temp_date = None


# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])
if unique_countries_list is not None:
    cols1[0].dataframe(pd.Series(unique_countries_list, name="Cities"), use_container_width=True)
else:
    cols1[0].write("⚠️ You still need to develop the Ex 3.3.")

if min_date is not None and max_date is not None:

    cols1[2].write("#")

    min_temp_text = f"""
    ### ☃️ Min Temperature: {min_temp:.1f}°C
    *{min_temp_city} on {min_temp_date}*
    """
    cols1[2].write(min_temp_text)

    cols1[2].write("#")

    max_temp_text = f"""
    ### 🏜️ Max Temperature: {max_temp:.1f}°C
    *{max_temp_city} on {max_temp_date}*
    """
    cols1[2].write(max_temp_text)

else:
    cols1[2].write("⚠️ You still need to develop the Ex 3.5.")


# ----- Plotting the temperatures over time for the selected cities -----

st.write("##")
st.header("Comparing the Temperatures of the Cities")

if unique_countries_list is not None:
    # Getting the list of cities to compare from the user
    selected_cities = st.multiselect("Select the cities to compare:", unique_countries_list, default=["Buenos Aires", "Dakar"], max_selections=4)

    cols2 = st.columns([6, 1, 6])

    start_date = cols2[0].date_input("Select the start date:", pd.to_datetime("2009-01-01").date())     # Getting the start date from the user
    end_date = cols2[2].date_input("Select the end date:", pd.to_datetime("2018-12-31").date())         # Getting the end date from the user

else:
    st.subheader("⚠️ You still need to develop the Ex 3.3.")

if unique_countries_list is not None and len(selected_cities) > 0:

    c = st.container(border=True)

    # TODO: Ex 3.7: Plot the temperatures over time for the selected cities for the selected time period,
    # every city has to be its own line with a different color.

    
    selected_cities = st.multiselect("Select cities:", temps_df['City'].unique())
    start_date = st.date_input("Select start date", min_value=temps_df['Date'].min(), max_value=temps_df['Date'].max())
    end_date = st.date_input("Select end date", min_value=start_date, max_value=temps_df['Date'].max())
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    selected_period = (start_date, end_date)

    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:
         
        city_df = temps_df[temps_df['City'] == city]
        city_df_period = city_df[(city_df['Date'] > start_date) & (city_df['Date'] < end_date)] 
        if not city_df_period.empty:
            plt.plot(city_df_period['Date'], city_df_period['AvgTemperatureFahrenheit'], label=city)

           
    
    
    

    
    plt.title("Temperatures Over Time for Selected Cities")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")

    plt.legend()
    plt.grid(True)

    c.pyplot(fig)



    # TODO: Make a histogram of the temperature reads of a list of selected cities, for the selected time period, 
    # every city has to be its own distribution with a different color.
    
    #temps_df['Date'] = pd.to_datetime(temps_df['Date'], errors='coerce')
    #elected_cities = st.multiselect("Select cities:", temps_df['City'].unique())
    #start_date = st.date_input("Select start date", min_value=temps_df['Date'].min(), max_value=temps_df['Date'].max())
    #end_date = st.date_input("Select end date", min_value=start_date, max_value=temps_df['Date'].max())
    #start_date = pd.to_datetime(start_date)
    #end_date = pd.to_datetime(end_date)

    if not selected_cities:
        st.warning("⚠️ Please select at least one city to generate the histogram.")
    else:
        fig = plt.figure(figsize=(10, 5))

        for city in selected_cities:
            city_df = temps_df[temps_df['City'] == city]   
            st.write(f"Filtering data for city: {city}")
            st.write(city_df.head())
            
            city_df_period = city_df[(city_df['Date'] >= start_date) & (city_df['Date'] <= end_date)]

            if not city_df_period.empty:  
                plt.hist(city_df_period['AvgTemperatureFahrenheit'], bins=20, alpha=0.5, label=city)
            else:
                 st.warning(f"⚠️ No data available for {city} in the selected period.")

# Titles and labels (outside the loop)
    
        plt.title("Temperature Distribution for Selected Cities")   
        plt.xlabel("Temperature (°F)")  
        plt.ylabel("Frequency")  
        plt.legend()
        plt.grid(True)

        st.pyplot(fig)
    









