import cv2_process_image
from cv2_process_image import find_best_ratio
from os.path import isfile, join
import pandas as pd
import os
from PIL import Image
import imutils
import cv2

DIR = '../all_photos/'
#file = '20200323_150630.jpg'

files_names = [f for f in os.listdir(DIR) if isfile(join(DIR, f))]
files_names.sort()



def main(file_path):
    d = get_all_parameters_for_single_file(file_path)
    best_ratio = get_best_parameter_for_single_file(d)
    scanned = cv2_process_image.show_segment(file_path, ratio_parameter=best_ratio)
    #cv2.imshow("scanned", imutils.resize(scanned, height=650))
    #cv2.waitKey(0)
    img = Image.fromarray(scanned, "L")
    img.save(os.path.join('../output/', file), "JPEG")


def get_best_parameter_for_single_file(d):
    df = pd.DataFrame(d)
    for row in df.values:
        l = [float(a) if a != 'None' else 0 for a in row[1:]]
    m = pd.Series(l)
    idx = m.idxmax()
    best_ratio = (idx + 1) * 50
    return best_ratio


def single_parameter_experiment(file_path, ratio_parameter):
    try:
        contour_area = find_best_ratio(file_path, ratio_parameter=ratio_parameter)
        _results = {'file': file, ratio_parameter: str(contour_area)}
        return _results
    except Exception:
        _results = {'file': file, ratio_parameter: 'failed'}
        return _results


def get_all_parameters_for_single_file(file_path):
    d = []
    ratio_parameter = 50
    results = single_parameter_experiment(file_path=file_path, ratio_parameter=ratio_parameter)
    ratio_parameter += 50
    while ratio_parameter < 550:
        b = single_parameter_experiment(file_path=file_path, ratio_parameter=ratio_parameter)
        results[ratio_parameter] = b[ratio_parameter]
        ratio_parameter += 50
    d.append(results)
    return d


for file in files_names[:]:
    file_path = os.path.join(DIR, file)
    main(file_path)
