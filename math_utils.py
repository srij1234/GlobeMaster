import numpy as np

def create_rotation_matrix_x(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([
        [1,  0,  0],
        [0,  c, -s],
        [0,  s,  c]
    ], dtype=np.float32)

def create_rotation_matrix_y(angle):
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array([
        [ c, 0,  s],
        [ 0, 1,  0],
        [-s, 0,  c]
    ], dtype=np.float32)
