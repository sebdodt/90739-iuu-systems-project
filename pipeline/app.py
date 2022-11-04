


data = load_data()


## Seavision
SV_data = get_seavision_data(data['mmsi'])


## combine data
final_data = combine_data(data,SV_data)