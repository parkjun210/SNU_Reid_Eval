# SNU_ReID
## Detection & ReID Pipeline를 위한 inference 및 test 코드


# Environments
Pytorch >= 1.13.0

Python >= 3.7.0

```
git clone https://github.com/parkjun210/SNU_Reid_Eval.git
cd SNU_ReID_Eval
conda create -n <ENV_name> python=3.7
conda activate <ENV_name>
pip install tqdm einops opencv-python yacs tensorboard attributedict pandas matplotlib seaborn motmetrics lap
pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
```


# Directory 설명

```
|──DATASET : market1501, PRW, MOT17 등 dataset을 저장하는 폴더
|──SNU_ReID
    |── results : inference결과가 저장되는 경로
    |── SNU_PersonDetection : Detection 모델 및 코드 경로
    |── SNU_PersonReID : ReID에 필요한 모델 및 코드 경로
    |── weights : inference에 필요한 Detection + ReID 모델들의 weight
    |── reid.cfg : 사용하는 모델들의 파라미터 (변경 x)
    |── config.py : infer, test시에 필요한 경로 및 파라미터 설정 
    |── infer.py : inference용 코드
    |── test.py : test용 코드

```

## DATASET 구성

#### dataset 폴더 구성 주의 사항: dataset 폴더는 python 코드보다 상위에 존재함

```
|── DATASET : dataset을 저장하는 폴더
    |── {dataset 이름}
        |── bounding_box_test
        |── bounding_box_train
        |── gt_bbox
        |── gt_query
        |── query
    |── {dataset 이름}
    |── {dataset 이름}
    makelr.py

|──SNU_ReID
   .
   .
   .

```


# Pretrained Weights

Inference 및 Test에 필요한 웨이트는 detection weight와 reid weight가 있다.

[여기](https://drive.google.com/drive/folders/1Tc0NUviqcDMYbIYvT-fQE6dp92NnvSO8?usp=drive_link)에서 필요한 웨이트를 다운받아 weights폴더에 위치하면된다.

이후 config.py에서 

--detection_weight_file
--reid_weight_file

argument에 대한 경로값들을 수정해 원하는 웨이트를 사용한다.


# Configuration

Inference 및 Test에 사용할 경로 및 파라미터 설정은 config.py에서 한다.

### Directory parameter

```

--infer_data_dir : Detection + ReID pipeline을 돌릴 이미지들의 경로

--dataset_root_dir : 데이터셋 경로 (default : '../DATASET/')

--dataset_name : ReID에서 갤러리로 사용하고자 하는 데이터셋 이름 (예: market1501, PRW, MOT17)

--detection_weight_file : 사용할 detection weight 경로

--reid_weight_file : 사용할 ReID weight 경로

--gt_txt_path : 사용할 GT txt 경로

--use_GT_IDs : result 결과에 GT label 표시

--video : result image 결과를 병합한 video 생성 여부


```

# Inference

detection 및 reid를 진행할 pretrained_weight 파일들을 weights 폴더에 위치하고 config.py에서 경로 설정

python util.make_gt.py를 통해 gt_revised.txt 파일 생성
(gt.txt 파일을 읽어서 frame, class, visibility, bbox scope 등을 고려, default는 1920x1080 size)

python infer.py를 통하여 evaluation 진행

```
python util/make_gt.py --path <path/to/gt.txt>
python infer.py --use_GT_IDs --video
```

Inference는 infer_data_dir 경로에 있는 이미지들에 대해 detection + ReID를 수행한다.

지정한 갤러리와 비교해서 각 이미지마다 검출된 ID 예측값을 출력한다.

--use_GT_IDs: 이 flag를 추가시 result image에 GT label 표시
--video: 이 flag 추가시 result images를 병합한 video 생성

# GT.txt 구성

|Position|Name|Description|
|:---:|:---:|:---|
| 1 | Frame number | Indicate at which frame the object is present |
| 2 | Identity number | Each pedestrian trajectory is identified by a unique ID (􀀀1 for detections) |
| 3 | Bounding box left | Coordinate of the top-left corner of the pedestrian bounding box |
| 4 | Bounding box top | Coordinate of the top-left corner of the pedestrian bounding box |
| 5 | Bounding box width| Width in pixels of the pedestrian bounding box |
| 6 | Bounding box height| Height in pixels of the pedestrian bounding box |
| 7 | Confidence score | DET: Indicates how confident the detector is that this instance is a pedestrian. GT: It acts as a flag whether the entry is to be considered (1) or ignored (0). |
| 8 | Class | GT: Indicates the type of object annotated |
| 9 | Visibility | GT: Visibility ratio, a number between 0 and 1 that says how much of that object is visible. Can be due to occlusion and due to image border cropping. |

|Class|ID|
|:---|:---:|
|Pedestrian | 1|
|Person on vehicle | 2|
|Car | 3|
|Bicycle | 4|
|Motorbike | 5|
|Non motorized vehicle | 6|
|Static person | 7|
|Distractor | 8|
|Occluder | 9|
|Occluder on the ground | 10|
|Occluder full | 11|
|Reflection | 12|