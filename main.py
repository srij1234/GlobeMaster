import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from texture_loader import load_texture
from opengl_utils import init_opengl, draw_sphere, apply_rotation_matrix
from math_utils import create_rotation_matrix_x, create_rotation_matrix_y
from location_utils import get_location, draw_location_dot

# Window setup
WIDTH, HEIGHT = 800, 600
texture_path = "C:/Users/Dell/Desktop/world_map_texture.jpg"
SPHERE_RES = 50
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Textured Rotating Globe')

    global camera_distance, mouse_dragging, prev_mouse_x, prev_mouse_y
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
    glTranslatef(0.0, 0.0, camera_distance)

    load_texture(texture_path)
    init_opengl()

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
        gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
        glTranslatef(0.0, 0.0, camera_distance)

        glPushMatrix()
        apply_rotation_matrix(rotation_matrix)
        draw_sphere(SPHERE_RES)
        draw_location_dot(latitude, longitude)
        glPopMatrix()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
