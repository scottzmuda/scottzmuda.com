import math
from decimal import Decimal
import bisect

def lat_to_natural_language( lat_deg ):

	latitude_regions = [
	(Decimal(-90.0), "antarctic"),
	(Decimal(-66.5), "subantarctic"),
	(Decimal(-55.0), "temperate south"),
	(Decimal(-35.0), "subtropical south"),
	(Decimal(-23.5), "tropical south"),
	(Decimal(00.0), "tropical north"),
	(Decimal(23.5), "subtropical north"),
	(Decimal(35.0), "temperate north"),
	(Decimal(55.0), "subarctic"),
	(Decimal(66.5), "arctic"),
	(Decimal(90.0), "beyond the arctic")]

	latitude_regions_ordered = []

	for lat_location, place_string in latitude_regions:
		bisect.insort_left(latitude_regions_ordered, [lat_location, place_string])

	latitude_here = [lat_deg, "here"]
	index_here = bisect.bisect_left(latitude_regions_ordered, latitude_here)

	latitude_regions_ordered.insert(index_here, latitude_here)

	return latitude_regions_ordered[index_here-1][1]

    #return progress + identity of location

	#distance_progress = \
	#(latitude_regions_ordered[index_here][0]-latitude_regions_ordered[index_here-1][0]) / \
	#(latitude_regions_ordered[index_here+1][0]-latitude_regions_ordered[index_here-1][0]) \

	#if distance_progress < (1/3):
	#	return "lower " + latitude_regions_ordered[index_here-1][1]
	#elif distance_progress < (2/3):
	#	return "middle " + latitude_regions_ordered[index_here-1][1]
	#else:
	#	return "upper " + latitude_regions_ordered[index_here-1][1]

def elev_m_to_elev_ft( elev_m ):
	return int(elev_m / Decimal(0.3048))


	
