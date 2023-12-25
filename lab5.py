#!/usr/bin/env python3
import sys
import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]
color_value = 0.0
theta = 0.0
phi = 0.0
R = 10
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0
camera_mode = False

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]


light_ambient2 = [color_value, 0.1, 0.3, 1.0]  # Soft blue
light_diffuse2 = [0.2, 0.2, 0.8, 1.0]  # Brighter blue
light_specular2 = [1.0, 1.0, 1.0, 1.0]  # Wh
light_position2 = [-10.0, 10.0, 5.0, 1.0]   # Position remains the same

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)


    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient2)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse2)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular2)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position2)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global R

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    theta += delta_x * pix2angle
    phi += delta_y * pix2angle

    if left_mouse_button_pressed:
        if camera_mode:
            theta += delta_x * pix2angle
            phi += delta_y * pix2angle

            # Konwersja kątów na radiany
            theta_rad = math.radians(theta)
            phi_rad = math.radians(phi)

            # Obliczenie nowej pozycji światła
            light_position[0] = R * math.sin(phi_rad) * math.cos(theta_rad)
            light_position[1] = R * math.sin(phi_rad) * math.sin(theta_rad)
            light_position[2] = R * math.cos(phi_rad)

            # Aktualizacja pozycji światła
            glLightfv(GL_LIGHT0, GL_POSITION, light_position)

            # Wizualizacja nowej pozycji światła
            render_light_sphere(light_position)
    else:
        light_ambient2 = [color_value, 0.1, 0.3, 1.0]
        light_diffuse2 = [0.2, color_value, 0.8, 1.0]  # Adjusted for visibility
        glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient2)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse2)
        glRotatef(theta, 0.0, 1.0, 0.0)


    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()


def render_light_sphere(light_pos):
    glPushMatrix()
    glTranslatef(light_pos[0], light_pos[1], light_pos[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 0.1, 10, 10)  # Mała sfera wizualizująca pozycję światła
    gluDeleteQuadric(quadric)
    glPopMatrix()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global camera_mode
    global color_value
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    elif key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        camera_mode = not camera_mode  # Przełączamy tryb pracy
        print("Camera mode status: " + str(camera_mode))
    elif key == GLFW_KEY_W and action == GLFW_PRESS:
        color_value = min(color_value + 0.1, 1.0)  # Ensure color_value doesn't go above 1.0
        print("Increased color_value:", color_value)
    elif key == GLFW_KEY_S and action == GLFW_PRESS:
        color_value = max(color_value - 0.1, 0.0)  # Ensure color_value doesn't go below 0.0
        print("Decreased color_value:", color_value)

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global mouse_y_pos_old
    global delta_y
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos
    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos



def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()