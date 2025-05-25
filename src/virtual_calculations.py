import numpy as np
from scipy.spatial.transform import Rotation

import back_projection as bp

def back_project_virtual(
        photo_size: np.ndarray, 
        horisontal_camera_size,
        f,
        camera_y,
        camera_euler_rotation_agles: np.ndarray,
        points_pixels: np.ndarray
    ) -> np.array:

    assert len(photo_size) == 2, "photo_size must be a 2D array"
    assert len(camera_euler_rotation_agles) == 3, "camera_euler_rotation_agles must be a 3D array"
    assert points_pixels.shape[0] > 0 and points_pixels.shape[1] == 2, "points_pixels must be an array of 3D arrays, N > 0"
    
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
    
    photo = bp.Photo(photo_width, photo_height)

    points_3D = []

    # Create a photo settings
    for i, point in enumerate(points_pixels):
        # Create the photo point
        photo_point = bp.PhotoPoint(point[0], point[1], photo)
        point_3D = projector.back_project(photo_point)
        points_3D.append(point_3D)

    return np.array(points_3D)

def print_3D_points(points_3D):
    print("3D point coordinates (cm):")
    for i, point in enumerate(points_3D):
        print(f"\tPoint {i}:", end=" ")
        for j in range(3):
            print(f"{point[j]:.4f}", end=" ")
        print()

if __name__ == "__main__":

    pass