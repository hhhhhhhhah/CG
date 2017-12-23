#!-*-coding:utf-8-*-

import math
import numpy
import sys
from numpy.linalg import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from PyQt4 import QtCore, QtGui, QtOpenGL

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL overpainting",
            "PyOpenGL must be installed to run this example.")
    sys.exit(1)

(Ui_MainWindow, QMainWindow) = uic.loadUiType("window.ui")

class GLWidget(QtOpenGL.QGLWidget): # класса области отрисовки
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.a = []  # массив координат опорных точек
        self.d = []  # массив координат производных
        self.b = []  # массив коэфициентов Bi
        self.t = []  # массив параметров
        self.f = False

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glCallList(1)
        if len(self.a) > 1:
            self.buildPoint()
        if len(self.d) > 1:
            self.buildDer()
        if len(self.b) > 1:
            self.buildSp()

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, -20.0, 20.0)
        glViewport(0, 0, w, h)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.makeObject()

    def makeObject(self): # построение единичных осей
        glNewList(1, GL_COMPILE)
        glColor3f(0.0, 0.0, 1.0)  # x
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glEnd()
        glColor3f(0.0, 1.0, 0.0)  # y
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glEnd()
        glColor3f(1.0, 0.0, 0.0)  # z
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()
        glEndList()

    @pyqtSlot()
    def rotXacw(self):  # поворот против часовой стрелки (ч.с.) оси Х
        glRotated(45, 1.0, 0.0, 0.0)
        self.updateGL()

    @pyqtSlot()
    def rotXcw(self): # поворот по ч.с.оси Х
        glRotated(-45, 1.0, 0.0, 0.0)
        self.updateGL()

    @pyqtSlot()
    def rotYacw(self): # поворот против ч.с. оси Y
        glRotated(45, 0.0, 1.0, 0.0)
        self.updateGL()

    @pyqtSlot()
    def rotYcw(self): # поворот по ч.с. оси Y
        glRotated(-45, 0.0, 1.0, 0.0)
        self.updateGL()

    @pyqtSlot()
    def rotZacw(self): # поворот против ч.с. оси Z
        glRotated(45, 0.0, 0.0, 1.0)
        self.updateGL()

    @pyqtSlot()
    def rotZcw(self): # поворот по ч.с. оси Z
        glRotated(-45, 0.0, 0.0, 1.0)
        self.updateGL()

    @pyqtSlot()
    def buildPoint(self): # отрисовка полигона кривой
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.makeObject()
        glCallList(1)
        glNewList(2, GL_COMPILE)
        glColor3f(1.0, 1.0, 1.0)
        k = len(self.a)
        if k > 1:
            for i in range(k):
                if len(self.a[i]) == 2:
                    glPointSize(5)
                    glBegin(GL_POINTS)
                    glVertex2f(self.a[i][0], self.a[i][1])
                    glEnd()
                else:
                    glPointSize(5)
                    glBegin(GL_POINTS)
                    glVertex3f(self.a[i][0], self.a[i][1], self.a[i][2])
                    glEnd()
            glColor3f(0.5, 0.5, 0.5)
            glBegin(GL_LINE_STRIP)
            for i in range(k):
                if len(self.a[i]) == 2:
                    glVertex2f(self.a[i][0], self.a[i][1])
                else:
                    glVertex3f(self.a[i][0], self.a[i][1], self.a[i][2])
            glEnd()
            glEndList()
            glCallList(2)
            self.swapBuffers()

    @pyqtSlot()
    def buildDer(self): # отрисовка векторов производных
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.makeObject()
        glCallList(1)
        glCallList(2)
        glNewList(3, GL_COMPILE)
        k = len(self.d)
        m = len(self.a)
        if k > 1:
            glColor3f(0.0, 0.3, 0.3)
            if len(self.d[0]) == 2:
                glBegin(GL_LINES)
                glVertex2f(self.a[0][0], self.a[0][1])
                glVertex2f(self.d[0][0]+self.a[0][0], self.d[0][1]+self.a[0][1])
                glEnd()
                glBegin(GL_LINES)
                glVertex2f(self.a[m-1][0], self.a[m-1][1])
                glVertex2f(self.d[1][0]+self.a[m-1][0], self.d[1][1]+self.a[m-1][1])
                glEnd()
            else:
                glBegin(GL_LINES)
                glVertex3f(self.a[0][0], self.a[0][1], self.a[0][2])
                glVertex3f(self.d[0][0]+self.a[0][0], self.d[0][1]+self.a[0][1], self.d[0][2]+self.a[0][2])
                glEnd()
                glBegin(GL_LINES)
                glVertex3f(self.a[m-1][0], self.a[m-1][1], self.a[m-1][2])
                glVertex3f(self.d[1][0]+self.a[m-1][0], self.d[1][1]+self.a[m-1][1], self.d[1][2]+self.a[m-1][2])
                glEnd()
        glEndList()
        glCallList(3)
        self.swapBuffers()

    @pyqtSlot()
    def buildSp(self): # построение сплайна
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.makeObject()
        glCallList(1)
        glCallList(2)
        if self.f:
            glCallList(3)
        glNewList(4, GL_COMPILE)
        k = len(self.a)
        if len(self.b) > 1:
            glColor3f(1.0, 0.0, 1.0)
            if len(self.a[0]) == 2:
                glBegin(GL_LINE_STRIP)
                for i in range(k - 1):
                    glVertex2f(self.a[i][0], self.a[i][1])
                    for j in range(1, 21):
                        x = self.b[i][0][0] + self.b[i][1][0] * (self.t[i+1] * j)/20.0 + self.b[i][2][0] * pow((self.t[i+1] * j)/20.0, 2) + \
                            self.b[i][3][0] * pow((self.t[i+1] * j)/20.0, 3)
                        y = self.b[i][0][1] + self.b[i][1][1] * (self.t[i+1] * j)/20.0 + self.b[i][2][1] * pow((self.t[i+1] * j)/20.0, 2) + \
                            self.b[i][3][1] * pow((self.t[i+1] * j)/20.0, 3)
                        glVertex2f(x, y)
                glVertex2f(self.a[k-1][0], self.a[k-1][1])
                glEnd()
            else:
                glBegin(GL_LINE_STRIP)
                for i in range(k - 1):
                    glVertex3f(self.a[i][0], self.a[i][1], self.a[i][2])
                    for j in range(1, 21):
                        x = self.b[i][0][0] + self.b[i][1][0] * (self.t[i+1] * j)/20.0 + self.b[i][2][0] * pow((self.t[i+1] * j)/20.0, 2) + \
                            self.b[i][3][0] * pow((self.t[i+1] * j)/20.0, 3)
                        y = self.b[i][0][1] + self.b[i][1][1] * (self.t[i+1] * j)/20.0 + self.b[i][2][1] * pow((self.t[i+1] * j)/20.0, 2) + \
                            self.b[i][3][1] * pow((self.t[i+1] * j)/20.0, 3)
                        z = self.b[i][0][2] + self.b[i][1][2] * (self.t[i+1] * j)/20.0 + self.b[i][2][2] * pow((self.t[i+1] * j)/20.0, 2) + \
                            self.b[i][3][2] * pow((self.t[i+1] * j)/20.0, 3)
                        glVertex3f(x, y, z)
                glVertex3f(self.a[k-1][0], self.a[k-1][1], self.a[k-1][2])
                glEnd()
        glEndList()
        glCallList(4)
        self.swapBuffers()

    @pyqtSlot()
    def scalep(self): # увеличение масштаба под сплайн
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.makeObject()
        glCallList(1)
        glCallList(2)
        if self.f:
            glCallList(3)
        glCallList(4)
        k = len(self.a)
        minxyz = []
        maxxyz = []
        temp = []
        for j in range(len(self.a[0])):
            for i in range(k):
                temp.append(self.a[i][j])
            minxyz.append(min(temp))
            maxxyz.append(max(temp))
            temp = []
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(minxyz[0]-1.0, maxxyz[0]+1.0, minxyz[1]-1.0, maxxyz[1]+1.0, -20.0, 20.0)
        self.updateGL()

    @pyqtSlot()
    def scalem(self): # возврат масштаба по умолчанию
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, -20.0, 20.0)
        self.updateGL()



class MainWindow(QMainWindow): # класс основого окна

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.glw = GLWidget()
        self.ui.hl.addWidget(self.glw)

        QObject.connect(self.ui.acwX, SIGNAL('clicked()'), self.glw, SLOT('rotXacw()'))
        QObject.connect(self.ui.cwX, SIGNAL('clicked()'), self.glw, SLOT('rotXcw()'))

        QObject.connect(self.ui.acwY, SIGNAL('clicked()'), self.glw, SLOT('rotYacw()'))
        QObject.connect(self.ui.cwY, SIGNAL('clicked()'), self.glw, SLOT('rotYcw()'))

        QObject.connect(self.ui.acwZ, SIGNAL('clicked()'), self.glw, SLOT('rotZacw()'))
        QObject.connect(self.ui.cwZ, SIGNAL('clicked()'), self.glw, SLOT('rotZcw()'))

        QObject.connect(self.ui.splineC, SIGNAL('clicked()'), self.glw, SLOT('buildSp()'))

        QObject.connect(self.ui.btPoint, SIGNAL('clicked()'), self.glw, SLOT('buildPoint()'))
        QObject.connect(self.ui.btDer, SIGNAL('clicked()'), self.glw, SLOT('buildDer()'))

        QObject.connect(self.ui.btScp, SIGNAL('clicked()'), self.glw, SLOT('scalep()'))
        QObject.connect(self.ui.btScm, SIGNAL('clicked()'), self.glw, SLOT('scalem()'))

    def __del__(self):
        self.ui = None

    def getT(self, n): # расчёт параметров
        t = []
        t.append(0)
        k = len(self.glw.a)
        l = len(self.glw.a[0])
        if n:
            for i in range(k-1):
                t.append(1)
        else:
            for i in range(k-1):
                if l == 2:
                    t.append(math.sqrt(pow((self.glw.a[i+1][0] - self.glw.a[i][0]), 2) +
                                       pow((self.glw.a[i+1][1] - self.glw.a[i][1]), 2)))
                else:
                    t.append(math.sqrt(pow((self.glw.a[i+1][0] - self.glw.a[i][0]), 2) +
                                       pow((self.glw.a[i+1][1] - self.glw.a[i][1]), 2) +
                                       pow((self.glw.a[i+1][2] - self.glw.a[i][2]), 2)))
        return t

    def genMatr(self, k): # создание двумерного массива
        m = []
        for i in range(k):
            m.append([])
            for j in range(k):
                m[i].append(0)
        return m

    def genVect(self, k): # создание одномерного массива
        r = []
        for i in range(k):
                r.append(0)
        return r

    def valueM(self, m, i, t): # расчёт элементов матрицы М
        m[i][i-1] = t[i+1]
        m[i][i] = 2 * (t[i+1] + t[i])
        m[i][i+1] = t[i]

    def valueR(self, r, i, t): # расчёт элементов матрицы R
        l = len(self.glw.a[0])
        sub_a1 = [self.glw.a[i+1][j] - self.glw.a[i][j] for j in range(l)]
        sub_a2 = [self.glw.a[i][j] - self.glw.a[i-1][j] for j in range(l)]
        sub_a1 = [x*pow(t[i], 2) for x in sub_a1]
        sub_a2 = [x*pow(t[i+1], 2) for x in sub_a2]
        sub_a = [sub_a1[j] + sub_a2[j] for j in range(len(sub_a1))]
        r[i] = [x*3/(t[i] * t[i+1]) for x in sub_a]

    def getMandR(self, t): # получение матриц М и R
        k = len(self.glw.a)
        m = self.genMatr(k)
        r = self.genVect(k)
        for i in range(1, k-1):
            self.valueM(m, i, t)
        for i in range(1, k-1):
            self.valueR(r, i, t)

        if self.ui.bcStr.isChecked() and len(self.glw.d) > 1:
            m[0][0] = 1
            m[k-1][k-1] = 1
            r[0] = self.glw.d[0]
            r[k-1] = self.glw.d[1]

        elif self.ui.bcSl.isChecked():
            m[0][0] = 1
            m[0][1] = 0.5
            m[k-1][k-2] = 2
            m[k-1][k-1] = 4

            a = [self.glw.a[1][j] - self.glw.a[0][j] for j in range(len(self.glw.a[0]))]
            r[0] = [3.0/(2.0*t[1]) * x for x in a]

            a = [self.glw.a[k-1][j] - self.glw.a[k-2][j] for j in range(len(self.glw.a[0]))]
            r[k-1] = [6/t[k-1] * x for x in a]

        elif (self.ui.bcC.isChecked() or self.ui.bcAc.isChecked()) and k >= 5:
            m[0][0] = 2 * (1 + t[k-1]/t[1])
            m[0][1] = t[k-1]/t[1]

            a = [self.glw.a[1][j] - self.glw.a[0][j] for j in range(len(self.glw.a[0]))]
            r[0] = [3 * t[k-1]/pow(t[1], 2) * x for x in a]
            a = [self.glw.a[k-2][j] - self.glw.a[k-1][j] for j in range(len(self.glw.a[0]))]
            a = [3/t[k-1] * x for x in a]
            if self.ui.bcC.isChecked():
                m[0][k-2] = 1
                r[0] = [r[0][i] - a[i] for i in range(len(a))]
            else:
                m[0][k-2] = -1
                r[0] = [r[0][i] + a[i] for i in range(len(a))]
            del m[k-1]
            del r[k-1]
            for i in range(k-1):
                del m[i][k-1]
        return m, r

    def floatArr(self, a): # преобразование списка NumPy в обычный список Python
        b =[]
        for i in range(len(a)):
            b.append([])
            for j in range(len(a[i])):
                b[i].append(0)
                b[i][j] = float(a[i][j])
        return b

    def updateMs(self): # обновление при изменении граничного условия
        if self.ui.bcSl.isChecked() or self.ui.bcC.isChecked() or self.ui.bcAc.isChecked():
            self.ui.twp.setEnabled(False)
        else:
            self.ui.twp.setEnabled(True)
        self.getB(self.ui.splineH.isChecked())
        self.glw.f = self.ui.twp.isEnabled()

    def getG(self, i, pp): # расчёт элементов матрицы G
        g = self.genVect(4)
        g[0] = self.glw.a[i]
        g[1] = pp[i]
        g[2] = self.glw.a[i+1]
        g[3] = pp[i+1]
        return g

    def getPP(self, m, r): # получение матрицы, хранящей координаты производных всех опорных точек
        pp = self.floatArr((numpy.dot(inv(m), r)))
        if self.ui.bcC.isChecked():
            pp.append(pp[0])
        elif self.ui.bcAc.isChecked():
            pp.append([x*(-1) for x in pp[0]])
        return pp

    def valueB(self, i, t, pp, v): # расчёт элементов матрицы B
        g = self.getG(i, pp)
        v[0] = [1, 0, 0, 0]
        v[1] = [0, 1, 0, 0]
        v[2] = [-3.0/pow(t[i+1], 2), -2.0/t[i+1], 3.0/pow(t[i+1], 2), -1.0/t[i+1]]
        v[3] = [2.0/pow(t[i+1], 3), 1.0/pow(t[i+1], 2), -2.0/pow(t[i+1], 3), 1.0/pow(t[i+1], 2)]
        return self.floatArr(numpy.dot(v, g))

    def getB(self, n): # получение коэффициентов Bi
        t = self.getT(n)
        m, r = self.getMandR(t)
        k = len(self.glw.a) - 1
        v = self.genVect(4)
        pp = self.getPP(m, r)
        b = self.genVect(k)
        for i in range(k):
            b[i] = self.valueB(i, t, pp, v)
        self.glw.b = b
        self.glw.t = t

    def checkData(self, q): # проверка введённых данных
        c = True
        for i in range(q.rowCount()):
            for j in range(q.columnCount()):
                twi = QTableWidgetItem(q.item(i, j))
                try:
                    if type(float(twi.text())) == float and c:
                        c = True
                except ValueError:
                    c = False
                    break
            if c == False:
                break
        return c

    def changeDer(self): # изменение значений производных в начальной и конечной точек на противоположные
        if len(self.glw.d) > 1:
            self.glw.d[0] = [self.glw.d[0][j] for j in range(len(self.glw.d[0]))]
            self.glw.d[1] = [self.glw.d[1][j] for j in range(len(self.glw.d[1]))]
            for i in range(self.ui.twp.rowCount()):
                for j in range(self.ui.twp.columnCount()):
                    twi = QTableWidgetItem((self.glw.d[i][j] * (-1.0)).__str__())
                    self.ui.twp.setItem(i, j, twi)

    def updateData(self): # перерасчёт коэффициентов Bi
        self.getB(self.ui.splineH.isChecked())

    def updateA(self): # обновление матрицы А
        a =[]
        self.updateMatr(self.ui.twc, a)
        self.glw.a = a
        if (self.ui.bcSl.isChecked() and len(self.glw.d) > 1) or self.ui.bcSl.isChecked() or self.ui.bcC.isChecked() \
                or self.ui.bcAc.isChecked():
            self.getB(self.ui.splineH.isChecked())

    def updateD(self): # обновление матрицы D
        self.glw.d = []
        self.glw.f = self.ui.twp.isEnabled()
        if self.glw.f:
            d = []
            self.updateMatr(self.ui.twp, d)
            self.glw.d = d
            self.getB(self.ui.splineH.isChecked())

    def updateMatr(self, qtw, m): # общий метод обновления
        if self.checkData(qtw):
            for i in range(qtw.rowCount()):
                m.append([])
                for j in range(qtw.columnCount()):
                    m[i].append(0)
                    twi = QTableWidgetItem(qtw.item(i, j))
                    m[i][j] = float(twi.text())

    def op_col(self): # удаление/добавление столбца в соответствии с размерностью пространства
        cc = self.ui.twc.columnCount()
        if cc == 2 and self.ui.ch3d.isChecked():
            self.ui.twc.setColumnCount(cc+1)
            self.ui.twp.setColumnCount(cc+1)
        elif self.ui.twc.columnCount() == 3 and self.ui.ch3d.isChecked() == False:
            self.ui.twc.setColumnCount(cc-1)
            self.ui.twp.setColumnCount(cc-1)
        self.ui.twc.setHorizontalHeaderItem(2, QTableWidgetItem("Z"))
        self.ui.twp.setHorizontalHeaderItem(2, QTableWidgetItem("Z"))
        self.updateA()

    def add_row(self): # добавление точки
        if self.ui.twc.rowCount() <= 19:
            self.ui.twc.setRowCount(self.ui.twc.rowCount()+1)
            self.updateA()

    def del_row(self): # удаление точки
        if self.ui.twc.rowCount() > 3:
            self.ui.twc.setRowCount(self.ui.twc.rowCount()-1)
            self.updateA()

    def fill(self, x, y, der): # заполнение таблциц
        self.ui.twc.setRowCount(len(x))
        self.ui.twc.setColumnCount(2)
        self.ui.twp.setColumnCount(2)
        self.ui.ch3d.setChecked(False)
        for i in range(len(x)):
            twi = QTableWidgetItem(x[i].__str__())
            self.ui.twc.setItem(i, 0, twi)
            twi = QTableWidgetItem(y[i].__str__())
            self.ui.twc.setItem(i, 1, twi)
        for i in range(2):
            twi = QTableWidgetItem(der[i].__str__())
            self.ui.twp.setItem(0, i, twi)
            twi = QTableWidgetItem(der[i+2].__str__())
            self.ui.twp.setItem(1, i, twi)

    def fill1(self): # пример 1
        x = [2, 2.5, 3, 1, 1.5, 4, 3.5, 0, 0.5, 5, 4.5]
        y = [2, 3, 1, 1.5, 4, 3.5, 0, 0.5, 5, 4.5, 0]
        der = [1, 2, -1, -1]
        self.fill(x, y, der)

    def fill2(self): # пример 2
        x = [3, 4, 6, 4, 5, 3, 1, 2, 0, 2, 3]
        y = [5, 3, 3, 2, 0, 1, 0, 2, 3, 3, 5]
        der = [1, -2, 1, 2]
        self.fill(x, y, der)

# -----------------------------------------------------#
if __name__ == '__main__': # основаная программа
    app = QtGui.QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle(w.trUtf8("Кубический сплайн и кривая Эрмита"))
    w.show()
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    QObject.connect(w.ui.btExit, SIGNAL('clicked()'), app, SLOT('quit()'))

    sys.exit(app.exec_())