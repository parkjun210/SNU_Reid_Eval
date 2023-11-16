import os

input_file_path = '../DATASET/MOT17-04-FRCNN_query/gt/gt.txt'  # 읽을 파일의 경로

output_file_path =  os.path.join(os.path.dirname(input_file_path),'MOT17_004_FRCNN_gt_250.txt')   # 쓸 파일의 경로

with open(output_file_path, 'w') as output_file:
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            parts = line.strip().split(',')
            frame_number = int(parts[0])

            if frame_number >= 801:
                # Frame number와 Identity number 조정
                # adjusted_frame_number = frame_number - 801
                adjusted_frame_number = frame_number
                
                # 1: pedestrian, 2: Person on vehicle, 7:Static person
                if not int(parts[-2]) in [1, 2, 7]: 
                    continue
                
                # considered (1) or ignored (0)
                if not float(parts[-3]) in [1]:
                    continue
                
                # Visibility
                if float(parts[-1]) < 0.2:
                    continue
                
                if float(parts[2]) < 0:
                    parts[4] = str(float(parts[4]) + float(parts[2]))
                    parts[2] = '0'
                    
                if float(parts[3]) < 0:
                    parts[5] = str(float(parts[5]) + float(parts[3]))
                    parts[3] = '0'
                    
                if float(parts[2]) + float(parts[4]) > 1920:
                    parts[4] = str(1920 - float(parts[2]))
                    
                if float(parts[3]) + float(parts[5]) > 1080:
                    parts[5] = str(1080 - float(parts[3]))
                    
                
                # 조정된 Frame number와 Identity number로 줄을 재구성
                adjusted_line = f"{adjusted_frame_number},{','.join(parts[1:])}\n"
                
                output_file.write(adjusted_line)