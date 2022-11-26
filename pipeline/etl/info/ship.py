import pandas as pd

output_filename = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\carrier_mmsi.csv"
output = pd.read_csv(output_filename)
def mmsi_info(output):
    '''
    appends columns  for ship's information
    - 'ETA': estimate time of arrival
    - 'Call Sign': unique alphanumeric identity that belongs to the vessel
    - 'Name': name of the carrier
    - 'Year built'
    - 'latitude'
    - 'longtitude'
    - 'Heading': the direction the vessels is going 
    - 'flag'
    - 'deadweight': weight
    - 'Registered Owner'
    - 'Speed'
    - 'Builder' 
    - 'Port Of Registry'
    '''
    ### assume ouput is as type of dataframe
    output = pd.DataFrame(output)
    ### **** to do: change the file name
    seaVision_file = r"C:\Users\Irene\Desktop\Fall22\Capstone Project\Data\lists-Reefers-2022-11-11_04-40.csv"
    sea_vision= pd.read_csv(seaVision_file)
    ### can be reused for other functions
    info_data = sea_vision[["ETA", 'Call Sign', "Name", 'Year Built', 'Latitude','Longitude', 'Heading', 'Flag', 'Deadweight', "MMSI", 'Registered Owner', 'Speed', 'Builder', 'Port Of Registry']]
    new_output = output.merge(info_data, left_on="MMSI", right_on="MMSI",how = "left")
    return new_output
    


