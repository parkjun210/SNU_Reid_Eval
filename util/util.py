import motmetrics as mm
import cv2
import os
from tqdm import tqdm

def write_results(filename, results):
    save_format = '{frame},{id},{x1},{y1},{w},{h},{s},-1,-1,-1\n'
    with open(filename, 'a') as f:
        for frame_id, tlwhs, track_ids, scores in results:
            for tlwh, track_id, score in zip(tlwhs, track_ids, scores):
                if track_id < 0:
                    continue
                x1, y1, w, h = tlwh
                line = save_format.format(frame=frame_id, id=track_id, x1=round(x1, 1), y1=round(y1, 1), w=round(w, 1), h=round(h, 1), s=round(score, 2))
                f.write(line)
    
    
    
def do_moteval(gt_path, tg_path):
    
    mm.lap.default_solver = 'lap'
    mh = mm.metrics.create()    

    gt = mm.io.loadtxt(gt_path, fmt='mot16', min_confidence=1)
    tg = mm.io.loadtxt(tg_path, fmt='mot16', min_confidence=-1)

    accs = []
    accs.append(mm.utils.compare_to_groundtruth(gt, tg, 'iou', distth=0.5))


    metrics = ['recall', 'precision', 'num_unique_objects', 'mostly_tracked',
                'partially_tracked', 'mostly_lost', 'num_false_positives', 'num_misses',
                'num_switches', 'num_fragmentations', 'mota', 'motp', 'num_objects']
    summary = mh.compute_many(accs, metrics=metrics, generate_overall=True)

    div_dict = {
        'num_objects': ['num_false_positives', 'num_misses', 'num_switches', 'num_fragmentations'],
        'num_unique_objects': ['mostly_tracked', 'partially_tracked', 'mostly_lost']}
    for divisor in div_dict:
        for divided in div_dict[divisor]:
            summary[divided] = (summary[divided] / summary[divisor])
    fmt = mh.formatters
    change_fmt_list = ['num_false_positives', 'num_misses', 'num_switches', 'num_fragmentations', 'mostly_tracked',
                        'partially_tracked', 'mostly_lost']
    for k in change_fmt_list:
        fmt[k] = fmt['mota']
    print(mm.io.render_summary(summary, formatters=fmt, namemap=mm.io.motchallenge_metric_names))

def save_pred(path, det, pred_class, result_txt_path):
    results = []
    frame_id = int(path.split('/')[-1].split('.')[0])
    feat = det.cpu().numpy()
    online_tlwhs = feat[:, :4]
    online_tlwhs[:, 2] = online_tlwhs[:, 2] - online_tlwhs[:, 0]
    online_tlwhs[:, 3] = online_tlwhs[:, 3] - online_tlwhs[:, 1]
    online_ids = pred_class
    online_scores = feat[:, 4]
    
    results.append((frame_id, online_tlwhs, online_ids, online_scores))
    write_results(result_txt_path, results)

def make_video(args):

    # Folder containing the images
    image_folder = os.path.join(args.output_dir, args.reid_save_dir)
    video_name = 'result_video_withGT.mp4' if args.use_GT_IDs else 'result_video.mp4'

    if os.path.exists(os.path.join(args.output_dir, video_name)):
        os.remove(os.path.join(args.output_dir, video_name))
    
    # Get the list of image files in the specified folder and sort them
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort(key=lambda x: int(x.split('.')[0]))  # Sort by number

    # Determine the width and height from the first image
    image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(image_path)
    height, width, layers = frame.shape

    # Video settings
    video = cv2.VideoWriter(os.path.join(args.output_dir, video_name), cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    # Append each image to the video
    print('make video using result images!')
    for image in tqdm(images):
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # Release the video writer
    cv2.destroyAllWindows()
    video.release()