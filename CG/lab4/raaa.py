from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from tkinter import *


class Cylinder:
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height
        a = int(input("Enter the accuracy of circle: "))
        self.appr = a
        self.longs = a
        self.userTheta = 0
        self.userHeight = 0
        self.light = [1.0, 1.0, 1.25]
        b = float(input("Enter the lighting level: "))
        self.intensity = [b, b, b]
        self.ambient_intensity = [0.1, 0.1, 0.1]
        # Поверхность (SMOTH или FLAT)
        self.surface = GL_SMOOTH

    def init(self):
        # Цвет бэкграунда
        glClearColor(0.0, 0.0, 0.0, 0.0)
        self.compute_location()
        # Закрытие объектами друг друга
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        # Модель освещения (включение отражение окружения)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)
        # Начало работы со светильником 0
        glEnable(GL_LIGHT0)
        # Установка светильника и его уровня освещения
        glLightfv(GL_LIGHT0, GL_POSITION, self.light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)
        # Включеие окрашивания поверхности
        glEnable(GL_COLOR_MATERIAL)
        # Окраска передней части
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    def compute_location(self):
        x = 2 * cos(self.userTheta)
        y = 2 * sin(self.userTheta)
        z = self.userHeight
        d = sqrt(x * x + y * y + z * z) * 0.5
        # Установка режима матрицы
        glMatrixMode(GL_PROJECTION)
        # Замена матрицы
        glLoadIdentity()
        glFrustum(-d, d, -d, d, d, 5)
        # Начальное положение видимости
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    def drawCylinder(self):
        circle_pts = []
        for i in range(self.appr + 1):
            angle = 2 * pi * (i / float(self.appr))
            x = self.radius * cos(angle)
            y = self.radius * sin(angle)
            pt = (x, y)
            circle_pts.append(pt)

        glBegin(GL_TRIANGLE_FAN)  # drawing the back circle
        glNormal(0, 0, self.height / 2.0)
        glVertex(0, 0, self.height / 2.0)
        for (x, y) in circle_pts:
            z = self.height / 2.0
            glVertex(x, y, z)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)  # drawing the front circle
        glNormal(0, 0, self.height / 2.0)
        glVertex(0, 0, self.height / 2.0)
        for (x, y) in circle_pts:
            z = -self.height / 2.0
            glVertex(x, y, z)
        glEnd()

        glBegin(GL_TRIANGLE_STRIP)  # draw the tube
        for (x, y) in circle_pts:
            z = self.height / 2.0
            glNormal(x, y, z)
            glVertex(x, y, z)
            glNormal(x, y, -z)
            glVertex(x, y, -z)
        glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Цвет оокрашивания
        glColor3f(0.5, 0.0, 0.0)
        # Модель шейдеров
        glShadeModel(self.surface)
        self.drawCylinder()
        self.draw_coordinate_system()
        self.draw_light()
        # Замена буфера на другое окно
        glutSwapBuffers()

    def draw_coordinate_system(self):
        glBegin(GL_LINES)
        # oX
        glColor3f(1.0, 0.0, 0.0);
        glVertex3f(0.0, 0.0, 0.0);
        glVertex3f(3.0, 0.0, 0.0);
        # oY
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f(0.0, 0.0, 0.0);
        glVertex3f(0.0, 3.0, 0.0);
        # oZ
        glColor3f(0.0, 0.0, 1.0);
        glVertex3f(0.0, 0.0, 0.0);
        glVertex3f(0.0, 0.0, 3.0);
        glEnd()

    def draw_light(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        # Светильник
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(0.0, 0.0, 2.0)
        glEnd()

    def special(self, key, x, y):
        # камера up/down
        if key == GLUT_KEY_UP:
            self.userHeight += 0.1
        if key == GLUT_KEY_DOWN:
            self.userHeight -= 0.1
        # Кручение камеры
        if key == GLUT_KEY_LEFT:
            self.userTheta += 0.1
        if key == GLUT_KEY_RIGHT:
            self.userTheta -= 0.1
        # Изменение поверхности
        if key == GLUT_KEY_HOME:
            if self.surface == GL_FLAT:
                self.surface = GL_SMOOTH
            else:
                self.surface = GL_FLAT
        # Изменение освещения
        if key == GLUT_KEY_PAGE_UP:
            b = max(self.intensity)
            for i in range(0, 3):
                self.intensity.pop()
            self.intensity += [b + 0.2, b + 0.2, b + 0.2]
            glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)
        if key == GLUT_KEY_PAGE_DOWN:
            b = max(self.intensity)
            for i in range(0, 3):
                self.intensity.pop()
            if b <= 0.2:
                self.intensity += [0.0, 0.0, 0.0]
            else:
                self.intensity += [b - 0.2, b - 0.2, b - 0.2]
            glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)
        self.compute_location()
        glutPostRedisplay()


def main():
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(600, 600)
        glutInitWindowPosition(400, 100)
        glutCreateWindow(b"Cylinder")
        s = Cylinder(0.7, 1.2)
        s.init()
        glutDisplayFunc(s.display)
        glutSpecialFunc(s.special)
        glutMainLoop()


if __name__ == '__main__':
    main()
