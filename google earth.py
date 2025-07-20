import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return None


def process_data(data):
    if not data or 'elements' not in data:
        print("No valid data found in the JSON file.")
        return pd.DataFrame()

    locations = []
    for element in data['elements']:
        if 'tags' in element and 'lat' in element and 'lon' in element:
            tags = element['tags']
            name = tags.get('name', 'Unnamed')
            amenity = tags.get('amenity', 'Unknown')
            lat = element['lat']
            lon = element['lon']

            locations.append({
                'name': name,
                'amenity': amenity,
                'lat': lat,
                'lon': lon
            })

    return pd.DataFrame(locations)


def create_geodataframe(df):
    if df.empty:
        return gpd.GeoDataFrame()

    geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf


if __name__ == "__main__":
    file_path = "export.json"
    json_data = load_json_file(file_path)
    df = process_data(json_data)

    if not df.empty:
        gdf = create_geodataframe(df)
        print(gdf.head())
    else:
        print("No data to display.")

# Replace 'path/to/your/file.json' with your actual JSON file path! Let me know if you want me to add more features or visualize the data. 🚀
