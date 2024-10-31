import numpy as np
import math
from OpenGL.GL import *
from OpenGL.arrays import vbo

def generate_sphere_vertices(latitude_steps, longitude_steps):
    vertices = []
    normals = []
    tex_coords = []
    for i in range(latitude_steps + 1):
        lat = np.pi * (-0.5 + float(i) / latitude_steps)
        sin_lat = math.sin(lat)
        cos_lat = math.cos(lat)
        for j in range(longitude_steps + 1):
            lon = 2 * np.pi * float(j) / longitude_steps
            sin_lon = math.sin(lon)
            cos_lon = math.cos(lon)
            x = cos_lat * cos_lon
            y = cos_lat * sin_lon
            z = sin_lat
            vertices.append((x, y, z))
            normals.append((x, y, z))  # Initial normals
            s = float(j) / longitude_steps
            t = float(i) / latitude_steps
            tex_coords.append((s, t))
    return vertices, normals, tex_coords

def generate_sphere_indices(latitude_steps, longitude_steps):
    indices = []
    for i in range(latitude_steps):
        for j in range(longitude_steps):
            first = (i * (longitude_steps + 1)) + j
            second = first + longitude_steps + 1
            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])
    return indices

def map_elevation_to_vertices(vertices, tex_coords, elevation_data):
    if elevation_data is None:
        print("Elevation data not available. Using default sphere.")
        normals = [(x, y, z) for (x, y, z) in vertices]
        return vertices, normals

    elevation_rows, elevation_cols = elevation_data.shape

    # Normalize elevation data
    elevation_min = np.nanmin(elevation_data)
    elevation_max = np.nanmax(elevation_data)
    elevation_range = elevation_max - elevation_min
    if elevation_range == 0:
        elevation_range = 1  # Prevent division by zero
    elevation_data = (elevation_data - elevation_min) / elevation_range

    new_vertices = []
    new_normals = []
    for idx, ((x, y, z), (s, t)) in enumerate(zip(vertices, tex_coords)):
        col = int(s * (elevation_cols - 1))
        row = int((1 - t) * (elevation_rows - 1))  # Flip t
        elevation = elevation_data[row, col]
        if np.isnan(elevation):
            elevation = 0  # Handle no-data values

        # Adjust the radius based on elevation
        SCALE_FACTOR = 0.1  # Adjust to control relief exaggeration
        radius = 1 + (elevation * SCALE_FACTOR)
        new_x = x * radius
        new_y = y * radius
        new_z = z * radius
        new_vertices.append((new_x, new_y, new_z))

        # Recompute normal
        normal = np.array([new_x, new_y, new_z])
        normal /= np.linalg.norm(normal)
        new_normals.append(normal.tolist())

    return new_vertices, new_normals

def create_vbo(vertices, normals, tex_coords, indices):
    vertex_data = np.array(vertices, dtype=np.float32)
    normal_data = np.array(normals, dtype=np.float32)
    tex_coord_data = np.array(tex_coords, dtype=np.float32)
    index_data = np.array(indices, dtype=np.uint32)

    vertex_vbo = vbo.VBO(vertex_data)
    normal_vbo = vbo.VBO(normal_data)
    tex_coord_vbo = vbo.VBO(tex_coord_data)
    index_vbo = vbo.VBO(index_data, target=GL_ELEMENT_ARRAY_BUFFER)

    return vertex_vbo, normal_vbo, tex_coord_vbo, index_vbo

def draw_vbo(vertex_vbo, normal_vbo, tex_coord_vbo, index_vbo, num_indices):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    vertex_vbo.bind()
    glVertexPointer(3, GL_FLOAT, 0, vertex_vbo)
    normal_vbo.bind()
    glNormalPointer(GL_FLOAT, 0, normal_vbo)
    tex_coord_vbo.bind()
    glTexCoordPointer(2, GL_FLOAT, 0, tex_coord_vbo)
    index_vbo.bind()

    glDrawElements(GL_TRIANGLES, num_indices, GL_UNSIGNED_INT, index_vbo)

    index_vbo.unbind()
    tex_coord_vbo.unbind()
    normal_vbo.unbind()
    vertex_vbo.unbind()
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
