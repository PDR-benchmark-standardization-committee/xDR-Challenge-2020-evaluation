# coding: utf-8
import os
import sys
import glob
import argparse
import re

import pandas as pd
from logging import getLogger, Formatter, StreamHandler, FileHandler, DEBUG, INFO

import dataloader
from index_evaluation import CalcIndex
import index_utils
import utils

sys.path.append('LTS-benchmark-tool')
from indicator_evaluation import CalcIndicator
import indicator_utils


def main(args):
    for track in args.track:
        logger.debug('- {}, {} evaluation START -'.format(args.trajection_folder, track))
        
        # Load data config 
        data_config_path = glob.glob(os.path.join(args.ground_truth_folder, '*.ini'))[0]
        conf = dataloader.config(track, config_file=data_config_path)

        # Directory path to evaluate
        tra_dname = os.path.join(args.trajection_folder, track)
        logger.debug('tra_dname:{}'.format(tra_dname))

        # Load groundtruth files
        map_size = dataloader.map_size(conf['map_dname'], conf['map_size_fname'])
        map_image = dataloader.map_image(conf['map_dname'], conf['map_image_fname'])
        area_info = dataloader.area_info(conf['map_dname'], conf['area_fname'])
        map_color = dataloader.map_color(conf['map_obstacle_color'], conf['map_trajectory_color'], conf['map_ref_color'], conf['map_BLE_color'])
        map_makersize = dataloader.map_makersize(conf['map_trajectory_size'], conf['map_ref_size'], conf['map_BLE_size'], conf['map_grid'])

        # Create result save directory
        result_basedir = os.path.join(tra_dname, 'result')
        index_savedir = os.path.join(result_basedir, 'index')
        indicator_savedir = os.path.join(result_basedir, 'indicator') 
        
        for dir_path in [result_basedir, index_savedir, indicator_savedir]:
            utils.create_dir(dir_path)

        extension_types = ['*.txt', '*.csv']
        tra_files = []
        for ext_type in extension_types:
            keyword = os.path.join(tra_dname, ext_type)
            tra_files.extend([os.path.split(file_path)[-1] for file_path in sorted(glob.glob(keyword, recursive=True))])
        
        if args.file:
            tra_files = args.file

        logger.debug('trajection files:{}'.format(tra_files))

        # Instance to calculate index
        evaluation_index = CalcIndex()
        index_holder = index_utils.IndexHolder()

        # Instance to calculate indicator
        evaluation_indicator = CalcIndicator()
        indicator_holder = indicator_utils.IndicatorHolder()

        CE_total = []
        EAG_total = []

        for tra_filename in tra_files:
            Ans_Ref_count = 0
            no_match_count = 0
            logger.debug('{} Evaluation START'.format(tra_filename))
            print('{} evaluation progress...'.format(tra_filename))
 
            # Load trajectory files
            tra_data = dataloader.load_point(tra_dname, tra_filename)
            tra_num = re.sub("\\D", "", tra_filename)

            # Load ground truth files
            ref_point = dataloader.load_point(conf['ref_dname'], conf['ref_fname'].format(tra_num))
            ans_point = dataloader.load_point(conf['ans_dname'], conf['ans_fname'].format(tra_num))
            ALIP_info = dataloader.ALIP_info(conf['ALIP_dname'], conf['ALIP_info_fname'].format(tra_num))
            BLE_info = dataloader.BLE_info(conf['BLE_dname'], conf['BLE_info_fname'].format(tra_num))

            index_holder.add_index('file_name', tra_filename)
            indicator_holder.add_indicator('file_name', tra_filename)
            
            # prepare evaluation point
            if ref_point is None:
                evaluation_point = ans_point
            else:
                evaluation_point = dataloader.drop_ans_duplicated_with_ref(ans_point, ref_point)
                
            if ALIP_info is None:
                eval_point_outof_ALIP = ans_point
                eval_point_between_ALIP = pd.DataFrame(index=[], columns=['unixtime', 'x_position_m', 'y_position_m'])
            else:
                eval_point_outof_ALIP = dataloader.filter_evaluation_data_between_ALIP(evaluation_point, ALIP_info, ALIP_flag=False)
                eval_point_between_ALIP = dataloader.filter_evaluation_data_between_ALIP(evaluation_point, ALIP_info, ALIP_flag=True)

            # I_ce, CE
            if 'I_ce' in args.index:
                CE_dataset = evaluation_indicator.CE_calculation(tra_data, eval_point_outof_ALIP)
                CE_dataframe = CE_dataset['CE']
                CE = CE_dataframe.values.tolist()
                CE.sort()
                CE_count = len(CE)
                CE_no_match_count = CE.count(-1)
                del CE[:CE_no_match_count]
                if CE == []:
                    CE = [-1]
                CE_percentile = indicator_utils.calc_percentile(CE, args.CE_percentile)
                indicator_holder.add_indicator(f'CE{args.CE_percentile}', CE_percentile)

                CE_savedir = os.path.join(indicator_savedir, 'CE')
                CE_total.extend(CE)
                utils.create_dir(CE_savedir) 
                indicator_utils.save_indicator(data=CE, indicator_name='CE', save_dir=CE_savedir, save_filename=f'Traj_No{tra_num}_CE.csv')
                CE_hist = indicator_utils.draw_histgram(data=CE, indicator_name='CE', percentile=args.CE_percentile)
                indicator_utils.save_figure(CE_hist, save_dir=CE_savedir, save_filename=f'Traj_No{tra_num}_CE_histgram.png')
                indicator_utils.save_indicator_debug(data=CE_dataset, save_dir=CE_savedir, save_filename=f'Traj_No{tra_num}_CE_debug.csv')
                
                I_ce = evaluation_index.I_ce(CE)
                index_holder.add_index('I_ce', I_ce)
                Ans_Ref_count += CE_count
                no_match_count += CE_no_match_count

            # I_ca, CA    
            if 'I_ca' in args.index:
                if args.area_weights is None:
                    area_weights = indicator_utils.get_CA_area_weights(evaluation_point, area_info)
                else:
                    area_weights = dataloader.area_weights_config(args.area_weights)
        
                if area_weights is None:
                    logger.debug('CA is calculated for whole area')
                    if args.CA_hist:
                        CA, CA_fig = evaluation_indicator.CA_2Dhistgram_calculation(tra_data, evaluation_point)
                    else:
                        CA, CA_fig = evaluation_indicator.CA_KernelDensity_calculation(tra_data, evaluation_point, band_width=None)
                    CA_df = pd.DataFrame({'CA': CA}, index=[0])
                
                else:
                    logger.debug('CA is calculated for each area division')
                    CA, CA_df, CA_fig = evaluation_indicator.Area_weighted_CA_calculation(tra_data, evaluation_point, area_info, area_weights, args.CA_hist)
                
                indicator_holder.add_indicator('CA', CA)
                CA_savedir = os.path.join(indicator_savedir, 'CA')
                utils.create_dir(CA_savedir) 
                indicator_utils.save_dataframe(CA_savedir, f'Traj_No{tra_num}_CA.csv', CA_df)
                       
                if isinstance(CA_fig, list):
                    for i in range(len(CA_fig)):
                        CA_fig[i].suptitle(f'Traj_No{tra_num}_area{i+1}_CA')
                        indicator_utils.save_figure(CA_fig[i], save_dir=CA_savedir, save_filename=f'Traj_No{tra_num}_area{i+1}_CA.png')        
                else:
                    CA_fig.suptitle(f'Traj_No{tra_num}_CA')
                    indicator_utils.save_figure(CA_fig, save_dir=CA_savedir, save_filename=f'Traj_No{tra_num}_CA.png')
  
                I_ca = evaluation_index.I_ca(CA)
                index_holder.add_index('I_ca', I_ca)
        
            # I_eag, EAG
            if 'I_eag' in args.index:
                EAG_dataset = evaluation_indicator.EAG_calculation(tra_data, ref_point, eval_point_between_ALIP)
                EAG_dataframe = EAG_dataset['EAG']
                EAG = EAG_dataframe.values.tolist()
                EAG.sort()
                EAG_count = len(EAG)
                EAG_no_match_count = EAG.count(-1)
                del EAG[:EAG_no_match_count]
                if EAG == []:
                    EAG = [-1]
                EAG_percentile = indicator_utils.calc_percentile(EAG, args.EAG_percentile)
                indicator_holder.add_indicator(f'EAG{args.EAG_percentile}', EAG_percentile)

                EAG_savedir = os.path.join(indicator_savedir, 'EAG')
                EAG_total.extend(EAG)
                utils.create_dir(EAG_savedir)
                indicator_utils.save_indicator(data=EAG, indicator_name='EAG', save_dir=EAG_savedir, save_filename=f'Traj_No{tra_num}_EAG.csv')
                EAG_hist = indicator_utils.draw_histgram(data=EAG, indicator_name='EAG', percentile=args.EAG_percentile)
                indicator_utils.save_figure(EAG_hist, save_dir=EAG_savedir, save_filename=f'Traj_No{tra_num}_EAG_histgram.png')
                indicator_utils.save_indicator_debug(data=EAG_dataset, save_dir=EAG_savedir, save_filename=f'Traj_No{tra_num}_EAG_debug.csv')
                
                I_eag = evaluation_index.I_eag(EAG)
                index_holder.add_index('I_eag', I_eag)
                Ans_Ref_count += EAG_count
                no_match_count += EAG_no_match_count

            # I_velocity, Requirement for moving velocity
            if 'I_velocity' in args.index:
                moving_velocity_df = evaluation_indicator.requirement_moving_velocity_check(tra_data, args.velocity)
                indicator_holder.add_indicator('requirement_velocity', moving_velocity_df['velocity'].mean())
                velocity_savedir = os.path.join(indicator_savedir, 'requirement_velocity')
                utils.create_dir(velocity_savedir)
                indicator_utils.save_dataframe(velocity_savedir, f'Traj_No{tra_num}_moving_velocity.csv', moving_velocity_df)

                I_velocity = evaluation_index.I_velocity(list(moving_velocity_df['flag']))
                index_holder.add_index('I_velocity', I_velocity)

            # I_obstacle, Requirement for obstacle avoidance
            if 'I_obstacle' in args.index:
                obstacle_df = evaluation_indicator.requirement_obstacle_check(tra_data, map_image, map_size)
                if len(obstacle_df) == 0:
                    obstacle_ratio = -1
                else:
                    obstacle_ratio = sum(obstacle_df['obstacle_cordinate_count']) / sum(obstacle_df['check_cordinate_count'])
                
                indicator_holder.add_indicator('requirement_obstacle', obstacle_ratio)
                obstacle_savedir = os.path.join(indicator_savedir, 'requirement_obstacle')
                utils.create_dir(obstacle_savedir)
                indicator_utils.save_dataframe(obstacle_savedir, f'Traj_No{tra_num}_obstacle.csv', obstacle_df)
            
                I_obstacle = evaluation_index.I_obstacle(list(obstacle_df['check_cordinate_count']), 
                                                            list(obstacle_df['obstacle_cordinate_count']))
                index_holder.add_index('I_obstacle', I_obstacle)

            if 'I_coverage' in args.index:
                I_coverage = evaluation_index.I_coverage(Ans_Ref_count, no_match_count)
                index_holder.add_index('I_coverage', I_coverage)

            # Draw trajectory
            Tra_savedir = os.path.join(indicator_savedir, 'Trajectory')
            utils.create_dir(Tra_savedir)
            Trajectory_image = indicator_utils.draw_trajectory(tra_data, map_image, map_size, f'Trajectory_No{tra_num}', ref_point, BLE_info, map_color, map_makersize)
            indicator_utils.save_figure(Trajectory_image, save_dir=Tra_savedir, save_filename=f'Tra_No{tra_num}.png')

            logger.debug('{} Evaluation END'.format(tra_filename))

        # Show each file's index
        file_index_summary = index_holder.summarize_file_index()
        utils.stdout_dataframe(file_index_summary, title='file index')
        utils.save_csv(save_file=file_index_summary, save_dir=index_savedir, save_filename='file_index.csv')

        # Show total index
        I_ce_total = evaluation_index.I_ce(CE_total)
        I_eag_total = evaluation_index.I_eag(EAG_total)
        index_weights = dataloader.index_weights(config_file='index_weights.ini')
        total_index = index_holder.calc_total_index(index_weights, I_ce_total, I_eag_total)
        utils.stdout_dataframe(total_index, title='total index')
        utils.save_csv(save_file=total_index, save_dir=index_savedir,save_filename='total_index.csv')

        # Show each file's indicator
        file_indicator_summary = indicator_holder.summarize_file_indicator()
        utils.stdout_dataframe(file_indicator_summary, title='file indicator')
        utils.save_csv(save_file=file_indicator_summary, save_dir=indicator_savedir, save_filename='file_indicator.csv')

        # Show total indicator
        total_indicator = indicator_holder.calc_total_indicator(CE_total, EAG_total)
        utils.stdout_dataframe(total_indicator, title='total indicator')
        utils.save_csv(save_file=total_indicator, save_dir=indicator_savedir, save_filename='total_indicator.csv')
    
        # Draw histgram and cumulative sum for total CE and EAG
        if 'I_ce' in args.index:
            CE_total_hist = indicator_utils.draw_histgram(data=CE_total, indicator_name='CE', percentile=args.CE_percentile)
            indicator_utils.save_figure(CE_total_hist, save_dir=CE_savedir, save_filename=f'CE_total_histgram.png')
            CE_cumulative_sum = indicator_utils.draw_cumulative_sum(CE_total, 'CE')
            indicator_utils.save_figure(CE_cumulative_sum, save_dir=CE_savedir, save_filename=f'CE_total_cumulative_sum.png')
            indicator_utils.save_total_indicator(data=CE_total, indicator_name='CE', save_dir=CE_savedir, save_filename=f'CE_total_cumulative_sum.csv')

        if 'I_eag' in args.index:
            EAG_total_hist = indicator_utils.draw_histgram(data=EAG_total, indicator_name='EAG', percentile=args.EAG_percentile)
            indicator_utils.save_figure(EAG_total_hist, save_dir=EAG_savedir, save_filename=f'EAG_total_histgram.png')
            EAG_cumulative_sum = indicator_utils.draw_cumulative_sum(EAG_total, 'EAG')
            indicator_utils.save_figure(EAG_cumulative_sum, save_dir=EAG_savedir, save_filename=f'EAG_total_cumulative_sum.png')
            indicator_utils.save_total_indicator(data=EAG_total, indicator_name='EAG', save_dir=EAG_savedir, save_filename=f'EAG_total_cumulative_sum.csv')

        logger.debug('- {}, {} evaluation END -'.format(args.trajection_folder, track))
    
if __name__ == '__main__':  

    parser = argparse.ArgumentParser(description='XDR Challenge Evaluation Setting')

    parser.add_argument('trajection_folder', type=str, help='Set trajection folder name')

    parser.add_argument('ground_truth_folder', type=str, help='Set ground truth folder name')
    
    parser.add_argument('--config', type=str, default='config.ini', 
                        help='Configuration file name')

    parser.add_argument('--VDR', action='store_const', dest='track', default=['VDR','PDR'],
                        const=['VDR'],help='Set  VDR track')
    
    parser.add_argument('--PDR', action='store_const', dest='track', default=['VDR','PDR'],
                        const=['PDR'],help='Set  PDR track')
    
    parser.add_argument('--file', nargs='*', help='Select file name for evaluation')
                        
    parser.add_argument('--I_ce', action='append_const', dest='index', default=[],
                        const='I_ce', help='Calculate I_ce')

    parser.add_argument('--CE_percentile', type=int, default=50,
                        help='Calculate percentile of Circular Error')
    
    parser.add_argument('--I_ca', action='append_const', dest='index', default=[],
                        const='I_ca', help='Calculate I_ca')

    parser.add_argument('--area_weights', default=None, help='area weights configuration path')

    parser.add_argument('--CA_hist', action='store_true', help='Calculate CA by 2D histgram')

    parser.add_argument('--band_width', type=float, default=None, help='band width for kernel density')

    parser.add_argument('--I_eag', action='append_const', dest='index', default=[],
                        const='I_eag', help='Calculate I_eag')

    parser.add_argument('--EAG_percentile', type=int, default=50,
                        help='Calculate percentile of Error Accumulation Gradient')

    parser.add_argument('--I_velocity', action='append_const', dest='index', default=[],
                        const='I_velocity', help='Calculate I_velocity')
    
    parser.add_argument('--velocity', type=float, default=1.5, help='appropriate walking velocity (unit: m/s)')

    parser.add_argument('--I_obstacle', action='append_const', dest='index', default=[],
                        const='I_obstacle', help='Calculate I_obstacle')

    parser.add_argument('--debug', action='store_const', dest='level', default=INFO, const=DEBUG, 
                        help='Logger debug mode')

    args = parser.parse_args()
    args.index = ['I_ce', 'I_ca', 'I_eag', 'I_velocity', 'I_obstacle', 'I_coverage'] if not args.index else args.index
    correspondence_index_indicator = {'I_ce': 'CE', 
                                   'I_ca': 'CA',
                                   'I_eag': 'EAG', 
                                   'I_velocity': 'requirement_velocity',
                                   'I_obstacle': 'requirement_obstacle',
                                   'I_coverage': 'trajectory_percentage'}
    args.indicators = [correspondence_index_indicator[index] for index in args.index]

    #　Logger setting
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)

    formatter = Formatter('%(asctime)s - %(name)s - %(message)s')

    # Standard output handler
    stream_handler = StreamHandler()
    stream_handler.setLevel(args.level)
    stream_handler.setFormatter(formatter)

    # File output handler
    log_file_name = os.path.basename(__file__) + '.log'
    file_handler = FileHandler(log_file_name, 'a')
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.debug('track:{}, index:{}, indicators:{}'.format(args.track, args.index, args.indicators))
    
    print('track: {}'.format(args.track))
    print('index: {}'.format(args.index))
    main(args)
