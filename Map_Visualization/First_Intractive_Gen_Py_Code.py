import pandas as pd
import plotly.express as px

# Path to your file (replace with the correct path)
file_path = "data.csv"

# Read the CSV file
try:
    data = pd.read_csv(file_path, encoding='latin1')  # Adjust encoding if needed
except Exception as e:
    print("Error reading file:", e)
    exit()

# Drop rows where 'PopCountry' or 'Sol#' is missing
data = data.dropna(subset=['PopCountry', 'Sol#'])

# Remove duplicate Sol# for each country
unique_opportunities = data[['PopCountry', 'Sol#']].drop_duplicates()

# Calculate the number of unique opportunities per country
country_opportunities = unique_opportunities.groupby('PopCountry').size().reset_index(name='PopCount')

# Create an interactive map using Plotly
fig = px.scatter_geo(
    country_opportunities,
    locations="PopCountry",  # Column containing country codes
    locationmode="ISO-3",    # Use ISO-3 country codes
    size="PopCount",         # Bubble size based on the number of opportunities
    color="PopCount",         # Bubble size based on the number of opportunities
    title="Geographical Distribution of Opportunities",
    hover_name="PopCountry", # Display country code on hover
    projection="natural earth",
    color_continuous_scale=px.colors.sequential.Viridis
)

# Show the map
fig.show()

# Save the map as an HTML file
output_file = "First_Intractive_opportunity_map.html"
fig.write_html(output_file)
print(f"Map has been saved to {output_file}")
