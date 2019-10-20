import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt

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

def plot_precision_recall_curve(y_target, y_score, ax=None):
    """Plot the Precision-Recall curve

    Parameters
    ----------
    y_target : list of float
        Target value of classicifation
    y_score : list of float
        Predicted score of correspoding each target

    Returns
    ------
    ax: matplotlib.axes
        an AxesSubplot with the plot
    """
    ax = ax or plt.gca()
    precision, recall, _ = precision_recall_curve(y_target, y_score)
    ax.step(recall, precision, color='b', 
            alpha=0.2, where='post')
    ax.set(ylabel='Precision', xlabel='Recall', 
           xlim = [0.0, 1.0], ylim = [0.0, 1.05],
           title = '2-class Precision-Recall curve: AP={0:0.2f}'.format(
               average_precision_score(y_target, y_score)))

    return ax


def plot_feature_selection(classifier, features, ax=None):
    """Plot the Precision-Recall curve

    Parameters
    ----------
    classifier : sklearn classifier object 
        classifier must be fitted before passing
    features : list of string
        list of features

    Returns
    ------
    df : pandas DataFrame
        feature importance dataframe
    """
    ax = ax or plt.gca()
    df = pd.DataFrame()
    df['feature'] = features
    df['importance'] = classifier.feature_importances_
    df=df.sort_values(by='importance', ascending=False)
    
    ax.barh(df['feature'], 
            df['importance'], 
            align='center')
    ax.set(ylabel='feature', xlabel='importance', 
           title = 'Feature Importance')

    return df    