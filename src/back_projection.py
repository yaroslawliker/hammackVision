###
### This module implements the back projection algorithm for image reconstruction.
###

import numpy as np


class Camera:
    def __init__(self, fx, fy, skew=0):
        self.fx = fx
        self.fy = fy
        self.skew = skew
        
        self.position = np.zeros(3)
        self.orientation = np.eye(3)
    
    def set_position(self, position):
        self.position = np.array(position)
    def get_position(self):
        return self.position

    def self_orientation(self, orientation):
        self.orientation = np.array(orientation)
    def get_orientation(self):
        return self.orientation

    def get_internal_matrix(self, u, v) -> np.ndarray[3, 3]:
        K = np.array([
            [self.fx, self.skew, u],
            [0, self.fy, v],
            [0, 0, 1]
        ])

        return K

    
    
class BackProjection:
    def __init__(self, camera: Camera):
        self.camera = camera
    
    def get_direction_to_point_camera(self, point, u, v):
        # Convert point to homogeneous coordinates
        point_homogeneous = np.array([point[0], point[1], 1])
        
        # Get the camera intrinsic matrix
        K = self.camera.get_internal_matrix(u, v)
        
        # Compute the direction vector in camera coordinates
        direction_vector = np.linalg.inv(K) @ point_homogeneous
        
        return direction_vector
    
    def get_direction_to_point_world(self, point, u, v):
        # Get the direction vector in camera coordinates
        direction_camera = self.get_direction_to_point_camera(point, u, v)
        
        # Transform the direction vector to world coordinates
        direction_world = np.linalg.inv(self.camera.orientation) @ np.linalg.inv(self.camera.position) @ direction_camera
        
        return direction_world
    
    def back_project(self, point, u, v):
        # Get the direction vector in world coordinates
        direction_world = self.get_direction_to_point_world(point, u, v)
        
        t0 = -self.camera.position[1] / direction_world[1]

        point_3d = self.camera.position + t0 * direction_world
        
        return point_3d
    
if __name__ == "__main__":

    pass


    


