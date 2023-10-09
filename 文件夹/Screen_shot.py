from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__((parent))
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.isPressLeft = False
        self.pos = []
        self.shape = None

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        if self.shape == 'rect':
            # rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
            rect = self.getRectangle()
            # print(rect)
            painter.drawRect(rect)
        elif self.shape=='point':
            painter.setPen(QPen(Qt.black, 0.1, Qt.SolidLine))
            painter.drawPoint(5, 5)

    def cancelselect(self):
        pass
        # self.setPixmap(QPixmap(""))  # 移除label上的图片
        # self.clear()
        # self.repaint()

    def getRectangle(self):
        res = self.getRectPos()
        x0, y0 = res[0]
        x1, y1 = res[1]
        pickRectWidth = int(qAbs(x0 - x1))
        pickRectHeight = int(qAbs(y0 - y1))
        pickRectTop = x0 if x0 < x1 else x1
        pickRectLeft = y0 if y0 < y1 else y1
        self.pickRect = QRect(pickRectTop, pickRectLeft, pickRectWidth, pickRectHeight)
        # 避免高度宽度为0时候报错
        if pickRectWidth == 0:
            self.pickRect.setWidth(2)
        if pickRectHeight == 0:
            self.pickRect.setHeight(2)
        return self.pickRect

    def mousePressEvent(self, event):
        self.isPressLeft = True
        self.x0 = event.x()
        self.y0 = event.y()
        print(self.x0)

    def mouseMoveEvent(self, event):
        if self.isPressLeft:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        global jpg
        QLabel.mouseReleaseEvent(self, event)
        if self.isPressLeft:
            # res = self.getRectPos()
            # x0,y0 = res[0]
            # x1,y1 = res[1]
            # error = False
            # print(x0,y0,x1,y1)
            # if x0!=0 and y0!=0:
            #     if x1==0 and y1==0:
            #         error = True
            #     if x1<x0 or y1<y0:
            #         error =True
            # if error:
            #     self.pos = []
            # else:
            #     crop_img = jpg[2*y0:2*y1, 2*x0:2*x1]
            #     # cv2.imshow("crop_img", crop_img)
            #     # cv2.waitKey()
            #     # cv2.destroyAllWindows()
            # #print(crop_img)
            self.isPressLeft = False

    def getRectPos(self):#相对坐标，相对label左上角的坐标
        self.pos=[]
        self.pos.append((self.x0, self.y0))
        self.pos.append((self.x1, self.y1))

        return self.pos
