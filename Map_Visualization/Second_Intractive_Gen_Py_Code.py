import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap

# Load the data
data = pd.read_csv('data.csv',encoding='latin1')  # Replace with your file path

# Preprocess the data
# Filter for unique opportunities
unique_opportunities = data.drop_duplicates(subset='Sol#')

# Define a mapping of country codes to latitude and longitude
country_coords = {
    "JPN": [36.2048, 138.2529], "KOR": [35.9078, 127.7669], "PHL": [12.8797, 121.7740], "SAU": [23.8859, 45.0792], "TTO": [10.6918, -61.2225], "KWT": [29.3117, 47.4818], "IND": [20.5937, 78.9629], "PER": [-9.1900, -75.0152], "BHS": [25.0343, -77.3963], "GRC": [39.0742, 21.8243], "IOT": [-6.3432, 71.8765], "GBR": [55.3781, -3.4360], "MAR": [31.7917, -7.0926], "ITA": [41.8719, 12.5674], "EGY": [26.8206, 30.8025], "UGA": [1.3733, 32.2903], "DEU": [51.1657, 10.4515], "SVK": [48.6690, 19.6990], "NOR": [60.4720, 8.4689], "UZB": [41.3775, 64.5853], "GAB": [-0.8037, 11.6094], "FRA": [46.6034, 1.8883], "NAM": [-22.9576, 18.4904], "TZA": [-6.369028, 34.888822], "SWZ": [-26.5225, 31.4659], "ESP": [40.4637, -3.7492], "MYS": [4.2105, 101.9758], "ETH": [9.145, 40.4897], "HKG": [22.3193, 114.1694], "FSM": [6.9106, 158.2475], "JAM": [18.1096, -77.2975], "AUS": [-25.2744, 133.7751], "BRA": [-14.2350, -51.9253], "PRT": [39.3999, -8.2245], "ECU": [-1.8312, -78.1834], "CRI": [9.7489, -83.7534], "POL": [51.9194, 19.1451], "COL": [4.5709, -74.2973], "LBR": [6.4281, -9.4295], "VNM": [14.0583, 108.2772], "PAN": [8.5380, -80.7821], "CUB": [21.5218, -77.7812], "AFG": [33.9391, 67.7100], "MDA": [47.4116, 28.3699], "HND": [13.9430, -83.3001], "AX1": [60.2737, 19.2395], "KEN": [-1.2921, 36.8219], "BGD": [23.685, 90.3563], "TKM": [38.9697, 59.5563], "HTI": [18.9712, -72.2852], "BHR": [25.9304, 50.6370], "GTM": [13.4747, -90.2308], "CPV": [16.0020, -24.0132], "MEX": [23.6345, -102.5528], "AUT": [47.5162, 14.5501], "CHL": [-35.6751, -71.5430], "DNK": [56.2639, 9.5018], "UKR": [48.3794, 31.1656], "COG": [-0.2280, 15.8270], "FIN": [61.9241, 25.7482], "XKS": [42.6026, 20.9020], "IRQ": [33.2232, 43.6793], "TLS": [-8.8742, 125.7275], "PRY": [-23.4425, -58.4438], "GHA": [7.9465, -1.0232], "BDI": [-3.3731, 29.9181], "THA": [15.8700, 100.9925], "MNE": [42.7087, 19.3744], "JOR": [30.5852, 36.2384], "BIH": [43.9159, 17.6791], "ZMB": [-13.1339, 27.8493], "TUR": [38.9637, 35.2433], "SSD": [6.8769, 31.3069], "LVA": [56.8796, 24.6032], "ARE": [23.4241, 53.8478], "EST": [58.5953, 25.0136], "BEL": [50.8503, 4.3517], "COD": [-4.0383, 21.7587], "IDN": [-0.7893, 113.9213], "CYP": [35.1264, 33.4299], "MUS": [-20.3484, 57.5522], "TJK": [38.8610, 71.2761], "HRV": [45.1, 15.2], "NPL": [28.3949, 84.1240], "ARM": [40.0691, 45.0382], "ROU": [45.9432, 24.9668], "LBN": [33.8547, 35.8623], "ALB": [41.1533, 20.1683], "BRN": [4.5353, 114.7277], "PLW": [7.5149, 134.5825], "BEN": [9.3075, 2.3158], "MDG": [-18.7669, 46.8691], "FJI": [-16.5782, 179.4144], "VEN": [6.4238, -66.5897], "AGO": [-11.2027, 17.8739], "LTU": [55.1694, 23.8813], "SRB": [44.0165, 21.0059], "NLD": [52.3784, 4.9009], "SEN": [14.6928, -14.0078], "ZAF": [-30.5595, 22.9375], "DJI": [11.8251, 42.5903], "MMR": [21.9139, 95.9560], "QAT": [25.3548, 51.1839], "GIN": [9.9456, -9.6966], "GEO": [42.3154, 43.3569], "MLI": [17.5707, -3.9962], "GUY": [4.8604, -58.9302], "OMN": [21.4735, 55.9754], "GRL": [71.7069, -42.6043], "BLZ": [17.1899, -88.4976], "SGP": [1.3521, 103.8198], "WSM": [-13.7590, -172.1046], "NZL": [-40.9006, 174.8860], "PAK": [30.3753, 69.3451], "RWA": [-1.9403, 29.8739], "LAO": [19.8563, 102.4955], "MWI": [-13.2543, 34.3015], "MNG": [46.8625, 103.8467], "KAZ": [48.0196, 66.9237], "CAN": [56.1304, -106.3468], "SWE": [60.1282, 18.6435], "MRT": [21.0079, -10.9400], "ATA": [-90.0000, 0.0000], "BFA": [12.2383, -1.5616], "LKA": [7.8731, 80.7718], "XWB": [0.0000, 0.0000], "CUW": [12.1696, -68.99], "SVN": [46.1511, 14.9955], "ISR": [31.0461, 34.8516], "MKD": [41.6086, 21.7453], "CHE": [46.8182, 8.2275], "ARG": [-38.4161, -63.6167], "NGA": [9.0820, 8.6753], "TUN": [33.8869, 9.5375], "AX2": [60.2737, 19.2395], "GNQ": [1.6508, 10.2679], "GNB": [11.8037, -15.1804], "GUM": [13.4443, 144.7937], "BOL": [-16.2902, -63.5887], "CIV": [7.5399, -5.5471], "VIR": [18.3358, -64.8963]
}

# Map the country codes to latitude and longitude
unique_opportunities.loc[:,'Latitude'] = unique_opportunities['PopCountry'].map(lambda x: country_coords[x][0] if x in country_coords else None)
unique_opportunities.loc[:,'Longitude'] = unique_opportunities['PopCountry'].map(lambda x: country_coords[x][1] if x in country_coords else None)

# Drop rows where latitude or longitude is missing
unique_opportunities = unique_opportunities.dropna(subset=['Latitude', 'Longitude'])


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
for _, row in unique_opportunities.iterrows():
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
map_object.save('Second_Intractive_opportunity_map.html')

# Display the map in a Jupyter Notebook (if applicable)
map_object.show_in_browser()
