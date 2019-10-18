import numpy as np 

def haversine_distance(loc1, loc2, earth_radius=6371.0):
    """
    The haversine formula determines the great-circle distance between two points on a sphere given their longitudes and latitudes. Important in navigation, it is a special case of a more general formula in spherical trigonometry, the law of haversines, that relates the sides and angles of spherical triangles.

    https://www.movable-type.co.uk/scripts/latlong.html

    Parameters
    ----------
    loc1 : pandas DataFrame
        The input data.
    loc2 : 

    earth_radius : float, default = 6371.0
        Earth radius parameter in km scale.

    Returns
    -------
    d : float
        Distance between two location in km scale.

    """

    lat1, lon1 = loc1
    lat2, lon2 = loc2

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    diff_lat = lat2-lat1
    diff_lon = lon2-lon1

    #dlat = math.radians(lat2-lat1)
    #dlon = math.radians(lon2-lon1)
    a = np.sin(diff_lat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(diff_lon/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = earth_radius * c

    return d