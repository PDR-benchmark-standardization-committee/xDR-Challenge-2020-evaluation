<div align="center">
<a href=https://unit.aist.go.jp/harc/xDR-Challenge-2020/><img src="images/banner-big.png" title="xDR Challenge 2020" width='500px'>
 </a>
</div>

# xDR-Challenge-2020-evaluation
屋内測位に関わる人を対象とした、xDR Challenge 2020コンペティションで使われる指数の計算を行えるツールです。  
本ツールの目的は評価指標の使用例としての指数を実際に計算できることと、コンペの評価の透明性を高めることです。  
指標と必要条件はコンペの指数を計算するために必要な値で、[LTS-benchmark-tool](https://github.com/PDR-benchmark-standardization-committee/LTS-benchmark-tool)を用いて計算されます。  
指標と必要条件の具体的な計算内容を見たい場合は、[LTS-benchmark-tool](https://github.com/PDR-benchmark-standardization-committee/LTS-benchmark-tool)をご覧ください。  
以下が、計算可能な指数の概要と、対応する指標と必要条件になります

| **指数**   | **対応する指標と必要条件**                       | **概要**                                                    |
 ---         |---                                               |---                                       
| I_ce       | 誤差絶対量: CE (Circular Error)                  | 正解座標と時間的最近傍の軌跡の距離が近いか評価              |
| I_ca       | 誤差分布偏移: CA (Circular Accuracy)             | 地図上のエリアごとの正解座標との誤差の分布を評価            | 
| I_eag      | 誤差累積速度: EAG (Accumulation Gradient)        | 位置補正のための座標からの誤差の累積スピードを評価          |
| I_velocity | 移動速度基準: Requirement for Moving Velocity    | 軌跡の速度が人間の歩行速度(1.5 m/s)以下であるか評価         |
| I_obstacle | 軌跡経路基準: Requirement for Obstacle Avoidance | 地図上の軌跡が人間が侵入できない障害物を通過していないか評価|

## 評価結果例
下表のようなxDR Challenge 2020 のコンペティションで使用される指数の値を各推定軌跡ごとに求めることが可能です。
<div align="cenetr">
<img src="images/result_graph.png" title="graph of index result" width='700px'>
</div>


## 必要条件
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

## ファイルの概要

| **ファイル名**         | **概要**                                                                 |
 ---                     |---                                       
| demo_groud_truth       | デモ用正解値データ. ディレクトリ構造を記載した設定ファイルを配置してます |
| demo_estimation        | デモ用推定軌跡データ                                                     |
| main.py                | 評価実行用スクリプト                                                     | 
| index_evaluation.py    | 指数計算モジュール                                                       |
| dataloader.py          | 正解データ, 推定軌跡読み込みモジュール                                   |
| utils.py               | フォルダ作成、結果出力など汎用的な処理をまとめたスクリプト               |
| index_utils.py         | 指数を扱うための関数をまとめたスクリプト                                 |
| index_weights.ini      | コンペスコアを計算するための指数の重みの設定ファイル                     |
| demo_area_weights.ini  | デモ推定軌跡用のエリア重み設定ファイル                                   |
| requirements.txt       | Pythonの必要ライブラリのバージョンをまとめたファイル                     |
| data_config_xDR_Challenge_2020_sample_data.ini| xDR Challenge 2020 サンプルデータを読み込むための設定ファイル|

## 使用方法
### Step.1 インストール
```
git clone --recursive https://github.com/PDR-benchmark-standardization-committee/xDR-Challenge-2020-evaluation
cd xDR-Challenge-2020-evaluation
pip install -r requirements.txt
```

### Step.2 推定ファイルを配置
PDR, VDRの推定軌跡ファイルをそれぞれ[estimatiion_folder]/PDR, [estimation_folder]/VDRに配置してください。  
デモデータの評価を行いたい場合、ご自身の推定軌跡ファイルを用意する必要はありません。  

```
xDR-Challenge-2020-evaluation/
    ├ estimation_folder (demo_estimation)/
    │       └ VDR/[**VDR esimation files**]
    │       └ PDR/[**PDR estimation files**]
    │
    ├ groud_truth_folder (demo_ground_truth)/
    │       └ [**data config ini file**]
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

### Step.3 正解値データのディレクリ構造を記載した設定ファイルを用意
正解データを読み込むために、正解値データのディレクトリ名、  
ファイル名を記載した設定ファイルを準備する必要があります。  
ご自身の用意した正解データを利用する際は、demo_ground_truthのフォルダにあるdemo_data_config.iniファイルを  
ご自身の正解データに合わせて修正し、正解データのディレクトリに配置してください。  
以下のような設定ファイルをご自身の正解値データに合わせて作成してください。  
```
; 正解値データフォルダ名
[ANSWER]
ground_truth_dname = 'demo_ground_truth'

[PDR]
; 各評価用データのディレクトリ名
map_dname = 'PDR_Map'
ans_dname = 'PDR_Ans'
ref_dname = 'PDR_Ref'
bup_dname = 'PDR_Bup'

; 各評価用データのファイル名
map_image_fname = 'Map_image.bmp'
map_size_fname = 'Map_size.csv'
area_fname = 'Area.csv'
ref_fname = 'PDR_Ref_No{}.csv'
ans_fname = 'PDR_Ans_No{}.csv'
bup_info_fname = 'PDR_Bup_info_No{}.csv'

[VDR]
; PDRと同様にディレクトリ名・ファイル名を記載
```
デモデータの評価を行いたい場合、設定ファイルが既にデモ用正解値データのフォルダ内に配置されていますので、  
設定ファイルを用意する必要はありません。  

### Step.4 評価の実行
評価を行う推定軌跡と正解データのフォルダのパスをコマンドライン引数に入力する必要があります。
```
python main.py [estimation_path] [ground_truth_path]
```
デモデータの評価を実行したい場合は、以下のスクリプトを実行してください
```
python main.py demo_estimation demo_ground_truth
```

指数と、対応する指標と必要条件の評価結果が推定軌跡のフォルダ内に保存されます。  
デモデータの評価を行った場合、以下のパスに結果が保存されます。

```
demo_estimation/
  └ VDR/
    └ results/
       ├ indicator
       └ index
         ├ file_index.csv
         └ total_index.csv
```


## コマンドライン引数
以下のコマンドライン引数を追加することが可能となっています。

### 1. PDR, VDRの選択
PDR, VDR、どちらの評価を行うか選択することができます。  
引数なしの場合は、PDR, VDR両方とも評価されます。

```
python main.py demo_estimation demo_ground_truth --VDR --PDR
```

### 2. 評価するファイルを選択
特定の軌跡ファイルを指定して、評価するファイルを選択することができます。  
例えば、以下のようなコマンドライン引数で実行した場合、  
[demo_estimation/VDR/VDR_Traj_No2.txt]の評価が実行されます。

```
python main.py demo_estimation demo_ground_truth --VDR --file VDR_Traj_No2.txt 
```

### 3. 計算する指標・必要条件の選択
計算を実行したい指数を選択することができます。  
引数なしの場合は、全ての指数の計算が実行されます  

```
python main.py demo_estimation demo_ground_truth --I_ce --I_ca --I_eag --I_velocity --I_obstacle
```

### 4. スコア計算のための各指数の重みを選択
[index_weights.ini]ファイルを書き換えることで、  
コンペスコアを求めるための各指数の重みを指定することができます。
デフォルトの各指数の重みは以下のようになっています。  
```
<config.ini>
;weights for each index
[WEIGHTS]
I_ce = 0.20
I_ca = 0.20
I_eag = 0.20
I_velocity = 0.20
I_obstacle = 0.20
```

### 5. パラメータの選択

I_ce, I_eagで計算するパーセント点を指定することができます。  
引数なしの場合は50パーセント点の値が計算されます。  

```
python main.py demo_estimation demo_ground_truth --CE_percentile 30 --EAG_percentile 75
```

I_velocityで用いられる速度しきい値を指定することができます。  
引数なしの場合は、1.5 m/s がしきい値として用いられます。

```
python main.py demo_estimation demo_ground_truth --velocity 1.8
```

I_caの計算でのカーネル密度推定のバンド幅を指定することができます。  
バンド幅の指定がない場合は、scikit-learnのデフォルトのバンド幅が用いられます。
```
python main.py demo_estimation demo_ground_truth --band_width 1.4
```

I_caの計算を二次元ヒストグラムで行うように切り替えることが可能となっています。  
引数なしの場合は、scipyのデフォルトパラメータのカーネル密度推定によってCAが計算されます  

```
python main.py demo_estimation demo_ground_truth --CA_hist
```

### 6. 事前に指定したエリア重みを使用する
I_caの計算に用いるエリア重みに、ご自身で設定した値を指定することができます。  
その場合、エリア重みを記述した設定ファイルを用意する必要があります。  
エリア重みの設定ファイルを指定しなかった場合、  
各エリアに含まれる正解値の全正解値に対する割合が各エリアの重みとなります。  
エリア重みの設定ファイルはデモデータ用のエリア重み設定ファイルのように作成してください。  
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

用意したエリア重みの設定フィアルのパスを指定してください。
```
python main.py demo_estimation demo_ground_truth --area_weights demo_area_weights.ini
```

## デモデータでの実行結果
デモ用の正解値、推定軌跡データを利用することで、評価ツール実行の様子を確認することができます。  
計算された指数は[demo_estimation/VDR/result/index] に保存されます。  
以下のような推定軌跡に対して評価を行った結果です。  
VDR_Traj_No2.txt  
<img src="images/VDR_sample.png" width=280px>  

```                                                 
(python36) $ python main.py demo_estimation --VDR
track: ['VDR']
index: ['I_ce', 'I_ca', 'I_eag', 'I_velocity', 'I_obstacle']
VDR_Traj_No1.txt evaluation progress...
100%|█████████████████████████████████████| 9006/9006 [00:02<00:00, 3168.33it/s]
VDR_Traj_No2.txt evaluation progress...
100%|█████████████████████████████████████| 7868/7868 [00:01<00:00, 4276.67it/s]
VDR_Traj_No3.txt evaluation progress...
100%|█████████████████████████████████████| 8957/8957 [00:02<00:00, 3039.98it/s]
VDR_Traj_No4.txt evaluation progress...
100%|█████████████████████████████████████| 7716/7716 [00:01<00:00, 4169.47it/s]
VDR_Traj_No5.txt evaluation progress...
100%|█████████████████████████████████████| 9054/9054 [00:03<00:00, 2485.73it/s]
VDR_Traj_No6.txt evaluation progress...
100%|█████████████████████████████████████| 7718/7718 [00:02<00:00, 3726.62it/s]
-------- file index --------
   file_name        I_ce     I_ca     I_eag    I_velocity   I_obstacle
======================================================================
VDR_Traj_No1.txt   85.273   51.256   98.448      94.137       86.725  
VDR_Traj_No2.txt   77.126   53.816   94.461      98.081       90.180  
VDR_Traj_No3.txt   89.130   62.959   100.000     95.132       85.035  
VDR_Traj_No4.txt   89.409   63.069   11.275      97.564       91.464  
VDR_Traj_No5.txt   81.077   31.457   98.078      94.621       77.852  
VDR_Traj_No6.txt   90.279   28.713   97.878      94.545       91.440   

-------- total index --------
 I_ce     I_ca    I_eag    I_velocity   I_obstacle   Score 
===========================================================
85.382   48.545   83.356     95.680       87.116     80.016 

-------- file indicator --------
   file_name       CE50     CA     EAG50   requirement_velocity   requirement_obstacle
======================================================================================
VDR_Traj_No1.txt   5.271   4.874   0.080          0.571                  0.133        
VDR_Traj_No2.txt   7.633   4.618   0.158          0.264                  0.098        
VDR_Traj_No3.txt   4.152   3.704   0.029          0.568                  0.150        
VDR_Traj_No4.txt   4.071   3.693   1.780          0.365                  0.085        
VDR_Traj_No5.txt   6.488   6.854   0.087          0.611                  0.221        
VDR_Traj_No6.txt   3.819   7.129   0.091          0.529                  0.086         

-------- total indicator --------
CE50     CA     EAG50   requirement_velocity   requirement_obstacle
===================================================================
5.239   5.145   0.371          0.484                  0.129         
```

## xDR Challenge 2020 サンプルデータでの評価
xDR Challenge 2020 の配布サンプルデータで評価を行う場合、データ読み込みのための設定ファイルである  
[data_config_xDR_challenge_2020_sample_data.ini]をサンプルデータのフォルダ直下に配置してください。  
[**注意**]:   
サンプルデータの参照点は正解点として扱われます。  
また、BUP情報がサンプルデータには含まれていないため、EAGの評価は行われません。  
EAGでの評価を行うためには、BUP情報を記載したファイルをご自身で作成していただく必要があります。  
また、エリア分割データがサンプルデータには含まれないため、CAの計算は全エリアの正解値を用いて行われます。    

```
xDR-Challenge-2020-evaluation/
    ├ sample data estimation folder/
    │       └ VDR/[**VDR esimation files**]
    │       └ PDR/[**PDR estimation files**]
    │
    ├ [sample data ground truth folder]/
    │       └ [data_config_xDR_challenge_2020_sample_data.ini]
    │
    ├ main.py
    ├ index_evaluation.py
    ├ index_utils.py
    ├ utils.py
    ├ dataloader.py
    ├ index_weights.ini
    ├ requirements.txt
    └ README.md
```

## ライセンス
Copyright (c) 2020 Satsuki Nagae and PDR benchmark standardization committee.  
xDR-Challenge-2020-evaluation is open source software under the [MIT license](LICENSE).  

## 参考文献 
- [xDR Challenge in industrial Scenario in 2020](https://unit.aist.go.jp/harc/xDR-Challenge-2020/)  
- [Ryosuke Ichikari, Katsuhiko Kaji, Ryo Shimomura, Masakatsu Kourogi, Takashi Okuma, Takeshi Kurata: Off-Site Indoor Localization Competitions Based on Measured Data in a Warehouse, Sensors, vol. 19, issue 4, article 763, 2019.](https://www.mdpi.com/1424-8220/19/4/763/htm#)
