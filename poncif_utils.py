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

def remove_path_too_close(a, b, dist=10):
    """
    Remove paths from a that are too close to b (less than dist)
    """
    if a and b:
        for a_path in a["objects"]:
            for b_path in b["objects"]:
                if b_path["stroke"] == "#ffff00":
                    for i in range(len(a_path["path"])):
                        for j in range(len(b_path["path"])):
                            if ((a_path["path"][i][-2] - b_path["path"][j][-2])**2 + (a_path["path"][i][-1] - b_path["path"][j][-1])**2) < dist **2:
                                a_path["path"][i] = ['M', a_path["path"][i][-2], a_path["path"][i][-1]]
                else:
                    continue
        return(a)
    else:
        return(None)

if __name__=="__main__":
    a = {'version': '4.4.0', 'objects': [{'type': 'path', 'version': '4.4.0', 'originX': 'left', 'originY': 'top', 'left': 176.5, 'top': 83.5, 'width': 202.01, 'height': 17, 'fill': None, 'stroke': '#000000', 'strokeWidth': 3, 'strokeDashArray': None, 'strokeLineCap': 'round', 'strokeDashOffset': 0, 'strokeLineJoin': 'round', 'strokeUniform': False, 'strokeMiterLimit': 10, 'scaleX': 1, 'scaleY': 1, 'angle': 0, 'flipX': False, 'flipY': False, 'opacity': 1, 'shadow': None, 'visible': True, 'backgroundColor': '', 'fillRule': 'nonzero', 'paintFirst': 'fill', 'globalCompositeOperation': 'source-over', 'skewX': 0, 'skewY': 0, 'path': [['M', 177.997, 84.997], ['Q', 178, 85, 180, 86], ['Q', 182, 87, 192.5, 89.5], ['Q', 203, 92, 214, 93.5], ['Q', 225, 95, 232.5, 96], ['Q', 240, 97, 253.5, 97.5], ['Q', 267, 98, 289.5, 99], ['Q', 312, 100, 316, 100], ['Q', 320, 100, 327, 100.5], ['Q', 334, 101, 343, 101], ['Q', 352, 101, 360.5, 101.5], ['Q', 369, 102, 371, 102], ['Q', 373, 102, 374.5, 102], ['Q', 376, 102, 377, 102], ['Q', 378, 102, 379, 102], ['L', 380.003, 102]]}], 'background': ''}  
    b = {'version': '4.4.0', 'objects': [{'type': 'path', 'version': '4.4.0', 'originX': 'left', 'originY': 'top', 'left': 268.5, 'top': 89.5, 'width': 47.01, 'height': 5, 'fill': None, 'stroke': '#000000', 'strokeWidth': 3, 'strokeDashArray': None, 'strokeLineCap': 'round', 'strokeDashOffset': 0, 'strokeLineJoin': 'round', 'strokeUniform': False, 'strokeMiterLimit': 10, 'scaleX': 1, 'scaleY': 1, 'angle': 0, 'flipX': False, 'flipY': False, 'opacity': 1, 'shadow': None, 'visible': True, 'backgroundColor': '', 'fillRule': 'nonzero', 'paintFirst': 'fill', 'globalCompositeOperation': 'source-over', 'skewX': 0, 'skewY': 0, 'path': [['M', 269.997, 91], ['Q', 270, 91, 270.5, 91], ['Q', 271, 91, 271.5, 91], ['Q', 272, 91, 272.5, 91], ['Q', 273, 91, 273.5, 91], ['Q', 274, 91, 274.5, 91], ['Q', 275, 91, 275.5, 91], ['Q', 276, 91, 276.5, 91], ['Q', 277, 91, 277.5, 91], ['Q', 278, 91, 279, 91], ['Q', 280, 91, 280.5, 91], ['Q', 281, 91, 281.5, 91], ['Q', 282, 91, 282.5, 91], ['Q', 283, 91, 283.5, 91], ['Q', 284, 91, 284.5, 91], ['Q', 285, 91, 285.5, 91], ['Q', 286, 91, 286.5, 91], ['Q', 287, 91, 287.5, 91], ['Q', 288, 91, 288.5, 91], ['Q', 289, 91, 289.5, 91], ['Q', 290, 91, 290.5, 91], ['Q', 291, 91, 291.5, 91], ['Q', 292, 91, 292.5, 91], ['Q', 293, 91, 293.5, 91], ['Q', 294, 91, 294.5, 91], ['Q', 295, 91, 295.5, 91], ['Q', 296, 91, 296.5, 91], ['Q', 297, 91, 297.5, 91], ['Q', 298, 91, 298.5, 91.5], ['Q', 299, 92, 299.5, 92], ['Q', 300, 92, 300.5, 92], ['Q', 301, 92, 301.5, 92], ['Q', 302, 92, 303, 92.5], ['Q', 304, 93, 304, 93.5], ['Q', 304, 94, 304.5, 94], ['Q', 305, 94, 305.5, 94], ['Q', 306, 94, 306.5, 94], ['Q', 307, 94, 307.5, 94], ['Q', 308, 94, 308.5, 94], ['Q', 309, 94, 309.5, 94.5], ['Q', 310, 95, 310.5, 95], ['Q', 311, 95, 311.5, 95], ['Q', 312, 95, 312.5, 95], ['Q', 313, 95, 313.5, 95], ['Q', 314, 95, 315, 95.5], ['Q', 316, 96, 316.5, 96], ['L', 317.003, 96]]}
], 'background': ''} 
    print(remove_path_too_close(a, b))