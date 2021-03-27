<div align="center">
<a href=https://unit.aist.go.jp/harc/xDR-Challenge-2020/><img src="images/banner-big.png" title="xDR Challenge 2020" width='500px'>
</a>
</div>

# xDR-Challenge-2020-evaluation
[日本語版(Japanese) README](README_JP.md)  
People who are involved in indoor positioning technology can calculate their competition's index for xDR Challenge 2020.  
This evaluation tool is to show the example of usage of indicators for the people who do not join the competition and guarantee the competition faireness.  
The indicator and requiremet that are necessary for evaluating index are calculated by [LTS-benchmark-tool](https://github.com/PDR-benchmark-standardization-committee/LTS-benchmark-tool/tree/xDR-Challenge-2020)   
If you want see the detail of indicator and requirement calculation, see [LTS-benchmark-tool](https://github.com/PDR-benchmark-standardization-committee/LTS-benchmark-tool/tree/xDR-Challenge-2020)   

| **Index**  | **Corresspond Indicator and Requirement**| **Description**                                          |
 ---         |---                                  |---                                       
| I_ce       | Circular Error (CE)                 | Check the distance between trajection and correct point        |
| I_ca       | Circular Accuracy (CA)              | Check the error distribution in each area                      | 
| I_eag      | Error Accumulation Gradient (EAG)   | Check trajection that is far from correction points is accurate|
| I_velocity | Requirement for Moving Velocity     | Check trajection velocity is within human walking speed        |
| I_obstacle | Requirement for Obstacle Avoidance  | Check trajection points exists obstacle human cannot enter     |
| I_coverage | Requirement for Trajectory Coverage | Check percentage of trajection points in true points           |

## Example of Evaluation Result
You can calculate each trajection index for xDR Challenge 2020 competition 
<div align="cenetr">
<img src="images/result_graph.png" title="graph of index result" width='700px'>
</div>


## Requirement
```
python==3.6.10  
numpy==1.18.1  
pandas==1.0.1  
texttable==1.6.2  
tqdm==4.43.0  
opencv-python==4.2.0.34  
matplotlib==3.1.3 
scipy==1.4.1
seaborn==0.10.1  
```

## Description of Files

| **Filename**           | **Description**                                                                    |
 ---                     |---                                       
| main.py                | Execute evaluation script for index                                                | 
| index_evaluation.py    | Module for calculating index                                                       |
| dataloader.py          | Module for loading ground truth data, estimation data                              |
| utils.py               | General functions to create result directory, stdout result                        |
| index_utils.py         | Specific functions to process index                                                |
| index_weights.ini      | Index weights to evaluate competition score                                        |
| demo_area_weights.ini  | Demo estimation's area weights                                                     |
| requirements.txt       | Python library package version                                                     |
| data_config.ini        | data configuration file to evaluate sample data for xDR Challenge 2020 competition|

## Usage
### Step.1 Install
```
git clone --recursive https://github.com/PDR-benchmark-standardization-committee/xDR-Challenge-2020-evaluation.git
cd xDR-Challenge-2020-evaluation
pip install -r requirements.txt
```

### Step.2 Place estimation files
Place each track's estimation files at [estimatiion_folder]/PDR and [estimation_folder]/VDR respectively.  
If you want to evaluate demo estimation files, you don't need to prepare estimation files.
```
xDR-Challenge-2020-evaluation/
    ├ estimation_folder/
    │       ├ VDR/
    |       |  └ VDR_Traj_No*.txt [**VDR esimation files**]
    |       |
    │       └ PDR/
    |          └ PDR_Traj_No*.txt [**PDR esimation files**]
    │
    ├ groud_truth_folder/
    |       ├ BLE_Beacon/
    |       |  └ BLE_info.csv
    |       |
    |       ├ VDR_ALIP/
    |       |  └ VDR_ALIP_info_No*.csv
    |       |
    |       ├ VDR_Ans/
    |       |  └ VDR_Ans_No*.csv
    |       |
    |       ├ VDR_Map/
    |       |  ├ Map_image.bmp
    |       |  ├ Map_size.csv
    |       |  └ VDR_Area.csv
    |       |
    |       ├ VDR_Module/
    |       |  └ VDR_Sens_No*.txt
    |       |
    |       ├ VDR_Ref/
    |       |  └ VDR_Ref_No*.csv
    |       |
    |       ├ PDR_ALIP/
    |       |  └ PDR_ALIP_info_No*.csv
    |       |
    |       ├ PDR_Ans/
    |       |  └ PDR_Ans_No*.csv
    |       |
    |       ├ PDR_Map/
    |       |  ├ Map_image.bmp
    |       |  ├ Map_size.csv
    |       |  └ PDR_Area.csv
    |       |
    |       ├ PDR_Module/
    |       |  └ PDR_Sens_No*.txt
    |       |
    |       ├ PDR_Ref/
    |       |  └ PDR_Ref_No*.csv
    |       |
    │       └ data_config.ini
    │
    ├ main.py
    ├ index_evaluation.py
    ├ index_utils.py
    ├ utils.py
    ├ dataloader.py
    ├ index_weights.ini
    ├ demo_area_weights.ini
    ├ requirements.txt
    └ README.md
```

### Step.3 Place directory structure configuration 
You need to prepare configuration file that correspond to ground truth folder to evaluate.  
If you want to use your own groud truth file, please edit [demo_ground_truth/demo_data_config.ini] and place at groud truth folder.  
Demo groud truth configuration file is already prepared, so you don't need edit configuration file,  
just keep next step.

```
; Folder name of answer data
[ANSWER]
ground_truth_dname = 'groud_truth_folder'

[PDR]
map_dname = 'PDR_Map'
ans_dname = 'PDR_Ans'
ref_dname = 'PDR_Ref'
ALIP_dname = 'PDR_Bup'
BLE_dname = 'BLE_Beacon'

map_image_fname = 'Map_image.bmp'
map_size_fname = 'Map_size.csv'
area_fname = 'PDR_Area.csv'
ref_fname = 'PDR_Ref_No{}.csv'
ans_fname = 'PDR_Ans_No{}.csv'
ALIP_info_fname = 'PDR_Bup_info_No{}.csv'
BLE_info_fname = 'BLE_info.csv'

map_obstacle_color = 'gray'
map_trajectory_color = 'green'
map_ref_color = 'orange'
map_ble_color = 'blue'

map_trajectory_size = '0.2'
map_ref_size = '0.3'
map_ble_size = '2'
map_grid = 'False'

[VDR]
; Please write folder and file name for evaluation as [PDR]
```

### Step.4 Evaluation
You need to select estimation and ground truth folder path for evaluation 
```
python main.py [estimation_path] [ground_truth_path]
```

If you want to see the demo estimation score results, you just execute following script
```
python main.py estimation_folder groud_truth_folder
```

Results are saved at estimation files folder.  
If you execute the evaluation for demo_estimation files, the score is saved at following folder.

```
estimation_folder/
  | VDR/
  | └ result/
  |    ├ indicator
  |    | ├ CA
  |    | | ├ Traj_No*_area*_CA.png
  |    | | └ Traj_No*_CA.csv
  |    | |
  |    | ├ CE
  |    | | ├ CE_total_cumulative_sum.csv
  |    | | ├ CE_total_cumulative_sum.png
  |    | | ├ CE_total_histgram.png
  |    | | ├ Traj_No*_CE.csv
  |    | | ├ Traj_No*_CE_debug.csv
  |    | | └ Traj_No*_CE_histgram.png
  |    | |
  |    | ├ EAG
  |    | | ├ EAG_total_cumulative_sum.csv
  |    | | ├ EAG_total_cumulative_sum.png
  |    | | ├ EAG_total_histgram.png
  |    | | ├ Traj_No*_EAG.csv
  |    | | ├ Traj_No*_EAG_debug.csv
  |    | | └ Traj_No*_EAG_histgram.png
  |    | |
  |    | ├ requirement_obstacle
  |    | | └ Traj_No*_obstacle.csv
  |    | |
  |    | ├ requirement_velocity
  |    | | └ Traj_No*_moving_velocity.csv
  |    | |
  |    | ├ Trajectory
  |    | | └ Tra_No*.png
  |    | |
  |    | ├ file_indicator.csv
  |    | └ total_indicator.csv
  |    |
  |    └ index
  |      ├ file_index.csv
  |      └ total_index.csv
  └ PDR/
    └result/ [***Almost the same as VDR result folder***]
```

## Optional Arguments
### 1. Select track
You can select track to evaluate.  
In default, both PDR and VDR score are calculated.

```
python main.py estimation_folder groud_truth_folder --VDR --PDR
```

### 2. Select files
You can choose specific estimation file to evaluate index.  
If you execute following script, [estimation_folder/VDR/VDR_Traj_No1.txt] index are evaluated.

```
python main.py estimation_folder groud_truth_folder --VDR --file VDR_Traj_No1.txt 
```

### 3. Select index
You can select competition index to calculate.  
In default, all index are calculated.

```
python main.py estimation_folder groud_truth_folder --I_ce --I_ca --I_eag --I_velocity --I_obstacle
```

### 4. Select index weights  
You can change index weights to calculate competition score in index_weights.ini  
Default index weights is below.
```
<config.ini>
;weights for each index
[WEIGHTS]
I_ce = 0.25
I_ca = 0.20
I_eag = 0.25
I_velocity = 0.15
I_obstacle = 0.15
```

### 5. Select parameters

You can select percentile to calculate I_ce and I_eag.  
In default, 50 percentile is used.  
```
python main.py estimation_folder groud_truth_folder --CE_percentile 30 --EAG_percentile 75
```

You can select threshold velocity for I_velocity.  
In default, I_velocity is calculated by threshold 1.5 m/s.  
```
python main.py estimation_folder groud_truth_folder --velocity 1.8
```

You can select band width to calculate I_ca by Kernel Density Estimation  
If you do not select band_width, scipy default band widht is used.  
```
python main.py estimation_folder groud_truth_folder --band_width 1.4
```

In default, I_ca is caluculated by Kernel Density Estimation, you can switch to use 2D histgram.    
```
python main.py estimation_folder groud_truth_folder --CA_hist
```

### 6. Use pre-defined area weights
You can use pre-defined area weights to calculate I_ca.  
You need to prepare area weights configuration ini file.  
Please see configuration format at [demo_area_weights.ini].  
If you do not select area weights configuration file path,  
area weights are set as the ratio of each area's answer points for total area answer points.  
```
; demo_area_weights.ini
[VDR]
area1 = 0.3
area2 = 0.3
area3 = 0.4

[PDR]
area1 = 0.4
area2 = 0.6
```
Please select area weigths configuration path
```
python main.py estimation_folder groud_truth_folder --area_weights demo_area_weights.ini
```

## Licence
Copyright (c) 2020 Satsuki Nagae and PDR benchmark standardization committee.  
xDR-Challenge-2020-evaluation is open source software under the [MIT license](LICENSE).  

## Reference 
- [xDR Challenge in industrial Scenario in 2020](https://unit.aist.go.jp/harc/xDR-Challenge-2020/)  
- [Ryosuke Ichikari, Katsuhiko Kaji, Ryo Shimomura, Masakatsu Kourogi, Takashi Okuma, Takeshi Kurata: Off-Site Indoor Localization Competitions Based on Measured Data in a Warehouse, Sensors, vol. 19, issue 4, article 763, 2019.](https://www.mdpi.com/1424-8220/19/4/763/htm#)
