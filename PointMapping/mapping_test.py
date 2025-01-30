import folium

# Create a map of the world with a zoom level of 2
m = folium.Map(location=[48.858448869, 2.2946447001], zoom_level=1, zoom_start=20, language='en')

# Create a list of latitude and longitude coordinates
coordinates = [
    [48.85844886989107, 2.2946447001326358],
    [48.85357427140073, 2.3449101122233618],
    [48.88098600921507, 2.35548126097005],
]

# Add markers to the map for each set of latitude and longitude coordinates
for latitude, longitude in coordinates:
    folium.Marker([latitude, longitude]).add_to(m)
    
# Create a PolyLine for given coordinates
polyline = folium.PolyLine(
    coordinates,
    color='red',
    weight=5,
    popup=f'This is a polyline with coordinates {coordinates}',
)

# Add the PolyLine to the map
polyline.add_to(m)

m.save("index.html")