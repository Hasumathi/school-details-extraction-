import osmnx as ox
import geopandas as gpd
import folium
import requests
import pandas as pd
from shapely.geometry import Point, Polygon
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Define the city or area for detection
CITY_NAME = "Bangalore, India"


# Step 1: Fetch School and Hospital Locations using OSM Overpass API
def get_osm_data(place_name, tag):
    query = f"""
    [out:json];
    area[name="{place_name}"]->.searchArea;
    (
      node["{tag}"](area.searchArea);
    );
    out body;
    """
    response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
    data = response.json()

    # Print response to check if data is received
    print(data)



    for element in data.get("elements", []):
        if "lat" in element and "lon" in element:
            locations.append({
                "name": element.get("tags", {}).get("name", "Unknown"),
                "latitude": element["lat"],
                "longitude": element["lon"]
            })

    return pd.DataFrame(locations)


# Fetch data for schools and hospitals
schools_df = get_osm_data(CITY_NAME, "amenity=school")
hospitals_df = get_osm_data(CITY_NAME, "amenity=hospital")

# Check the DataFrame structure
print(schools_df.head())
print(schools_df.columns)

# Convert to GeoDataFrame (using correct column names)
schools_gdf = gpd.GeoDataFrame(schools_df, geometry=gpd.points_from_xy(schools_df['lon'], schools_df['lat']))
hospitals_gdf = gpd.GeoDataFrame(hospitals_df, geometry=gpd.points_from_xy(hospitals_df['lon'], hospitals_df['lat']))


# Convert to GeoDataFrame


# Step 2: Fetch Road Network Data
road_graph = ox.graph_from_place(CITY_NAME, network_type="drive")
roads_gdf = ox.graph_to_gdfs(road_graph, nodes=False, edges=True)

# Step 3: Create a Feature Set for Machine Learning
schools_gdf["risk_factor"] = np.random.uniform(0.5, 1.0, size=len(schools_gdf))
hospitals_gdf["risk_factor"] = np.random.uniform(0.6, 1.0, size=len(hospitals_gdf))

# Prepare training data
features = []
labels = []

for _, row in schools_gdf.iterrows():
    features.append([row.geometry.x, row.geometry.y])
    labels.append(1)

for _, row in hospitals_gdf.iterrows():
    features.append([row.geometry.x, row.geometry.y])
    labels.append(2)

X = np.array(features)
y = np.array(labels)

# Step 4: Train a Machine Learning Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Step 5: Visualize on an Interactive Map
map_osm = folium.Map(location=[schools_df.latitude.mean(), schools_df.longitude.mean()], zoom_start=12)

# Add Schools
for _, row in schools_df.iterrows():
    folium.Marker(
        location=[row.latitude, row.longitude],
        popup=f"School: {row.name}",
        icon=folium.Icon(color="blue", icon="graduation-cap", prefix="fa"),
    ).add_to(map_osm)

# Add Hospitals
for _, row in hospitals_df.iterrows():
    folium.Marker(
        location=[row.latitude, row.longitude],
        popup=f"Hospital: {row.name}",
        icon=folium.Icon(color="red", icon="plus-square", prefix="fa"),
    ).add_to(map_osm)

# Save the map
map_osm.save("detected_zones_map.html")

print("✅ Processing complete! Open 'detected_zones_map.html' to see results.")

# Let me know if you want me to add any enhancements! 🚀
