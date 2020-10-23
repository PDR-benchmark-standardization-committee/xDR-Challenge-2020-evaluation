# coding: utf-8
import math
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from logging import getLogger
from tqdm import tqdm
from scipy.stats import kde


tqdm.pandas()
logger = getLogger("__main__").getChild("index_evaluation")


class CalcIndex(object):
    def I_ce(self, CE):
        '''
        Calculate absolute error index

        Parameters
        ----------
        CE: list of float
            Circular Error (CE) (unit: m)

        Returns
        -------
        index : float
            absolute error index

        Notes
        -----
        I_ce = 100 - 10 * CE50           (CE50 < 1)
        I_ce = 100 - 100/29 * (CE50 - 1) (1 <= CE50 <= 30)
        I_ce = 0                         (30 < CE50)
        '''

        logger.debug('Calculate absolute error START')
        logger.debug('CE: {}'.format(CE))

        CE50 = np.median(CE)
        logger.debug('CE50: {}'.format(CE50))

        if CE50 < 1:
            index = 100 - 10 * CE50
        
        elif 1 <= CE50 <= 30:
            index = 100 - (100/29) * (CE50 - 1)
        
        elif 30 < CE50: 
            index = 0

        logger.debug('Calculate absolute error END')
        logger.debug('I_ce: {}'.format(index))
        
        return index
        
    def I_eag(self, EAG):
        '''
        Calculate relative error index

        Parameters
        ----------
        EAG: list of float
            Error Accumulation Gradient (unit: m/s)

        Returns
        -------
        index : float
            relative error index

        Notes
        -----
        I_eag = 100                             (EAG50 < 0.05)
        I_eag = 100 - 100/1.95 * (EAG50 - 0.05) (0.05 < EAG50 < 2.0)
        I_eag = 0                               (2.0 < EAG50)
        '''

        logger.debug('Calculate relative error START')   
        logger.debug('EAG: {}'.format(EAG))

        EAG50 = np.median(EAG)
        logger.debug('EAG50: {}'.format(EAG50))

        if EAG50 < 0.05:
            index = 100

        elif 0.05 <= EAG50 <= 2.0:
            index = 100 - (100/1.95) * (EAG50 - 0.05)
        
        elif 2.0 < EAG50:
            index = 0

        logger.debug('Calculate relative error END')   
        logger.debug('I_eag: {}'.format(index))

        return index

    def I_ca(self, area_weighted_CA):
        '''
        Calculate error deviation 

        Parameters
        ----------
        area_weihgted_CA: float
        
        Returns
        -------
        index : float
            error deviation index

        Notes
        -----
        I_ca = 100 - 10 * CA (Area_weighted_CA < 10)
        I_ca = 0                (0 < Area_weighted_CA)
        Area_weighted_CA = sum(weight * CA)

        '''
        logger.debug('Calculate error deviation START')
        logger.debug('Area_weighted_CA: {}'.format(area_weighted_CA))

        if area_weighted_CA <= 10:
            index = 100 - 10 * area_weighted_CA
        
        elif 10 < area_weighted_CA:
            index = 0
        
        else:
            raise ValueError('Area_weighted_CA:{}'.format(area_weighted_CA))

        logger.debug('Calculate error deviation END')
        logger.debug('I_ca: {}'.format(index))

        return index

    def I_velocity(self, velocity_flag):
        '''
        Calculate velocity error index

        Parameters
        ----------
        velocity_flag: list of 0/1

        Returns
        ------- 
        index : float 
            velocity error index
        
        Notes
        -----
        I_velocity is percentage of appropriate trajectory points those velocity is within
        reasonable human walking spped 1.5(m/s).

        I_velocity = 100 * appropriate_trajectory / total_trajectory
        '''
        logger.debug('Calculate velocity error START')
        
        index = 100 * (sum(velocity_flag) / len(velocity_flag))
        
        logger.debug('I_velocity : {}'.format(index))
        logger.debug('Calculate velocity error END')
        
        return index

    def I_obstacle(self, check_cordinate_count, obstacle_cordinate_count):
        '''
        Calculate obstacle error index

        Parameters
        ---------- 
        check_cordinate_count: list of int
            
        obstacle_cordinate_count: list of int
        
        Returns
        -------
        index : float
            obstacle error

        Notes
        -----
        I_obstacle is percentage of appropriate trajection point those points 
        on map doesn't exist obstacle
        
        I_obstacle = 100 * appropriate_trajection / total_trajection
        '''

        logger.debug('Calculate obstacle error START')

        index = 100.0 * (sum(check_cordinate_count) - sum(obstacle_cordinate_count)) / sum(check_cordinate_count)

        logger.debug('Calculate obstacle error END')
        logger.debug('I_obstacle : {}'.format(index))
        return index
