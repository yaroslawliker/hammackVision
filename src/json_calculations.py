import json
import numpy as np

import back_project_facade

def run_calculation(data: list, camera_names: list = None, comparing=False):

    for session in data:
        if camera_names is None or (session["name"] in camera_names):
            camera = session["camera"]
            points = session["points"]
            points_pixels = [point["pixels"] for point in points]

            # Intrisic parameters format
            if "fx" in camera and "u" in camera and "v" in camera:
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

            print("--- Session: " + session["name"])
            back_project_facade.print_3D_points(points_3D)

            if (comparing == True):
                print("Errors:")
                points_actual = []
                for point in points:
                    try:
                        points_actual.append(point["real"])
                    except KeyError:
                        points_actual.append(None)                    

                i = 0
                for point_actual, point_estimated in zip(points_actual, points_3D):
                    if (point_actual is None):
                        print(f"\tPoint {i}: no real calculation")
                        continue

                    error_abs = [point_actual[i] - point_estimated[i] for i in range(3)]
                    error_rel = [error_abs[i] / point_estimated[i] for i in (0,2)]
                    error_rel.insert(1, 0)

                    error_abs = [round(error_abs[i],2) for i in range(3)]

                    error_rel_percent = [round(abs(error_rel[i]*100), 1) for i in range(3)]
                    error_rel_str = [str(error_rel_percent[i])+"%" for i in range(3)]
                    
                    print(f"\tPoint {i}: abs: {error_abs}, rel: {error_rel_str}")

                    i+=1

def run_calculation_on_path(json_path, session_names = None):
    with open(json_path, "rt") as file:
        parsed = json.load(file)
        run_calculation(parsed, session_names, True)

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
    #     ["table", "fridge"]
    # )

    run_calculation_on_path(
        "data/test/back projection/real/cola.json"
    )

    