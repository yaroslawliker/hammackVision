import numpy as np
from scipy.spatial.transform import Rotation

import back_projection as bp

def back_project_virtual(
        photo_size: tuple, 
        horisontal_camera_size,
        f,
        camera_y,
        camera_euler_rotation_agles: tuple,
        point_pixels: tuple
    ) -> np.array:
    
    photo_width = photo_size[0]
    photo_height = photo_size[1]

    pixel_size_cm = horisontal_camera_size / photo_width

    f_per_pixel = f / pixel_size_cm

    camera_position = np.array([0, camera_y, 0])

    rotation = Rotation.from_euler('xyz', camera_euler_rotation_agles, degrees=True)
    camera_orientation = rotation.as_matrix()

    # Instantiate the camera
    camera = bp.Camera(f_per_pixel, f_per_pixel)
    camera.set_position(camera_position)
    camera.set_orientation(camera_orientation)

    # Instantiate the back projector
    projector = bp.BackProjector(camera)
    
    # Create a photo settings
    photo = bp.Photo(photo_width, photo_height)

    # Create the green point
    green_point = bp.PhotoPoint(669, 685, photo)

    point_3D = projector.back_project(green_point)
    return point_3D
    

def virtual_straight():
    point_3D = back_project_virtual(
        photo_size=(1920, 1080),
        horisontal_camera_size=36 / 100,
        f=30 / 100,
        camera_y=100,
        camera_euler_rotation_agles=(0, 0, 0),
        point_pixels=(669, 685)
    )
    print("3D point coordinates (cm):", point_3D)



if __name__ == "__main__":
    virtual_straight()



