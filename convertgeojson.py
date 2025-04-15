import json
from pyproj import Transformer, CRS

# --- Configuration ---
# Define the source CRS (Coordinate Reference System)
# Common Vienna OGD CRS is EPSG:31256 (MGI / Austria GK M34)
# Adjust if you know the exact source CRS is different.
source_crs_epsg = 31256

# Define the target CRS (WGS 84 - Latitude/Longitude)
target_crs_epsg = 4326

# Input and Output file paths
input_geojson_path = '/Users/haraldbeker/EuropeanMaps/WienBezirke.json'
output_geojson_path = '/Users/haraldbeker/EuropeanMaps/WienBezirke_WGS84.json'
# --- End Configuration ---

# Create a transformer object
# always_xy=True ensures (longitude, latitude) order for geographic CRS,
# which is the standard for GeoJSON. For projected CRS like EPSG:31256,
# the order is typically (Easting, Northing) or (X, Y).
# pyproj handles the axis order based on the CRS definition.
transformer = Transformer.from_crs(
    f"EPSG:{source_crs_epsg}",
    f"EPSG:{target_crs_epsg}",
    always_xy=True # Crucial for correct GeoJSON longitude, latitude order
)

def transform_coordinates(coords, transformer):
    """
    Recursively transforms nested lists of coordinates.
    Handles Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon.
    """
    if not coords:
        return coords
    # Check if the first element is a number (indicates a coordinate pair)
    if isinstance(coords[0], (int, float)):
        # It's a single coordinate pair [x, y]
        lon, lat = transformer.transform(coords[0], coords[1])
        return [lon, lat]
    else:
        # It's a list of coordinates or nested lists
        return [transform_coordinates(c, transformer) for c in coords]

# Load the GeoJSON data
try:
    with open(input_geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
except FileNotFoundError:
    print(f"Error: Input file not found at {input_geojson_path}")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {input_geojson_path}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while reading the file: {e}")
    exit()


# Iterate through features and transform geometries
if geojson_data.get("type") == "FeatureCollection":
    for feature in geojson_data.get("features", []):
        geometry = feature.get("geometry")
        if geometry and "coordinates" in geometry:
            try:
                geometry["coordinates"] = transform_coordinates(
                    geometry["coordinates"],
                    transformer
                )
            except Exception as e:
                print(f"Error transforming coordinates for feature {feature.get('id', 'N/A')}: {e}")
                # Optionally skip this feature or handle the error differently
                continue
elif geojson_data.get("type") == "Feature":
     geometry = geojson_data.get("geometry")
     if geometry and "coordinates" in geometry:
         try:
            geometry["coordinates"] = transform_coordinates(
                geometry["coordinates"],
                transformer
            )
         except Exception as e:
            print(f"Error transforming coordinates for the feature: {e}")
# Add more conditions if other GeoJSON types (like GeometryCollection) are possible

# Save the transformed GeoJSON data
try:
    with open(output_geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2) # Use indent for readability
    print(f"Successfully transformed coordinates and saved to {output_geojson_path}")
except Exception as e:
    print(f"An error occurred while saving the transformed file: {e}")

