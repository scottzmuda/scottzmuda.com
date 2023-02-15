import math

def lat_to_natural_language( lat_deg ):

	deltas_latitude_locations = []
	deltas_latitude_locations.append(lat_deg + 90)
	deltas_latitude_locations.append(lat_deg + 66.5)
	deltas_latitude_locations.append(lat_deg + 23.5)
	deltas_latitude_locations.append(lat_deg)
	deltas_latitude_locations.append(lat_deg - 23.5)
	deltas_latitude_locations.append(lat_deg - 66.5)


	#find nearest
	nearest_location_index = min((i for i, num in enumerate(deltas_latitude_locations) if num > 0))
	
	if nearest_location_index in [1, 4]:
		if deltas_latitude_locations[nearest_location_index] < 43/3:
			magnitude_string = "low "
		if deltas_latitude_locations[nearest_location_index] < 86/3:
			magnitude_string = "middle "
		else:
			magnitude_string = "high "
	else:
		if deltas_latitude_locations[nearest_location_index] < 23.5/3:
			magnitude_string = "low "
		if deltas_latitude_locations[nearest_location_index] < 47/3:
			magnitude_string = "middle "
		else:
			magnitude_string = "high "

	if lat_deg < 0:
		relation_string = "southern "
	else:
		relation_string = "northern "

	if nearest_location_index in [0, 5]:
		return magnitude_string + relation_string + "polar region"
	if nearest_location_index in [1, 4]:
		return magnitude_string + relation_string + "temperate region"
	if nearest_location_index in [2, 3]:
		return magnitude_string + relation_string + "tropical region"
	
