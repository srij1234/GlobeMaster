from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def init_opengl():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

def draw_sphere(sphere_res):
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    glColor3f(1, 1, 1)
    gluSphere(quad, 1, sphere_res, sphere_res)

def apply_rotation_matrix(matrix):
    rotation = np.identity(4)
    rotation[:3, :3] = matrix
    glMultMatrixf(rotation.T)
