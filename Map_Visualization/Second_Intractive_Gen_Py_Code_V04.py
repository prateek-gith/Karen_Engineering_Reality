import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from datetime import datetime
import numpy as np


# Load the data
data = pd.read_excel('data_20241226_V04.xlsx', sheet_name='data')  # Replace with your file path
all_lat_long_data = pd.read_excel('data_20241226_V04.xlsx', sheet_name='All_Country_Lat_Long')  # Replace with your file path
usa_data = pd.read_excel('data_20241226_V04.xlsx', sheet_name='USA_State')  # Replace with your file path
input_data = pd.read_excel('data_20241226_V04.xlsx', sheet_name='Input')  # Replace with your file path


# Preprocess the data
unique_opportunities = data.drop_duplicates(subset='Sol#')

filtered_data = unique_opportunities

# Prompt the user for a date input
posted_date = input_data.loc[0, 'Start_Date']
# print(posted_date)
posted_date= str(posted_date)


# Check if the input is 'None'
if posted_date == "none" or posted_date == "None" or posted_date=='' or posted_date==pd.NaT or posted_date==np.nan or posted_date== 'nan':
    posted_date = None
else:
    try:
        # Parse the input string into a datetime object
        posted_date = datetime.strptime(posted_date, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD'. or None")

        
due_date = input_data.loc[0, 'End_Date']
due_date= str(due_date)

# Check if the input is 'None'
if due_date == "none" or due_date == "None" or due_date=='' or due_date==pd.NaT or due_date==np.nan or due_date== 'nan': 
    due_date = None
else:
    try:
        # Parse the input string into a datetime object
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD'. or None")

NAIC_Code=input_data.loc[0, 'NaicsCode']
print(NAIC_Code, type(NAIC_Code))
# NAIC_Code= int(NAIC_Code)

if NAIC_Code == 0 or NAIC_Code == 'None' or NAIC_Code=='' or NAIC_Code==pd.NaT or NAIC_Code=='none' or NAIC_Code==np.nan:
    filtered_data = filtered_data.dropna(subset=['NaicsCode'])
    
else:
    
    filtered_data = filtered_data.dropna(subset=['NaicsCode'])
    filtered_data = filtered_data[filtered_data['NaicsCode'] == NAIC_Code]

# Filter the data based on the date range
if posted_date and due_date:
    # print(posted_date, due_date)
    filtered_data = filtered_data[
        (pd.to_datetime(filtered_data['ResponseDeadLine'],errors='coerce', utc=True).dt.date >= posted_date) & 
        (pd.to_datetime(filtered_data['ResponseDeadLine'],errors='coerce', utc=True).dt.date <= due_date)
    ]
elif posted_date:
    filtered_data = filtered_data[pd.to_datetime(filtered_data['ResponseDeadLine'], errors='coerce', utc=True).dt.date >= posted_date]
elif due_date:
    filtered_data = filtered_data.dropna(subset=['ResponseDeadLine'])  # Drop rows with NaT
    filtered_data['ResponseDeadLine'] = pd.to_datetime(
        filtered_data['ResponseDeadLine'], errors='coerce', utc=True
    )  # Ensure uniform datetime conversion
    filtered_data = filtered_data[filtered_data['ResponseDeadLine'].dt.date <= due_date]


filtered_data_new=filtered_data


take_input = 'All'
if take_input == 'All' or take_input == 'all':
    filtered_data = pd.merge(filtered_data, all_lat_long_data, on='PopCountry', how='inner')
    filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])


    # Create a base map centered at an approximate location
    map_center = [20, 0]  # Adjust this for a relevant central location
    map_object = folium.Map(
        location=map_center, 
        zoom_start=2, 
        tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' 
            '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )

    # map_object = folium.Map(location=map_center, zoom_start=2, tiles='Stamen Terrain')
    map_object = folium.Map(location=map_center, zoom_start=2, tiles='OpenStreetMap')


    # Add marker clustering
    marker_cluster = MarkerCluster().add_to(map_object)

    # Add markers for each opportunity
    for _, row in filtered_data.iterrows():
        country = row['PopCountry']
        title = row['Title']
        sol = row['Sol#']
        opp_type = row['Type']
        deadline = row['ResponseDeadLine']
        location = [row.get('Latitude', 0), row.get('Longitude', 0)]  # Use lat/lon if available

        # Dynamic popup with detailed information
        popup_content = f"""
        <b>Title:</b> {title}<br>
        <b>Sol#:</b> {sol}<br>
        <b>Type:</b> {opp_type}<br>
        <b>Deadline:</b> {deadline}<br>
        <b>Country:</b> {country}
        """
        folium.Marker(
            location=location,
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='blue' if opp_type == 'Solicitation' else 'green')  # Dynamic color
        ).add_to(marker_cluster)

    # Add a heatmap layer (optional)
    heatmap_data = filtered_data[['Latitude', 'Longitude']].dropna().values.tolist()
    # print(heatmap_data)
    HeatMap(heatmap_data).add_to(map_object)

    # Save the map as an HTML file
    map_object.save('ALL_Intractive_opportunity_map_V04.html')

    # Display the map in a Jupyter Notebook (if applicable)
    # map_object.show_in_browser()
    
    
take_input = 'USA'
if take_input == 'USA':
    filtered_data = filtered_data_new
    
    filtered_data = pd.merge(filtered_data, usa_data, on='PopState', how='inner')

    filtered_data['PopCountry'] = filtered_data['PopCountry_y']

    filtered_data.drop(columns=['PopCountry_y'], inplace=True)


    filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])


    # Create a base map centered at an approximate location
    map_center = [20, 0]  # Adjust this for a relevant central location
    map_object = folium.Map(
        location=map_center, 
        zoom_start=2, 
        tiles='https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
        attr='Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' 
            '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    )

    # map_object = folium.Map(location=map_center, zoom_start=2, tiles='Stamen Terrain')
    map_object = folium.Map(location=map_center, zoom_start=2, tiles='OpenStreetMap')


    # Add marker clustering
    marker_cluster = MarkerCluster().add_to(map_object)

    # Add markers for each opportunity
    for _, row in filtered_data.iterrows():
        country = row['PopCountry']
        title = row['Title']
        sol = row['Sol#']
        opp_type = row['Type']
        deadline = row['ResponseDeadLine']
        location = [row.get('Latitude', 0), row.get('Longitude', 0)]  # Use lat/lon if available

        # Dynamic popup with detailed information
        popup_content = f"""
        <b>Title:</b> {title}<br>
        <b>Sol#:</b> {sol}<br>
        <b>Type:</b> {opp_type}<br>
        <b>Deadline:</b> {deadline}<br>
        <b>Country:</b> {country}
        """
        folium.Marker(
            location=location,
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='blue' if opp_type == 'Solicitation' else 'green')  # Dynamic color
        ).add_to(marker_cluster)

    # Add a heatmap layer (optional)
    heatmap_data = filtered_data[['Latitude', 'Longitude']].dropna().values.tolist()
    # print(heatmap_data)
    HeatMap(heatmap_data).add_to(map_object)

    # Save the map as an HTML file
    map_object.save('USA_Intractive_opportunity_map_V04.html')

    # Display the map in a Jupyter Notebook (if applicable)
    # map_object.show_in_browser()
