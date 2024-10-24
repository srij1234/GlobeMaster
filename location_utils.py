import math
import numpy as np
import geocoder
from OpenGL.GL import *

def get_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]
    else:
        print("Could not fetch location. Using default coordinates (0, 0).")
        return 0, 0

def latlong_to_cartesian(lat, lon):
    lon_radians = math.radians(lat)
    lat_radians = math.radians(lon - 90)

    x = math.cos(lat_radians) * math.cos(lon_radians)
    y = math.sin(lat_radians)
    z = math.cos(lat_radians) * math.sin(lon_radians)

    return np.array([x, y, z])

def draw_location_dot(lat, lon):
    pos = latlong_to_cartesian(lat, lon)
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glColor3f(1, 0, 0)

    glBegin(GL_QUADS)
    size = 0.02
    # Front face
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    # Back face
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(-size, size, -size)
    # Left face
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, size, -size)
    # Right face
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)
    # Top face
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    # Bottom face
    glVertex3f(-size, -size, -size)
    glVertex3f(size, -size, -size)
    glVertex3f(size, -size, size)
    glVertex3f(-size, -size, size)
    
    glEnd()
    glPopMatrix()
