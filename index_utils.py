# coding: utf-8
import os 

import pandas as pd
import numpy as np
from collections import defaultdict

from logging import getLogger


logger = getLogger("__main__").getChild("utility")


class IndexHolder(object):
    def __init__(self):
        self.index_values = defaultdict(list)

    def add_index(self, index_name, index):
        self.index_values[index_name].append(index)
        
    def summarize_file_index(self):
        file_index = pd.DataFrame(self.index_values)
        return file_index

    def calc_total_index(self, weights, I_ce_total, I_eag_total):
        logger.debug('weights:{}'.format(weights))
        calc_index = [index_name for index_name in self.index_values.keys() if index_name != 'file_name']
        total_index_stats = {key : np.mean(self.index_values[key]) for key in calc_index}
        total_index_stats['I_ce'] = I_ce_total
        total_index_stats['I_eag'] = I_eag_total

        Score = 0
        for key, value in total_index_stats.items():
            if key is not 'I_coverage':
                logger.debug('{} : {}, weight: {}'.format(key, value, weights[key].values[0]))
                Score += weights[key] * value
        #trajectory percentage
        Score = Score * (value / 100)

        total_index_stats['Score'] = Score.values[0]

        total_index = pd.DataFrame(total_index_stats, index=['1',])

        return total_index

