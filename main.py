import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from texture_utils import load_texture
from opengl_utils import init_opengl, apply_rotation_matrix, init_lighting
from math_utils import create_rotation_matrix_x, create_rotation_matrix_y
from location_utils import get_location, draw_location_dot
from sphere_geometry import (
    generate_sphere_vertices,
    generate_sphere_indices,
    map_elevation_to_vertices,
    create_vbo,
    draw_vbo,
)
from elevation_utils import load_elevation_data

# Window setup
WIDTH, HEIGHT = 800, 600
texture_path = r"C:\Users\Dell\Desktop\zaza.png"  # Update with your actual texture image file
elevation_tiff_path = r"C:\Users\Dell\Desktop\Resized.tif"
SPHERE_RES = 500  # Adjust for performance; higher values increase detail
camera_distance = -5  # Start at distance -5 from the globe

MIN_ZOOM = -2  # Prevent zooming in too much
MAX_ZOOM = -20  # Prevent zooming out too much

latitude, longitude = get_location()  # Get user's latitude and longitude

mouse_dragging = False
prev_mouse_x, prev_mouse_y = 0, 0
MOUSE_ROT_SPEED = 0.005
rotation_matrix = np.identity(3)

def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('3D Relief Globe with Elevation Data')

    global camera_distance, mouse_dragging, prev_mouse_x, prev_mouse_y
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, camera_distance)
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Light blue background

    load_texture(texture_path)
    init_opengl()
    init_lighting()

    # Load elevation data
    elevation_data = load_elevation_data(elevation_tiff_path)

    # Generate sphere geometry
    vertices, normals, tex_coords = generate_sphere_vertices(SPHERE_RES, SPHERE_RES)
    indices = generate_sphere_indices(SPHERE_RES, SPHERE_RES)

    # Map elevation to vertices and compute normals
    vertices, normals = map_elevation_to_vertices(vertices, tex_coords, elevation_data)

    # Create VBOs
    vertex_vbo, normal_vbo, tex_coord_vbo, index_vbo = create_vbo(vertices, normals, tex_coords, indices)
    num_indices = len(indices)

    global rotation_matrix
    clock = pygame.time.Clock()
    ROT_SPEED = 0.05
    ZOOM_SPEED = 0.2

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_dragging = True
                    prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up
                    camera_distance += ZOOM_SPEED
                elif event.button == 5:  # Scroll down
                    camera_distance -= ZOOM_SPEED
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    mouse_dragging = False
            if event.type == pygame.MOUSEMOTION and mouse_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = -mouse_x + prev_mouse_x
                dy = -mouse_y + prev_mouse_y
                prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
                rotation_y = create_rotation_matrix_y(-dx * MOUSE_ROT_SPEED)
                rotation_matrix = np.dot(rotation_y, rotation_matrix)
                rotation_x = create_rotation_matrix_x(-dy * MOUSE_ROT_SPEED)
                rotation_matrix = np.dot(rotation_x, rotation_matrix)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rotation_y = create_rotation_matrix_y(ROT_SPEED)
            rotation_matrix = np.dot(rotation_y, rotation_matrix)
        if keys[pygame.K_RIGHT]:
            rotation_y = create_rotation_matrix_y(-ROT_SPEED)
            rotation_matrix = np.dot(rotation_y, rotation_matrix)
        if keys[pygame.K_UP]:
            rotation_x = create_rotation_matrix_x(ROT_SPEED)
            rotation_matrix = np.dot(rotation_x, rotation_matrix)
        if keys[pygame.K_DOWN]:
            rotation_x = create_rotation_matrix_x(-ROT_SPEED)
            rotation_matrix = np.dot(rotation_x, rotation_matrix)
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            camera_distance += ZOOM_SPEED
        if keys[pygame.K_MINUS]:
            camera_distance -= ZOOM_SPEED

        camera_distance = max(min(camera_distance, MIN_ZOOM), MAX_ZOOM)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(0, 0, -camera_distance, 0, 0, 0, 0, 1, 0)

        glPushMatrix()
        apply_rotation_matrix(rotation_matrix)

        glColor3f(1, 1, 1)  # Ensure color is white before drawing the globe

        # Draw the relief globe
        draw_vbo(vertex_vbo, normal_vbo, tex_coord_vbo, index_vbo, num_indices)

        # Draw the location marker
        draw_location_dot(latitude, longitude)

        glPopMatrix()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
