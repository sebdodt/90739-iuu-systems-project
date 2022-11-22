import geopandas as gpd
from shapely.geometry import mapping
import pandas as pd
from shapely.geometry import Point
import numpy as np

def in_eez(output):
    '''
    appends columns:
    - 'in_us_eez': whether boat is currently in U.S. EEZ
    - 'in_nato_eez': whether boat is currently in the EEZ of a nato-allied country
    - 'in_five_eyes_eez': whether boat is currently in the EEZ of a five eye member
    - 'in_eez': whether boat is currently in any EEZ
    - 'eez': name of the EEZ where boat is currently in
    '''

    ### to do: change the file name, this is the file name&oath of SEAVISION data file
    output = pd.DataFrame(output)
    file_name = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\lists-Reefers-2022-11-11_04-40.csv"
    df= pd.read_csv(file_name)
    df['coordinates'] = list(zip(df['Latitude'], df['Longitude']))
    df.coordinates = df.coordinates.apply(Point)
    ### to do: change the file name, this is the file name&path of EEZ Shapfile 
    Shapefile = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\World_ECS_v1_20221013\World_ECS_v1_20221013\ecs_v01.shp"
    gdf_polygons = gpd.read_file(Shapefile)
    gdf_points = gpd.GeoDataFrame(df, geometry='coordinates')
    gdf_points.crs = gdf_polygons.crs
    sjoin = gpd.sjoin(gdf_points, gdf_polygons, how='left', op='within')
    df_join = pd.DataFrame(sjoin)
    result = df_join[["MMSI", "Latitude", "Longitude", "MRGID_TER1", "TERRITORY1", "TERRITORY2","SOVEREIGN1", "SOVEREIGN2", "ISO_SOV1"]]
    ## Append useful columns!
    result["in_eez"] = np.where(result['MRGID_TER1'].isna(), 0, 1)
    us_iso = "USA"
    # five eyes countries: Australia, Canada, New Zealand, the United Kingdom and the United States
    five_eyes_iso =["USA", "AUS", "CAN", "NZL","GBR"] 
    result['in_us_eez'] = np.where(result['ISO_SOV1']== "USA", 1, 0)
    result['in_five_eyes_eez']= result.apply(lambda x: 1 if x['ISO_SOV1'] in five_eyes_iso else 0, axis=1 )
    new_output = output.merge(result,left_on="MMSI", right_on="MMSI",how = "left")
    return new_output



    



