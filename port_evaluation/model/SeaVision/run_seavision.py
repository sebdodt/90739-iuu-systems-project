from datetime import datetime
from api import seavision_ships_in_radius

data = seavision_ships_in_radius(
    lat=61.3765696863914,
    lon=172.931172943579,
    datetime=datetime(2022, 9, 19, 8, 20, 0))
print(data)