import pandas as pd
import numpy as np

def at_port(output):
    '''
    appends columns:
    - 'at_port': whether ship is currently at port
    - 'at_us_port': whether ship is currently at U.S. port
    - 'name_port': name of the port that the ship is at
    - 'country_port': country of the port where the ship is at
    '''
    ### assume ouput is as type of dataframe
    output = pd.DataFrame(output)
    seaVision_file = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\lists-Reefers-2022-11-11_04-40.csv"
    sea_vision= pd.read_csv(seaVision_file)
    ### can be reused for other functions
    ############
    at_port_data = sea_vision[["MMSI", "Navigation Status"]]
    at_port_data['at_port'] = np.where(at_port_data["Navigation Status"]=="5-Moored", 1, 0)
    new_output = output.merge(at_port_data, left_on="MMSI", right_on="MMSI",how = "left")
    return new_output
