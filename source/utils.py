import numpy as np
import pandas as pd

def haversine_distance(lat1, lon1, lat2, lon2, earth_radius=6371.0):
    """
    The haversine formula determines the great-circle distance 
    between two points on a sphere given their longitudes and latitudes. 
    Important in navigation, it is a special case of 
    a more general formula in spherical trigonometry, the law of haversines, 
    that relates the sides and angles of spherical triangles.

    https://www.movable-type.co.uk/scripts/latlong.html

    Parameters
    ----------
    lat1 : pandas Series
        Origin latitudes
    lon1 : pandas Series
        Origin longitudes
    lat2 : pandas Series
        Destination latitudes
    lon2 : pandas Series
        Destination longitudes
    earth_radius : float, default = 6371.0
        Earth radius parameter in km scale.

    Returns
    -------
    d : pandas Series in float
        Distance between two location in km scale.
    """

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    diff_lat = lat2-lat1
    diff_lon = lon2-lon1

    a = np.sin(diff_lat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(diff_lon/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = earth_radius * c

    return d

def get_trip_distance(data, code):
    """
    Get the trip distance between origin and destination 

    Parameters
    ----------
    data : pandas DataFrame
        data must contain 'origin' and 'destination' in iata code
    code : pandas DataFrame
        iata code location information
        code must contain code, longitutes, latitudes

    Returns
    -------
    distance : list of float
        Distance between origin and destination
    """

    data = data.rename(columns={data.columns[0]:'origin', 
                                data.columns[1]:'destination'})
    code = code.rename(columns={code.columns[0]:'code', 
                                code.columns[1]:'lat',
                                code.columns[2]:'lon'})

    for idx, col in enumerate(data.columns):
        data = pd.merge(data, code, how='inner',
                            left_on=col, right_on='code')
        data = data.rename(columns={'lat':'lat'+str(idx+1), 'lon':'lon'+str(idx+1)})
        data.drop('code', axis=1, inplace=True)

    distance = haversine_distance(data['lat1'],data['lon1'],data['lat2'],data['lon2'])
    return list(distance)