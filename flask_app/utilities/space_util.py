import math
from decimal import Decimal

def lat_to_natural_language( lat_deg ):

	deltas_latitude_locations = []
	deltas_latitude_locations.append(lat_deg + Decimal(90.0))
	deltas_latitude_locations.append(lat_deg + Decimal(66.5))
	deltas_latitude_locations.append(lat_deg + Decimal(23.5))
	deltas_latitude_locations.append(lat_deg)
	deltas_latitude_locations.append(lat_deg - Decimal(23.5))
	deltas_latitude_locations.append(lat_deg - Decimal(66.5))


	#find nearest
	nearest_location_index = min(enumerate(deltas_latitude_locations), key=lambda x: x[1] if x[1] > 0 else float('inf'))[0]

	if nearest_location_index in [1, 4]:
		if deltas_latitude_locations[nearest_location_index] < (43/3):
			magnitude_string = "lower "
		elif deltas_latitude_locations[nearest_location_index] < 86/3:
			magnitude_string = "middle "
		else:
			magnitude_string = "upper "

	else:
		if deltas_latitude_locations[nearest_location_index] < 23.5/3:
			magnitude_string = "lower "
		elif deltas_latitude_locations[nearest_location_index] < 47/3:
			magnitude_string = "middle "
		else:
			magnitude_string = "upper "

	if nearest_location_index in [0, 5]:
		return "polar region"
	if nearest_location_index in [1, 4]:
		return "temperate region"
	if nearest_location_index in [2, 3]:
		return "tropical region"

def elev_m_to_elev_ft( elev_m ):
	return int(elev_m / Decimal(0.3048))


	
