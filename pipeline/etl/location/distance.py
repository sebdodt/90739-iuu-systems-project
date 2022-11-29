from shapely import wkt
import geopandas as gpd
from shapely.geometry import mapping
import pandas as pd
from shapely.geometry import Point

# code Source: https://stackoverflow.com/questions/36972537/distance-from-point-to-polygon-when-inside
Shapefile = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\s_22mr22\s_22mr22.shp"
gpd_polygons = gpd.read_file(Shapefile)
us_terr=gpd_polygons
print(len(us_terr))
def find_distance(latitude, longtitude):
    pos = "POINT({0} {1})".format(latitude, longtitude)
    if not pd.isna(latitude):
        if not pd.isna(longtitude):
            pt = wkt.loads(pos)
            min_distance = float("inf")
            neareast_state = "N/A"
            for i in range(len(us_terr)):
                poly = us_terr.iloc[i,5]
                distance = poly.boundary.distance(pt)
                if(distance < min_distance):
                    min_distance = distance
                    nearest_state = us_terr.iloc[i,1]
    else:
        min_distance = -float("inf")
        nearest_state="N/A"
    return min_distance,nearest_state


def distance_to_USA(result):
    '''
    appends columns:
    - "distance_to_us": the mimimum distance of the carrier (given latitude and longtitude) to U.S terriotry
    '''
    result["distance_to_us"] = [find_distance(x,y) for x,y in zip(result['Latitude'], result['Longitude'])]
    return result
