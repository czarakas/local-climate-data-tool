"""
Regrid the historical observations to be consistent with processed CMIP6 model
output.

Author: Jacqueline Nugent
Last Modified: November 29, 2019
"""
import math
import datetime as dt
from netCDF4 import Dataset
import xarray as xr
import pandas as pd
import numpy as np

import analysis_parameters


OUT_DIR = analysis_parameters.DIR_PROCESSED_DATA + 'observation_data/'


def convert_to_360(lons):
    """
    Convert longitudes with the convention -180 to 180 degrees to longitudes
    with the convention 0 to 360 degrees. Argument is 1D numpy array of
    longitudes. Returns 1D numpy array of converted longitudes.
    """
    new_lons = np.empty(len(lons))

    for n in range(len(lons)):
        if lons[n] < 0:
            new_lons[n] = 360 + lons[n]
        else:
            new_lons[n] = lons[n]

    return new_lons


def calculate_temps(filename):
    """
    Converts the temperature anomalies and climatologies from the
    observations file into actual average, maximum, and minimum temperatures.
    Returns the average, maximum, and minimum temperatures and their
    dimensions (time, lat, lon) as a list of numpy arrays.
    """
    ### read in data, skipping first 100 years (1200 months) to match times
    ### in CMIP6 model data:
    nc1 = Dataset(filename, 'r')
    lat = nc1.variables['latitude'][:]
    lon = convert_to_360(nc1.variables['longitude'][:])
    time_avg = nc1.variables['time'][1200:]
    t_avg_anom = nc1.variables['temperature'][1200:][:][:]
    t_avg_clima = nc1.variables['climatology'][:][:][:]

    ### convert native time variables (in decimal year) to match model times
    [dec_start, yr_start] = math.modf(time_avg[0])
    mnth_start = int(dec_start*12 + 1)
    first = dt.datetime(year=int(yr_start), month=mnth_start, day=15)

    [dec_end, yr_end] = math.modf(time_avg[-1])
    mnth_end = int(dec_end*12 + 1)
    last = dt.datetime(year=int(yr_end), month=mnth_end, day=15)

    time = pd.date_range(start=first, end=last, periods=len(time_avg))

    ### calculate the avg temperatures from the anomalies and climatologies:
    t_avg = np.empty(np.shape(t_avg_anom))

    for i in range(12):
        t_avg[i::12, :, :] = [(x + t_avg_clima[i, :, :])
                              for x in t_avg_anom[i::12, :, :]]

    return [t_avg, time, lat, lon]


def create_obs_dataset(t_avg, time, lat, lon):
    """
    Create Dataset for the average temperature observations with variable
    'mean' in degrees C and dimensions time, lat, and lon.

    Arguments are the calculated average temperatures and the coordinates of
    the dimensions (time, lat, lon) as returned by calculate_temps(). Returns
    a the Dataset.
    """
    best_data = xr.Dataset(data_vars={'mean': (['time', 'lat', 'lon'], t_avg)},
                           coords={'time': time, 'lat': lat, 'lon': lon})

    ### reorganize data so that the longitudes are in ascending order
    best_data = best_data.sortby('lon')
    
    # temp:
    print('dataset created')

    return best_data


def save_dataset(best_data, data_path_out):
    """Save the processed temperature observation Datasets to zarr files"""
    print('saving dataset...')
    best_data.load()
    best_data.chunk({'lat':10, 'lon':10, 'time':-1})
    best_data.to_zarr(data_path_out + 'historical_obs.zarr')


##################### Main Workflow ##########################################

def process_all_observations(data_path, data_path_out=OUT_DIR):
    """Processes the historical observations file"""
    obs_file = data_path + 'Complete_TAVG_LatLong1.nc'

    # read in the file and calculate average temperatures
    [mean_temp, times, lats, longs] = calculate_temps(obs_file)

    # generate the datasets
    obs_ds = create_obs_dataset(mean_temp, times, lats, longs)

    # save the datasets
    save_dataset(obs_ds, data_path_out)