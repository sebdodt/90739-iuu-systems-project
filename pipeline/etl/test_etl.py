
from info.ship import *
from location.eez import *
from location.port import *
from location.distance import *
import geopandas as gpd
from shapely.geometry import mapping
import pandas as pd
from shapely.geometry import Point
import numpy as np
### the output file from Dylan side
output_filename = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\carrier_mmsi.csv"
output = pd.read_csv(output_filename)
result = mmsi_info(output)
result = at_port(pd.DataFrame(result))
result = in_eez(pd.DataFrame(result))
result = distance_to_USA(pd.DataFrame(result))
