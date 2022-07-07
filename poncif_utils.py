import cv2
import numpy as np
from svgpathtools import parse_path

def get_contours(image, low_threshold=300, high_threshold=400):
    print(f"Computing contour with {low_threshold = } and {high_threshold = }")
    img_array = np.array(image)
    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    canny = cv2.Canny(img, low_threshold, high_threshold, edges=True, L2gradient=True)
    contours, _ = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    return(contours)

def get_contours_dict(image, low_threshold = 300, high_threshold = 400, scale=1, sampling=1):
    contours = get_contours(image, low_threshold, high_threshold)
    contours_dict = {i:[(contours[i][j][0]*scale).tolist() for j in range(0, len(contours[i]), sampling)] for i in range(len(contours))}
    return(contours_dict)

def contours2json(contours, stroke_width=3, stroke_color="#000000"):
    json_data = {'version': '4.4.0', 'objects': [], 'background': '#eee'}
    path_info = {'type': 'path', 'version': '4.4.0', 'originX': 'left', 'originY': 'top', 'fill': None, 'stroke': stroke_color, 'strokeWidth': stroke_width, 'strokeDashArray': None, 'strokeLineCap': 'round', 'strokeDashOffset': 0, 'strokeLineJoin': 'round', 'strokeUniform': False, 'strokeMiterLimit': 10, 'scaleX': 1, 'scaleY': 1, 'angle': 0, 'flipX': False, 'flipY': False, 'opacity': 1, 'shadow': None, 'visible': True, 'backgroundColor': '', 'fillRule': 'nonzero', 'paintFirst': 'fill', 'globalCompositeOperation': 'source-over', 'skewX': 0, 'skewY': 0}
    path_list = []
    for contour in contours.values():
        if not contour == []:
            path = [['M'] + contour[0]]
            for i, point in enumerate(contour[1:]):
                origine = contour[i]
                path.append(['L', *origine, *point])
        path_list.append(path)
    for path in path_list:
        path_complete = path_info.copy()
        path_complete["path"] = path
        json_data["objects"].append(path_complete)
    return(json_data)

def get_target_size(size, container_size):
    ratio = min(container_size[0]/size[0], container_size[1]/size[1])
    target_size = [int(size[0] * ratio), int(size[1] * ratio)]
    print(f"converted {size} to {target_size}")
    return(target_size)

def add_path_no_duplicate(a, b):
    """
    add b to a with no duplicates
    """
    if a and b:
        existing_pth = [i["path"] for i in a["objects"]]
        for obj in b["objects"]:
            if obj["path"] not in existing_pth:
                a["objects"].append(obj)
                existing_pth.append(obj["path"])
        return(a)
    else:
        return(None)

if __name__=="__main__":
    a = {"objects":[{"path": [1, 2]}, {"path": [2, 3]}, {"path": [3, 4]}]}    
    b = {"objects":[{"path": [2, 2]}, {"path": [3, 3]}, {"path": [3, 4]}]}
    print(add_path_no_duplicate(a, b))