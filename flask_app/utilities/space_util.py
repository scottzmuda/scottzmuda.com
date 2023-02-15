import math

def lat_to_natural_language( lat_deg ):

	deltas_latitude_locations = []
	deltas_latitude_locations.append(lat_deg - 90)
	deltas_latitude_locations.append(lat_deg - 0)
	deltas_latitude_locations.append(lat_deg + 90)

	#find nearest
	nearest_location_index = min(enumerate(deltas_latitude_locations), key=lambda x: abs(x[1]))[0]
	
	if deltas_latitude_locations[nearest_location_index] < 0:
		relation_string = "down from the "
	else:
		relation_string = "up from the "

	if abs(deltas_latitude_locations[nearest_location_index]) < 5:
		magnitude_string = "right "
	elif abs(deltas_latitude_locations[nearest_location_index]) < 15:
		magnitude_string = "a bit "
	elif abs(deltas_latitude_locations[nearest_location_index]) < 30:
		magnitude_string = "a good bit "
	else:
		magnitude_string = "about a quarter way "

	if nearest_location_index == 0:
		return magnitude_string + relation_string + "north pole"
	if nearest_location_index == 1:
		return magnitude_string + relation_string + "equator"
	if nearest_location_index == 2:
		return magnitude_string + relation_string + "south pole"
