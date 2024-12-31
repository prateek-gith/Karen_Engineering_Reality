import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap

# Load the data
# data = pd.read_csv('data.csv',encoding='latin1')  # Replace with your file path
data = pd.read_excel('data_20241226.xlsx')

usa_data = pd.read_csv('us_states_with_coordinates.csv',encoding='latin1')  # Load USA state latitude and longitude data


# Preprocess the data
# Filter for unique opportunities
unique_opportunities = data.drop_duplicates(subset='Sol#')

# Define a mapping of country codes to latitude and longitude
country_coords = {
    "USA": [37.0902, -95.7129, 0],
}

# Map the country codes to latitude and longitude
unique_opportunities.loc[:,'Latitude'] = unique_opportunities['PopCountry'].map(lambda x: country_coords[x][0] if x in country_coords else None)
unique_opportunities.loc[:,'Longitude'] = unique_opportunities['PopCountry'].map(lambda x: country_coords[x][1] if x in country_coords else None)

# Drop rows where latitude or longitude is missing
unique_opportunities = unique_opportunities.dropna(subset=['Latitude', 'Longitude'])

filtered_data = unique_opportunities

# Merge state data
filtered_data = pd.merge(filtered_data, usa_data, on='PopState', how='inner', suffixes=('_opportunity', '_usa'))
# print(filtered_data.columns)
filtered_data['Latitude'] = filtered_data['Latitude_usa']
filtered_data['Longitude'] = filtered_data['Longitude_usa']
# filtered_data['PopCountry'] = filtered_data['PopCountry_usa']
filtered_data.drop(columns=['Latitude_opportunity', 'Longitude_opportunity','Latitude_usa', 'Longitude_usa'], inplace=True)
# print(filtered_data.head())


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
heatmap_data = unique_opportunities[['Latitude', 'Longitude']].dropna().values.tolist()
HeatMap(heatmap_data).add_to(map_object)

# Save the map as an HTML file
map_object.save('USA_Intractive_opportunity_map.html')

# Display the map in a Jupyter Notebook (if applicable)
map_object.show_in_browser()
