import math
import numpy as np
import geocoder
from OpenGL.GL import *
from OpenGL.GLU import *

def get_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]
    else:
        print("Could not fetch location. Using default coordinates (0, 0).")
        return 0, 0

def latlong_to_cartesian(lat, lon):
    lat_radians = math.radians(lat)
    lon_radians = math.radians(lon)
    x = math.cos(lat_radians) * math.cos(lon_radians)
    y = math.cos(lat_radians) * math.sin(lon_radians)
    z = math.sin(lat_radians)
    return np.array([x, y, z])

def draw_location_dot(lat, lon):
    pos = latlong_to_cartesian(lat, lon)
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glColor3f(1, 0, 0)
    
    quadric = gluNewQuadric()
    gluSphere(quadric, 0.02, 10, 10)  # Draw a small sphere as the location marker
    gluDeleteQuadric(quadric)
    
    glPopMatrix()
    glColor3f(1, 1, 1)  # Reset color to white
