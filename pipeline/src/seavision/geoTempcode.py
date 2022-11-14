import geopandas as gpd
from shapely.geometry import mapping
import pandas as pd
from shapely.geometry import Point


file_name = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\lists-Reefers-2022-11-11_04-40.csv"
df= pd.read_csv(file_name)
print(df.columns)
df['coordinates'] = list(zip(df['Latitude'], df['Longitude']))
df.coordinates = df.coordinates.apply(Point)
Shapefile = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\World_ECS_v1_20221013\World_ECS_v1_20221013\ecs_v01.shp"
gdf_polygons = gpd.read_file(Shapefile)
gdf_points = gpd.GeoDataFrame(df, geometry='coordinates')
gdf_points.crs = gdf_polygons.crs
sjoin = gpd.sjoin(gdf_points, gdf_polygons, how='left', op='within')
df_join = pd.DataFrame(sjoin)



####### function to get EEZ related base dataframe
def eez_base():
    file_name = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\lists-Reefers-2022-11-11_04-40.csv"
    Shapefile = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\World_ECS_v1_20221013\World_ECS_v1_20221013\ecs_v01.shp"
    df= pd.read_csv(file_name)
    df['coordinates'] = list(zip(df['Latitude'], df['Longitude']))
    df.coordinates = df.coordinates.apply(Point)
    gdf_polygons = gpd.read_file(Shapefile)
    gdf_points = gpd.GeoDataFrame(df, geometry='coordinates')
    gdf_points.crs = gdf_polygons.crs
    sjoin = gpd.sjoin(gdf_points, gdf_polygons, how='left', op='within')
    pd.set_option('display.max_columns', None)
    df_join = pd.DataFrame(sjoin)
    df_join["eez_indicator"]= df_join.apply(lambda x: 0 if x.MRGID_TER1.isna() else 1)
    pd.set_option('display.max_columns', None)
    result = df_join[["MMSI", "Latitude", "Longitude", "MRGID_TER1", "TERRITORY1", "TERRITORY2","SOVEREIGN1", "SOVEREIGN2", "eez_indicator"]]
    return result
    




