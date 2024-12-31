import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import streamlit as st

# Load the data
data = pd.read_excel('data_20241226.xlsx')  # Replace with your file path
usa_data = pd.read_csv('us_states_with_coordinates.csv')  # Load USA state latitude and longitude data


# Preprocess the data
unique_opportunities = data.drop_duplicates(subset='Sol#')

# Define a mapping of country codes to latitude and longitude
country_coords = {
        "USA": [37.0902, -95.7129, 0],
        "CUB": [21.5218, -77.7812, 0],
        "BEL": [50.8503, 4.3517, 0],
        "KEN": [-1.2921, 36.8219, 0],
        "AUS": [-25.2744, 133.7751, 0],
        "GUY": [4.8604, -58.9302, 0],
        "MEX": [23.6345, -102.5528, 0],
        "KWT": [29.3117, 47.4818, 0],
        "GRC": [39.0742, 21.8243, 0],
        "ECU": [-1.8312, -78.1834, 0],
        "GBR": [55.3781, -3.4360, 0],
        "ISR": [31.0461, 34.8516, 0],
        "QAT": [25.3548, 51.1839, 0],
        "IRQ": [33.2232, 43.6793, 0],
        "SSD": [6.8770, 31.3069, 0],
        "ITA": [41.8719, 12.5674, 0],
        "SEN": [14.4974, -14.4524, 0],
        "AGO": [-11.2027, 17.8739, 0],
        "COL": [4.5709, -74.2973, 0],
        "GTM": [15.7835, -90.2308, 0],
        "BHR": [25.9304, 50.6378, 0],
        "JAM": [18.1096, -77.2975, 0],
        "JPN": [36.2048, 138.2529, 0],
        "TCD": [15.4542, 18.7322, 0],
        "EST": [58.5953, 25.0136, 0],
        "VEN": [6.4238, -66.5897, 0],
        "GEO": [42.3154, 43.3569, 0],
        "JOR": [30.5852, 36.2384, 0],
        "PHL": [12.8797, 121.7740, 0],
        "PLW": [7.5149, 134.5825, 0],
        "KOR": [35.9078, 127.7669, 0],
        "SAU": [23.8859, 45.0792, 0],
        "TTO": [10.6918, -61.2225, 0],
        "IND": [20.5937, 78.9629, 0],
        "PER": [-9.1900, -75.0152, 0],
        "BHS": [25.0343, -77.3963, 0],
        "IOT": [-6.3432, 71.8765, 0],
        "MAR": [31.7917, -7.0926, 0],
        "EGY": [26.8206, 30.8025, 0],
        "UGA": [1.3733, 32.2903, 0],
        "DEU": [51.1657, 10.4515, 0],
        "SVK": [48.6690, 19.6990, 0],
        "NOR": [60.4720, 8.4689, 0],
        "UZB": [41.3775, 64.5853, 0],
        "GAB": [-0.8037, 11.6094, 0],
        "FRA": [46.6034, 1.8883, 0],
        "NAM": [-22.9576, 18.4904, 0],
        "TZA": [-6.3690, 34.8888, 0],
        "SWZ": [-26.5225, 31.4659, 0],
        "ESP": [40.4637, -3.7492, 0],
        "MYS": [4.2105, 101.9758, 0],
        "ETH": [9.1450, 40.4897, 0],
        "HKG": [22.3193, 114.1694, 0],
        "FSM": [6.8873, 158.2150, 0],
        "BRA": [-14.2350, -51.9253, 0],
        "PRT": [39.3999, -8.2245, 0],
        "CRI": [9.7489, -83.7534, 0],
        "POL": [51.9194, 19.1451, 0],
        "LBR": [6.4281, -9.4295, 0],
        "VNM": [14.0583, 108.2772, 0],
        "PAN": [8.5379, -80.7821, 0],
        "AFG": [33.9391, 67.7100, 0],
        "MDA": [47.4116, 28.3699, 0],
        "HND": [15.2000, -86.2419, 0],
        "AX1": [60.1926, 24.9458, 0],
        "BGD": [23.6850, 90.3563, 0],
        "TKM": [38.9697, 59.5563, 0],
        "HTI": [18.9712, -72.2852, 0],
        "CPV": [15.1201, -23.6052, 0],
        "AUT": [47.5162, 14.5501, 0],
        "CHL": [-35.6751, -71.5430, 0],
        "DNK": [56.2639, 9.5018, 0],
        "UKR": [48.3794, 31.1656, 0],
        "COG": [-0.2280, 15.8277, 0],
        "FIN": [61.9241, 25.7482, 0],
        "XKS": [42.6026, 20.9020, 0],
        "TLS": [-8.8742, 125.7275, 0],
        "PRY": [-23.4425, -58.4438, 0],
        "GHA": [7.9465, -1.0232, 0],
        "BDI": [-3.3731, 29.9189, 0],
        "THA": [15.8700, 100.9925, 0],
        "MNE": [42.7087, 19.3744, 0],
        "BIH": [43.9159, 17.6791, 0],
        "ZMB": [-13.1339, 27.8493, 0],
        "TUR": [38.9637, 35.2433, 0],
        "LVA": [56.8796, 24.6032, 0],
        "ARE": [23.4241, 53.8478, 0],
        "COD": [-4.0383, 21.7587, 0],
        "IDN": [-0.7893, 113.9213, 0],
        "CYP": [35.1264, 33.4299, 0],
        "MUS": [-20.3484, 57.5522, 0],
        "TJK": [38.8610, 71.2761, 0],
        "HRV": [45.1000, 15.2000, 0],
        "NPL": [28.3949, 84.1240, 0],
        "ARM": [40.0691, 45.0382, 0],
        "ROU": [45.9432, 24.9668, 0],
        "LBN": [33.8547, 35.8623, 0],
        "ALB": [41.1533, 20.1683, 0],
        "BRN": [4.5353, 114.7277, 0],
        "BEN": [9.3077, 2.3158, 0],
        "MDG": [-18.7669, 46.8691, 0],
        "FJI": [-17.7134, 178.0650, 0],
    }

# Map the country codes to latitude and longitude
unique_opportunities['Latitude'] = unique_opportunities['PopCountry'].map(lambda x: country_coords[x][0] if x in country_coords else None)
unique_opportunities['Longitude'] = unique_opportunities['PopCountry'].map(lambda x: country_coords[x][1] if x in country_coords else None)

# Drop rows where latitude or longitude is missing
unique_opportunities = unique_opportunities.dropna(subset=['Latitude', 'Longitude'])

# Streamlit App
st.title('Interactive Opportunity Map')

filtered_data = unique_opportunities

# Filters
countries = unique_opportunities['PopCountry'].unique()
selected_country = st.sidebar.selectbox('Select Country', ['All'] + list(countries))

if selected_country != 'All':
    filtered_data = filtered_data[filtered_data['PopCountry'] == selected_country]
    if selected_country == 'USA':
        # Merge state data
        filtered_data = pd.merge(filtered_data, usa_data, on='PopState', how='inner', suffixes=('_opportunity', '_usa'))
        filtered_data['Latitude'] = filtered_data['Latitude_usa']
        filtered_data['Longitude'] = filtered_data['Longitude_usa']
        filtered_data['PopCountry'] = filtered_data['PopCountry_usa']
        filtered_data.drop(columns=['Latitude_opportunity', 'Longitude_opportunity','Latitude_usa', 'Longitude_usa'], inplace=True)
        # print(filtered_data.columns.tolist())
    else:
        filtered_data['Latitude'] = filtered_data['Latitude']
        filtered_data['Longitude'] = filtered_data['Longitude'] 


states = filtered_data['PopState'].unique()
selected_state = st.sidebar.selectbox('Select State', ['All'] + list(states))

if selected_state != 'All':      
    filtered_data = filtered_data[filtered_data['PopState'] == selected_state]



# Convert 'ResponseDeadLine' to datetime
unique_opportunities['ResponseDeadLine'] = pd.to_datetime(unique_opportunities['ResponseDeadLine'], errors='coerce', utc=True)
# print(f"Unique Opportunities: {unique_opportunities['ResponseDeadLine']}")

due_date = st.sidebar.date_input('Filter by Due Date', value=None)
if due_date:
    filtered_data = filtered_data.dropna(subset=['ResponseDeadLine'])  # Drop rows with NaT
    filtered_data['ResponseDeadLine'] = pd.to_datetime(
        filtered_data['ResponseDeadLine'], errors='coerce', utc=True
    )  # Ensure uniform datetime conversion
    filtered_data = filtered_data[filtered_data['ResponseDeadLine'].dt.date == due_date]
    
filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])

# Create the map
map_center = [20, 0]
map_object = folium.Map(location=map_center, zoom_start=2, tiles='OpenStreetMap')
marker_cluster = MarkerCluster().add_to(map_object)
# Add full-screen control to the map
from folium.plugins import Fullscreen
Fullscreen().add_to(map_object)

# Add markers
for _, row in filtered_data.iterrows():
    popup_content = f"""
    <b>Title:</b> {row['Title']}<br>
    <b>Sol#:</b> {row['Sol#']}<br>
    <b>Type:</b> {row['Type']}<br>
    <b>Deadline:</b> {row['ResponseDeadLine']}<br>
    <b>Country:</b> {row['PopCountry']}<br>
    <b>State:</b> {row['PopState']}<br>
    <b>Description:</b> <a href='{row['Description']}' target='_blank'>{row['Description']}</a>
    """
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_content, max_width=300),
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

# Add heatmap
heatmap_data = filtered_data[['Latitude', 'Longitude']].dropna().values.tolist()
HeatMap(heatmap_data).add_to(map_object)

# Display the map
# st.write('### Filtered Map')
st.components.v1.html(map_object._repr_html_(), height=1600, width=700, scrolling=False )
