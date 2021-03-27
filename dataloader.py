# coding: utf-8
import os
import sys

import cv2
import pandas as pd
import numpy as np
from configparser import ConfigParser
from logging import getLogger


logger = getLogger("__main__").getChild("dataloader")


def config(track, config_file='config.ini'):
    '''
    Load ini file and submitted data 

    Parameters
    ----------
    track : str 
        'VDR' or 'PDR'
    config_file : str
        Loading configuration file name
    Retruns
    -------
    conf : list
        [ini file documents, submit file directory path]
    '''
    logger.debug('Loading configuration file: {}'.format(config_file))

    if not os.path.exists(config_file):
        raise FileExistsError('{} does not exist'.format(config_file))

    # Load ini file
    config_ini = ConfigParser()
    config_ini.optionxform = str
    config_ini.read(config_file, encoding='utf-8')
    conf = dict()

    ini_names ={'dir_name':['map_dname', 'ans_dname', 'ref_dname', 'ALIP_dname', 'BLE_dname'],
                'file_name':['map_image_fname', 'map_size_fname', 'area_fname', 'ref_fname', 
                'ans_fname', 'ALIP_info_fname', 'BLE_info_fname'],
               'map_color':['map_obstacle_color', 'map_trajectory_color', 'map_ref_color', 
               'map_BLE_color'],
               'map_makersize':['map_trajectory_size', 'map_ref_size', 'map_BLE_size', 'map_grid']}

    ground_truth_dname = config_ini['ANSWER']['ground_truth_dname'].strip("'")
    
    for key, values in ini_names.items():
        for v in values:
            item = config_ini[track][v].strip("'")
            if key == 'dir_name':
                item = os.path.join(ground_truth_dname, item)
            
            conf[v] = item
            logger.debug('{}: {}'.format(v, item))

    logger.debug("Configuration file load complete!")
    return conf

def index_weights(config_file='index_weights.ini'):
    '''
    Load index weights

    Parameters
    ----------
    config_file : str
        Loading configuration file name
    Retruns
    -------
    weights: DataFrame
    '''

    logger.debug('Loading index weights: {}'.format(config_file))

    if not os.path.exists(config_file):
        raise FileExistsError('{} does not exist'.format(config_file))

    # Load ini file
    config_ini = ConfigParser()
    config_ini.optionxform = str
    config_ini.read(config_file, encoding='utf-8')

    weights = {}  
    for key in config_ini['WEIGHTS']:
        w = float(config_ini['WEIGHTS'][key])
        weights[key] = w
        logger.debug('{} : {}'.format(key, w))

    weights = pd.DataFrame(weights, index=['i',])
    return weights

def map_size(base_dname, map_size_fname):
    '''
    Load map size file

    Parameters
    ----------
    base_dname : str
    map_size_fname : str
    
    Returns
    -------
    map_size : ndarray of float
        map size [x, y]
    '''
    map_size_path = os.path.join(base_dname, map_size_fname)
    logger.debug('Loading Map size file : {}'.format(map_size_path))
    
    try:
        map_size_df = pd.read_csv(map_size_path, names=['x[m]', 'y[m]'])
    except FileNotFoundError:
        logger.debug('{} does not exists'.format(map_size_path))
        return None

    map_size = map_size_df.values[0]

    logger.debug('Map size load complete! map size: {}'.format(map_size))

    return map_size

def map_image(base_dname, map_image_fname):

    '''
    load map bitmap

    Parameters
    ----------
    base_dname : str
    map_image_fname : str
    
    Returns
    -------
    bitmap : ndarray of int
        bitmap data 
    '''

    map_image_path = os.path.join(base_dname, map_image_fname)
    logger.debug('Loading map image : {}'.format(map_image_path))

    map_img = cv2.imread(map_image_path, cv2.IMREAD_GRAYSCALE)
    
    # Value 1 is obstacle 
    bitmap = np.where(map_img==255, 0, 1)
    logger.debug('map image load complete! image shape:{}'.format(bitmap.shape))

    return bitmap

def ALIP_info(base_dname, ALIP_info_fname):
    '''
    Load true ALIP info file

    Parameters
    ----------
    base_dname : str
    ALIP_info_fname : str
    
    Returns
    -------
    ALIP_info : DataFrame
        columns = ['ALIP_start', 'ALIP_end']
    '''
    
    ALIP_info_path = os.path.join(base_dname, ALIP_info_fname)
    logger.debug('Loading ALIP info :{}'.format(ALIP_info_path))

    try:
        ALIP_info = pd.read_csv(ALIP_info_path)
    except FileNotFoundError:
        logger.debug('{} does not exist'.format(ALIP_info_path))
        return None
    
    ALIP_info.columns = ['ALIP_start', 'ALIP_end']

    logger.debug('ALIP info load complete! columns:{}, shape:{}'.\
            format(ALIP_info.columns, ALIP_info.shape))
    return ALIP_info

def load_point(base_dname, point_fname):
    '''
    Load point data file

    Parameters
    ----------
    base_dname : str
    point_fname : str
    
    Returns
    -------
    point : DataFrame
        columns = ['unixtime', 'x_position_m', 'y_position_m']
    '''
    point_path = os.path.join(base_dname, point_fname)
    logger.debug('Loading point data: {}'.format(point_path))

    try:
        point = pd.read_csv(point_path, names=['unixtime', 'x_position_m', 'y_position_m'])
    except FileNotFoundError:
        logger.debug('{} does not exists'.format(point_path))
        return None
    
    logger.debug('Point data load complete! columns:{}, shape:{}'.\
        format(point.columns, point.shape))
    
    return point

def area_info(base_dname, area_fname):
    '''
    Area info files
    
    Parameters
    ----------
    base_dname : str
    area_fname : str

    Returns
    -------
    area_info : DataFrame
        DataFrame columns = ['area', 'x_position_m', 'y_position_m', 'x_length', 'y_length']
    '''
    area_info_path = os.path.join(base_dname, area_fname)
    logger.debug('Loading Area info file:{}'.format(area_info_path))
    
    try:
        area_info = pd.read_csv(area_info_path)
    except FileNotFoundError:
        logger.debug('{} does not exist'.format(area_info_path))
        return None

    logger.debug('Area info load complete! columns:{}, shape:{}'.\
            format(area_info.columns, area_info.shape))
    
    return area_info

def area_weights_config(track, config_file='area_weights_config.ini'):
    '''
    Load area weights configuration file for E_error_deviation
    
    Parameters
    ----------
    track : str 
        'VDR' or 'PDR'
    config_file : str
        Loading configuration file name
    Retruns
    -------
    area_weights : list of float
    '''

    logger.debug('Loading area weights configuration file.')
    logger.debug('track: {}, config file: {}'.format(track, config_file))
    if not os.path.exists(config_file):
        logger.error('FileExistsError {} does not exist'.format(config_file))
        return None
        
    config_ini = ConfigParser()
    config_ini.optionxform = str
    config_ini.read(config_file, encoding='utf-8')

    area_weights = list()
    for area, weight in config_ini[track].items():
        logger.debug('{}: {}'.format(area, weight))
        area_weights.append(float(weight))
    
    return area_weights

def drop_ans_duplicated_with_ref(ans_point, ref_point):
    '''
    drop duplicated raw with reference point from answer point

    Parameters
    ----------
    ans_point : DataFrame
        total ground truth point
    ref_point : DataFrame
        reference point which is not for evaluation

    Returns
    -------
    ans_ref_nonduplicated : DataFrame
    '''

    ans_point = ans_point.drop_duplicates()
    ref_point = ref_point.drop_duplicates()
    df_concat = pd.concat([ans_point, ref_point], axis=0)

    # Duplicated row is True
    is_duplicated = (df_concat.duplicated(keep=False)) 
    ans_ref_nonduplicated = df_concat[[not(i) for i in is_duplicated]]

    return ans_ref_nonduplicated

def filter_evaluation_data_between_ALIP(evaluation_point, ALIP_info, ALIP_flag):
    '''
    Filter data between ALIP or not

    Parameters
    ----------
    evaluation_point: DataFrame
        DataFrame columns = ['unixtime', 'x_position_m', 'y_position_m']
    ALIP_info : DataFrame
        ALIP period time information
    ALIP_flag : boolean
        filter point is between ALIP or not

    Returns
    -------
    eval_point : DataFrame
        evaluation point for indicators, index
    '''

    # Check weather unixtime is between start and end time of ALIP_info
    def is_unixtime_between_ALIP(x):
        for ALIP_start, ALIP_end in zip(ALIP_info['ALIP_start'].values, ALIP_info['ALIP_end'].values):
            if ALIP_start<= x <=ALIP_end:
                return True
        return False
    
    if ALIP_flag:
        # Boolean array
        is_unixtime_between_ALIPinfo = evaluation_point['unixtime'].apply(lambda x:is_unixtime_between_ALIP(x))
        eval_point = evaluation_point[is_unixtime_between_ALIPinfo]
        logger.debug('evaluation point BETWEEN ALIP period is selected')

    else:
        is_unixtime_out_of_ALIPinfo = [not i for i in evaluation_point['unixtime'].apply(lambda x:is_unixtime_between_ALIP(x))]
        eval_point = evaluation_point[is_unixtime_out_of_ALIPinfo]
        logger.debug('evaluation point OUT OF ALIP period is selected')
    
    return eval_point

def BLE_info(base_dname, BLE_info_fname):
    '''
    Load true ble info file

    Parameters
    ----------
    base_dname : str
    BLE_info_fname : str
    
    Returns
    -------
    BLE_info : DataFrame
        columns = ['mac_address', 'orientatio', 'height_m', 'x_position_m', 'y_position_m', 'Ptx', 'Lux']
    '''
    
    BLE_info_path = os.path.join(base_dname, BLE_info_fname)
    logger.debug('Loading BLE info :{}'.format(BLE_info_path))

    try:
        BLE_info = pd.read_csv(BLE_info_path)
    except FileNotFoundError:
        logger.debug('{} does not exist'.format(BLE_info_path))
        return None

    logger.debug('BLE info load complete! columns:{}, shape:{}'.\
            format(BLE_info.columns, BLE_info.shape))

    return BLE_info

def map_color(map_obstacle_color, map_trajectory_color, map_ref_color, map_BLE_color):
    '''
    Load map color

    Parameters
    ----------
    map_obstacle_color : str
    map_trajectory_color : str
    map_ref_color : str
    map_BLE_color : str

    Returns
    -------
    map_color : list
    '''
    
    map_color = [map_obstacle_color, map_trajectory_color, map_ref_color, map_BLE_color]
    
    return map_color

def map_makersize(map_trajectory_size, map_ref_size, map_BLE_size, map_grid):
    '''
    Load map color

    Parameters
    ----------
    map_obstacle_color : str
    map_trajectory_color : str
    map_ref_color : str
    map_BLE_color : str
    map_grid : str

    Returns
    -------
    map_makersize : list
    '''

    if map_grid is 'True':
        map_grid = True
    else:
        map_grid = False
    
    map_makersize = [map_trajectory_size, map_ref_size, map_BLE_size, map_grid]

    return map_makersize
