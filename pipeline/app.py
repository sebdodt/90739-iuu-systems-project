
## importing functions
from src.gfw import run_gfw
from src.seavision import run_seavision
from etl.activity import meetings, perc_filled, severity
from etl.info import owner, ship
from etl.location import distance, dod_zone, eez, port, rfmo
from output import export

## importing data
carriers, loitering, encounters, port_visits = run_gfw.run_gfw()
carriers_sv_info = run_seavision.get_info(carriers)
carriers_sv_history = run_seavision.get_history(carriers)


## creating variables
### vessel info
# ...

### location specific
output = carriers[['mmsi', 'imo']]
output = port.at_port(output)
output = eez.in_eez(output)
output = rfmo.in_rfmo(output)
# ...

### activity
# ...

## returning output
export.export_data(output)
print(" > Done.")