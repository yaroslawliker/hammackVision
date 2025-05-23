import numpy as np
from scipy.spatial.transform import Rotation

cam_matrix = [
        [1.6e+03, 0, 9.6e+02],
        [0, 1.6e+03, 5.4e+02],
        [0, 0, 1.0]
    ]

cam_pos = np.array([0, 200, 0])

point_homogen = [834, 635, 1]

rotation_bad = Rotation.from_euler('x', 15, degrees=True).as_matrix()

rotation_good = np.array([
        [1,  0,  0],
        [0.0000000,  0.9659258, -0.2588190],
        [0.0000000,  0.2588190,  0.9659258]
    ])

rotation = rotation_bad

vector_cam = np.linalg.inv(cam_matrix) @ point_homogen
vector_world = rotation.T @ vector_cam

t0 = -cam_pos[1] / vector_world[1]

op1 = t0 * vector_world
print("op1", op1)
op2 = cam_pos + op1
print("cam_pos", op2)

point_3D = cam_pos + t0 * vector_world

print("3D point in world coordinates:", point_3D)

"""
rotation:
array([[ 1.        ,  0.        ,  0.        ],
       [ 0.        ,  0.96592583, -0.25881905],
       [ 0.        ,  0.25881905,  0.96592583]])

array([[ 1.       ,  0.       ,  0.       ],
       [ 0.       ,  0.9659258, -0.258819 ],
       [ 0.       ,  0.258819 ,  0.9659258]])


# Cam
array([-0.07875 ,  0.059375,  1.      ])

array([-0.07875 ,  0.059375,  1.      ])

# World
array([-0.07875   ,  0.31617089,  0.95055845])

array([-0.07875   ,  0.31617084,  0.95055842])

# t0
-632.5693024526022

-632.5693958130638

# Result
array([ 4.98148326e+01,  2.84217094e-14, -6.01294093e+02])

array([  49.81483992,    0.        , -601.29416661])

------------------------------------------



"""




