import logging
import datetime
import numpy as np

LOGGER = logging.getLogger(__name__)

def load_saved_state(file) -> dict:
    # Get the date from the filename: f"inputstate-{date.strftime('%Y%m%d_%H')}.npz"
    date_str = file.stem.split("-")[2]
    date = datetime.datetime.strptime(date_str, "%Y%m%d_%H")

    with np.load(file, allow_pickle=False) as data:
        fields = {k: data[k] for k in data.files}

    state = {"date": date, "fields": fields}
    return state


def save_state(state, outfile):
    np.savez(outfile, **state["fields"])

def find_nearest_point_index(lat_arr, lon_arr, lat0, lon0):
    """
    Works with 1D arrays of point coordinates (possibly from an unstructured grid).
    Returns the index of the point closest to (lat0, lon0) using great-circle distance.
    """
    # ensure arrays are 1D and same length
    lats = np.ravel(lat_arr)
    lons = np.ravel(lon_arr)
    lons = np.where(lons > 180, lons - 360, lons)

    # convert to radians
    lat_r = np.deg2rad(lats)
    lon_r = np.deg2rad(lons)
    lat0_r = np.deg2rad(lat0)
    lon0_r = np.deg2rad(lon0)

    # haversine formula for central angle (vectorized)
    dlat = lat_r - lat0_r
    dlon = lon_r - lon0_r
    a = np.sin(dlat / 2.0)**2 + np.cos(lat_r) * np.cos(lat0_r) * np.sin(dlon / 2.0)**2
    central_angle = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return int(np.argmin(central_angle))