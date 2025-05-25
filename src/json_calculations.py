import json
import numpy as np

import virtual_calculations

def run_calculation(data: list, camera_names: list = None, comparing=False):

    for session in data:
        if session["name"] in camera_names or camera_names is None:
            camera = session["camera"]
            points = session["points"]
            points_pixels = [point["pixels"] for point in points]

            points_3D = virtual_calculations.back_project_virtual(
                np.array(camera["photoSize"]),
                camera["horizontalSensorSize"],
                camera["focalLength"],
                camera["y"],
                np.array(camera["eulerRotationAngles"]),
                np.array(points_pixels)
            )
            print("--- Session: " + session["name"])
            virtual_calculations.print_3D_points(points_3D)

            if (comparing == True):
                print("Errors:")
                points_actual = [point["real"] for point in points]
                i = 0
                for point_actual, point_estimated in zip(points_actual, points_3D):
                    error_abs = [point_actual[i] - point_estimated[i] for i in range(3)]
                    error_rel = [error_abs[i] / point_estimated[i] for i in (0,2)]
                    error_rel.insert(1, 0)

                    error_abs = [round(error_abs[i],2) for i in range(3)]

                    error_rel_percent = [round(abs(error_rel[i]*100), 1) for i in range(3)]
                    error_rel_str = [str(error_rel_percent[i])+"%" for i in range(3)]
                    
                    print(f"\tPoint {i}: abs: {error_abs}, rel: {error_rel_str}")

                    i+=1

if __name__ == "__main__":
    json_path = "data/test/back projection/virtual.json"
    session_names = ["15degree"]

    with open(json_path, "rt") as file:
        parsed = json.load(file)
        
        run_calculation(parsed, session_names, True)