import json
import numpy as np

import back_project_facade

def calculate_error(estimated, actual):

    error_abs = [actual[i] - estimated[i] for i in range(3)]

    error_rel = []
    for i in range(3): 
        if estimated[i] == 0: 
            error_rel.append(0) 
        else: 
            error_rel.append(error_abs[i] / estimated[i])

    return error_abs, error_rel

def print_3Dpoint(point, num, digits_after_dot=2):
    print(f"\tPoint {num}:", end=" ")
    for i in range(3):
        print(round(point[i], digits_after_dot), end=" ")
    print()

def print_errors(estimated, actual, num):
    error_abs, error_rel = calculate_error(estimated, actual)

    error_abs = [round(error_abs[i], 2) for i in range(3)]
    error_rel_percent = [round(abs(error_rel[i] * 100), 1) for i in range(3)]
    error_rel_str = [str(error_rel_percent[i]) + "%" for i in range(3)]

    print(f"\t\tActual: {actual}")
    print(f"\t\tAbsolute: {error_abs}")
    print(f"\t\tRelative: {error_rel_str}")

def calculate_3Dpoints(data: list, camera_names: list = None):

    result = []

    for session in data:
        if camera_names is None or (session["name"] in camera_names):
            camera = session["camera"]
            points = session["points"]
            points_pixels = [point["pixels"] for point in points]

            # Intrisic parameters format
            if "fx" in camera:
                fx = camera["fx"]
                fy = camera["fy"] if "fy" in camera else fx

                u = camera["u"] if "u" in camera else camera["photoSize"][0] / 2
                v = camera["v"] if "v" in camera else camera["photoSize"][1] / 2
            
            # Pixel size and focal length format
            elif "pixelSize" in camera and "focalLength" in camera:
                fx = camera["focalLength"] / camera["pixelSize"]
                fy = fx

            # Horizontal sensor size and photo size format
            elif "horizontalSensorSize" in camera and "focalLength" in camera:
                pixel_size = camera["horizontalSensorSize"] / camera["photoSize"][0]
                fx = camera["focalLength"] / pixel_size
                fy = fx

            else:
                raise ValueError("Object must contain at least one of this param groups: (fx,u,v, maybe fy) or (pixelSize, focalLength) or horisontalSensorSize")
            
            points_3D = back_project_facade.back_project_points(
                    np.array(camera["photoSize"]),
                    fx,
                    fy,
                    camera["y"],
                    np.array(camera["eulerRotationAngles"]),
                    np.array(points_pixels)
                )
            
            points_actual = []
            for point in points:
                try:
                    points_actual.append(point["real"])
                except KeyError:
                    points_actual.append(None)

            result.append([points_3D, points_actual, session["name"]])

    return result

def show_results(points_3D, points_actual, session_name, comparing=False):
    print("--- Session: " + session_name)

    i = 0
    for point_actual, point_estimated in zip(points_actual, points_3D):
        print_3Dpoint(point_estimated, i)
        if comparing and point_actual is not None:
            print_errors(point_estimated, point_actual, i)
        i += 1

def extract_json_data(json_path):
    with open(json_path, "rt") as file:
        parsed = json.load(file)
    
    return parsed

def run_calculation_on_path(json_path, session_names=None, comparing=True):
    parsed = extract_json_data(json_path)
    
    res = calculate_3Dpoints(parsed, session_names)
    for points_3D, points_actual, session_name in res:
        show_results(points_3D, points_actual, session_name, comparing=True)

if __name__ == "__main__":

    # run_calculation_on_path(
    #     "data/test/back projection/virtual/3cubes.json",
    #     ["straight","15degree"]
    # )

    # run_calculation_on_path(
    #     "data/test/back projection/real/noinfo.json",
    #     ["random city photo"]
    # )

    run_calculation_on_path(
        "data/test/back projection/real/room.json",
        ["fridge"]
    )



    # run_calculation_on_path(
    #     "data/test/back projection/real/cola.json"
    # )

    