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

def guess_angle(json_path, 
                alpha_start, alpha_stop, alpha_step, 
                y_start, y_stop, y_step, 
                sample_cost_function = None, batch_cost_function = None,
                use_points=None,
                print_every_new=False):

    if sample_cost_function is None:
        sample_cost_function = lambda x, y: (abs(x) + abs(y)) / 2

    if batch_cost_function is None:
        batch_cost_function = lambda errors: sum(errors) / len(errors)


    parsed = extract_json_data(
        json_path,
    )

    min_err_abs = float("inf")
    min_i = 0
    min_y = 0

    angles = [alpha_start + alpha_step*i for i in range( int((alpha_stop - alpha_start) / alpha_step) + 1)]
    for i in angles:
        parsed[0]["camera"]["eulerRotationAngles"][0] = i

        ys = [y_start + y_step*i for i in range( int((y_stop - y_start) / y_step) + 1)]
        for y in ys:
            parsed[0]["camera"]["y"] = y

            points_3D, points_actual, _  = calculate_3Dpoints(parsed)[0]

            if use_points is not None:
                points_3D = [points_3D[j] for j in use_points]
                points_actual = [points_actual[j] for j in use_points]

            errors_abs = [calculate_error(points_3D[j], points_actual[j])[0] for j in range(len(points_3D))]

            errors = [sample_cost_function(error[0], error[2]) for error in errors_abs]

            error = batch_cost_function(errors)

            if error < min_err_abs:
                min_err_abs = error
                min_i = i
                min_y = y
                if print_every_new:
                    print(f"New min: {min_err_abs} for angle {min_i} and y {min_y}")
        
    print(f"Angle: {min_i}, Y: {min_y} Error: {min_err_abs}")


if __name__ == "__main__":

    # run_calculation_on_path(
    #     "data/test/back projection/virtual/3cubes.json",
    #     ["straight","15degree"]
    # )

    # run_calculation_on_path(
    #     "data/test/back projection/real/noinfo.json",
    #     ["random city photo"]
    # )

    # run_calculation_on_path(
    #     "data/test/back projection/real/room.json",
    #     ["fridge"]
    # )

    # run_calculation_on_path(
    #     "data/test/back projection/real/cola.json"
    # )
    
    # guess_angle("data/test/back projection/real/roomtop.json", -60, 60, 0.1, lambda x, y: (x**2 + y**2)**0.5, False)
    
    # print("Guessing angles...")

    # print("By X only")
    # guess_angle("data/test/back projection/real/roomtop.json",
    #              20, 60, 0.1,
    #              223, 227, 0.1,
    #              sample_cost_function=lambda x, y: (abs(x)),
    #              print_every_new=False)
    
    # print("By Y only")
    # guess_angle("data/test/back projection/real/roomtop.json",
    #              20, 60, 0.1,
    #              223, 227, 0.1,
    #              sample_cost_function=lambda x, y: (abs(y)),
    #              print_every_new=False)
    
    # print("By first point")
    # guess_angle("data/test/back projection/real/roomtop.json",
    #              20, 60, 0.1,
    #              223, 227, 0.1,
    #              use_points=[0],
    #              print_every_new=False)
    
    # print("By second point")
    # guess_angle("data/test/back projection/real/roomtop.json",
    #              20, 60, 0.1,
    #              223, 227, 0.1,
    #              use_points=[1],
    #              print_every_new=False)

    # print("Total")
    # guess_angle("data/test/back projection/real/roomtop.json",
    #              20, 60, 0.1,
    #              223, 227, 0.1,
    #              print_every_new=False)
    



    run_calculation_on_path("data/test/back projection/real/roomtop.json")


    