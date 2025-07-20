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
            amenity = tags.get('amenity', 'Unknown').lower()  # Normalize to lowercase
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
    file_path = "hospital.json"
    json_data = load_json_file(file_path)
    df = process_data(json_data)

    if not df.empty:
        gdf = create_geodataframe(df)

        # Extract school and hospital names
        school_names = df[df['amenity'] == 'school']['name'].drop_duplicates().tolist()
        hospital_names = df[df['amenity'] == 'hospital']['name'].drop_duplicates().tolist()

        if school_names:
            print("List of all schools:")
            for name in school_names:
                print(name)
        else:
            print("No schools found in the data.")

        if hospital_names:
            print("\nList of all hospitals:")
            for name in hospital_names:
                print(name)
        else:
            print("No hospitals found in the data.")
    else:
        print("No data to display.")

# This version will print all school and hospital names separately! Let me know if you want more changes or enhancements! 🚀
