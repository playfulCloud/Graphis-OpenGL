import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *



def drawSquare(cordsToPlaceX, cordsToPlaceY, sizeA, sizeB):
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(cordsToPlaceX, cordsToPlaceY)
    glVertex2f(cordsToPlaceX+sizeA, cordsToPlaceY)
    glVertex2f(cordsToPlaceX, cordsToPlaceY+sizeB)
    glEnd()
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    secondTriangleX = cordsToPlaceX+sizeA
    secondTriangleY = cordsToPlaceX+sizeB
    glVertex2f(secondTriangleX, secondTriangleY)
    glVertex2f(cordsToPlaceX+sizeA, cordsToPlaceY)
    glVertex2f(cordsToPlaceX, cordsToPlaceY+sizeB)
    glEnd()



def drawSquareWithDeformationAndRandomColor(cordsToPlaceX, cordsToPlaceY, sizeA, sizeB,deformation = 1.0):
    glBegin(GL_TRIANGLES)
    sizeA = sizeA * deformation
    sizeB = sizeB * deformation
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(cordsToPlaceX, cordsToPlaceY)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(cordsToPlaceX + sizeA, cordsToPlaceY)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(cordsToPlaceX, cordsToPlaceY + sizeB)
    glEnd()

    glBegin(GL_TRIANGLES)
    secondTriangleX = cordsToPlaceX + sizeA
    secondTriangleY = cordsToPlaceX + sizeB
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(secondTriangleX, secondTriangleY)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(cordsToPlaceX + sizeA, cordsToPlaceY)
    glColor3f(random.random(), random.random(), random.random())
    glVertex2f(cordsToPlaceX, cordsToPlaceY + sizeB)
    glEnd()

def sierpinski(cordsToPlaceX, cordsToPlaceY, size, level):
    if level == 0:
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(cordsToPlaceX, cordsToPlaceY)
        glVertex2f(cordsToPlaceX + size, cordsToPlaceY)
        glVertex2f(cordsToPlaceX + size, cordsToPlaceY + size)
        glVertex2f(cordsToPlaceX, cordsToPlaceY + size)
        glEnd()
    else:
        size /= 3
        level -= 1
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                sierpinski(cordsToPlaceX + i * size, cordsToPlaceY + j * size, size, level)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    #drawSquareWithDeformationAndRandomColor(10.0,10.0,50.0,50.0,-2) # dziala rysowanie prostokąta
    sierpinski(10.0,10.0,100.0,4) # dziala rysowanie prostokąta
    # glColor3f(0.0, 1.0, 0.0)
    # glBegin(GL_LINES)
    # glVertex2f(0.0, 0.0)
    # glVertex2f(50.0, 0.0)
    # glEnd()

    # glColor3f(1.0, 0.0, 0.0)
    # glBegin(GL_TRIANGLES)
    # glVertex2f(0.0, 0.0)
    # glVertex2f(0.0, 50.0)
    # glVertex2f(-50.0, 0.0)
    # glEnd()

    glFlush()


# Przygotowanie rzutni -> zwiększenie pola na jakim rysowany jest obraz.
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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, "akwamaryna", None, None)
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