""" Just few experiments with rotating a line """


import arcade
import math

def mult_matrix_vector(m, v):
    n = len(v)
    result = [0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i] += m[i][j] * v[j]
    return result

def rotate_on_fi(point, fi):
    """Rotates point on fi angle, given in degrees around the coordinates (0,0)"""
    fi = math.radians(fi)
    matrix = [
        [math.cos(fi), -math.sin(fi)],
        [math.sin(fi), math.cos(fi)]
    ]
    return mult_matrix_vector(matrix, point)

def rotate_on_fi_around_pivot(point, fi, pivot):
    """Rotates a point on fi angle (given in degrees) round the pivot"""
    new_point = point.copy()
    new_point[0] -= pivot[0]
    new_point[1] -= pivot[1]

    new_point = rotate_on_fi(new_point, fi)

    new_point[0] += pivot[0]
    new_point[1] += pivot[1]

    return new_point
        
# Setting up drawing
arcade.open_window(600, 600, "Drawing Primitives Example", resizable=True)
arcade.set_background_color(arcade.color.WHITE)
arcade.start_render()

# Defining dots
point1 = [100, 100]
point2 = [200, 300]

# Drawing simple line
arcade.draw_line(point1[0], point1[1], point2[0], point2[1], arcade.color.RED, 3)

# Rotating
fi_degrees = 30
pivot = point1
rotated_point1 = rotate_on_fi_around_pivot(point1, fi_degrees, pivot)
rotated_point2 = rotate_on_fi_around_pivot(point2, fi_degrees, pivot)

# Drawing second line
arcade.draw_line(rotated_point1[0], rotated_point1[1], rotated_point2[0], rotated_point2[1], arcade.color.GREEN, 3)

arcade.finish_render()
arcade.run()
