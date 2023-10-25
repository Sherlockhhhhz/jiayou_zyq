#图像有参数的函数
import sys
import inspect
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication
from os_demo.tools import image_process_methods as IPM


class Params_Window(QWidget):
    def __init__(self,function: callable):
        super().__init__()
        self.function = function  # 获取对应的函数
        self.initUI()
#量身定制的输入框
    def initUI(self):
        self.setObjectName("loginWindow")
        self.setStyleSheet('#loginWindow{background-color:white}')
        self.setObjectName("MainWindow")
        self.setWindowTitle("确认参数")
        self.setWindowIcon(QIcon(':/images/images/sys_logo.png'))
        self.resize(400, 300)
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(0, 0, 400, 300))
        self.widget.setStyleSheet("#widget_2{\n"
                                    "background-color: rgb(255, 255, 255);\n"
                                    "border:0px solid;\n"
                                    "border-radius:5px;\n"
                                    "}")
        self.widget.setObjectName("widget_2")
        params = inspect.signature(self.function).parameters
        print(params)
        self.params_list = list(params)
        self.params_list.pop(0)#将image参数去除，因为image参数不需要用户填写
        self.lineEdit = []  # 输入框列表
        _translate = QtCore.QCoreApplication.translate  # 输入中文
        for i in range(len(self.params_list)):
            self.lineEdit.append(QtWidgets.QLineEdit(self.widget))
            self.lineEdit[i].setGeometry(QtCore.QRect(100, 50 + i * 50, 200, 30))
            self.lineEdit[i].setStyleSheet("border:1px solid;\n"
                                           "font: 9pt \"Terminal\";\n"
                                           "color:black;\n")
            self.lineEdit[i].setObjectName(f"lineEdit{i}")
            #判断函数的参数值是否有默认值
            if params[self.params_list[i]].default != inspect.Parameter.empty:
                self.lineEdit[i].setPlaceholderText(
                    _translate("MainWindow", f"默认值为{params[self.params_list[i]].default}"))

            # 文字说明 输入框前面
            self.label = QtWidgets.QLabel(self.widget)
            self.label.setGeometry(QtCore.QRect(50, 50 + i * 50, 20, 30))
            self.label.setStyleSheet("color: black;\n"
                                     "font: 9pt \"Terminal\";\n"
                                     )
            self.label.setObjectName(f"label{i}")
            self.label.setText(_translate("MainWindow", f'{self.params_list[i]} :'))
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(150, 200, 80, 40))
        self.pushButton.setStyleSheet("#pushButton{\n"
                                      "background-color: orange;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 9pt \"Terminal\";\n"
                                      "border:1px solid;\n"
                                      "border-radius:0px;\n"
                                      "}\n"
                                      "#pushButton::pressed{\n"
                                      "background-color: rgb(102, 102, 102);\n"
                                      "}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pw = Params_Window(IPM.linear_trans)
    sys.exit(app.exec_())


