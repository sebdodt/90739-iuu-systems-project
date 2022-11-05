
## importing functions
from src.gfw import run_gfw
from src.seavision import run_seavision


## importing data
carriers, loitering, encounters, port_visits = run_gfw.run_gfw()
carriers_sv_info = run_seavision.get_info(carriers)
carriers_sv_history = run_seavision.get_history(carriers)


## creating variables



## returning output
