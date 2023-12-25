#!/usr/bin/env python3
import sys

import numpy
import numpy as np
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *





def calculate_normals(vertices, N):
    normals = np.zeros(vertices.shape)

    # Loop through all the vertices except the edges
    for i in range(1, N-1):
        for j in range(1, N-1):
            # Take vectors to the surrounding vertices
            v0 = vertices[i, j]
            v1 = vertices[i-1, j] - v0
            v2 = vertices[i, j-1] - v0
            v3 = vertices[i+1, j] - v0
            v4 = vertices[i, j+1] - v0

            # Calculate the normals as the average cross-product of the surrounding vectors
            n1 = np.cross(v1, v2)
            n2 = np.cross(v2, v3)
            n3 = np.cross(v3, v4)
            n4 = np.cross(v4, v1)
            n = (n1 + n2 + n3 + n4) / 4.0

            # Normalize the normal vector
            normals[i, j] = n / np.linalg.norm(n)

    # Handle the edges and corners separately if needed
    # ...

    return normals

def drawEgg(N):
    vertices = np.zeros((N, N, 3))
    for i in range(N):
        u = i / (N - 1)
        for j in range(N):
            v = j / (N - 1)
            x = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * np.cos(np.pi * v)
            y = 160 * pow(u, 4) - 320 * pow(u, 3) + 160 * pow(u, 2) - 5
            z = (-90 * pow(u, 5) + 225 * pow(u, 4) - 270 * pow(u, 3) + 180 * pow(u, 2) - 45 * u) * np.sin(np.pi * v)
            vertices[i, j] = [x, y, z]
    normals = calculate_normals(vertices, N)
    return vertices,normals


def draw_prymitive(vertices, normals, N):
    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(normals[i][j])
            glVertex3fv(vertices[i][j])
            glNormal3fv(normals[i+1][j])
            glVertex3fv(vertices[i+1][j])
        glEnd()


def draw_points(vertices, N):
    glBegin(GL_POINTS)  # Rozpoczyna rysowanie używając punktów
    for i in range(N):
        for j in range(N):
            glVertex3fv(vertices[i][j])  # Rysuje pojedynczy punkt dla każdego wierzchołka
    glEnd()


def draw_lines(vertices, N):
    glBegin(GL_LINES)
    for i in range(N - 1):
        for j in range(N - 1):
            # Linie poziome
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i][j + 1])

            # Linie pionowe
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i + 1][j])

            # Dodatkowe linie na przekątnych dla lepszej wizualizacji
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i + 1][j + 1])

            if j > 0:
                # Przekątne w drugą stronę
                glVertex3fv(vertices[i][j])
                glVertex3fv(vertices[i + 1][j - 1])
    glEnd()


def draw_triangles(vertices, N):
    glBegin(GL_TRIANGLES)
    for i in range(N - 1):
        for j in range(N - 1):
            # Pierwszy trójkąt każdego kwadratu siatki
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i + 1][j])
            glVertex3fv(vertices[i][j + 1])

            # Drugi trójkąt każdego kwadratu siatki
            glVertex3fv(vertices[i + 1][j])
            glVertex3fv(vertices[i + 1][j + 1])
            glVertex3fv(vertices[i][j + 1])
    glEnd()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)

    # Enable light number 0
    glEnable(GL_LIGHT0)

    # Set position and color of light
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 10.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.9, 0.9, 0.9, 1.0])

    # Set material properties which will reflect the light
    glMaterialfv(GL_FRONT, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    spin(time * 180 / 3.1415)
    N = 30

    egg_vert,normals = drawEgg(N)
    draw_prymitive(egg_vert, normals, N)

    axes()
    glFlush()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
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
