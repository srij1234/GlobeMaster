from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def init_opengl():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)  # Normalize normals for lighting

def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = [0.0, 0.0, 2.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def apply_rotation_matrix(matrix):
    rotation = np.identity(4, dtype=np.float32)
    rotation[:3, :3] = matrix
    glMultMatrixf(rotation.T)
