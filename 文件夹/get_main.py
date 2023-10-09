import sys
import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, \
    QPushButton, QLineEdit, QRadioButton, QToolBar, QFileDialog
from PyQt5.QtCore import *
from  login import Login_window
import pymysql
from new_mainwindow import MainWindow
import os
from Screen_shot import MyLabel
import image_process_methods as IPM
import image_window as IPW
from work import worker
import sys
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog
from login import Login_window
import pymysql
from new_mainwindow import MainWindow
import os
import image_process_methods as IPM
import image_window as IPW
from work import worker
from yolov5.detect import run, run2
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import check_img_size


def is_Chinese(word):
    for ch in word:
        if '\u4e00' > ch or ch > '\u9fff':
            return False
    return True

def is_month(month):
    return  1 <= eval(month) <= 12

def is_day(day):
    return 1 <= eval(day) <= 31

class Ocr_demo():
    def __init__(self):
        self.login_window = Login_window() # 登录界面窗口
        self.main_window = MainWindow() # 主界面窗口
        self.worker = worker() # 用户
        self.index = 0 # 索引
        self.timer = QTimer() # 计时器
        self.timer.setInterval(15) # 设置计时器运行时间间隔
        self.cam = cv2.VideoCapture(0) # 摄像头
        self.db = pymysql.connect( # 连接数据库
                host='localhost',
                user="root",
                password='123456',
                database='db1'
            )
        
        self.weights = '../yolov5/yolov5s.pt' # yolo预训练网络参数
        self.dnn = False # yolo参数
        self.data = '../yolov5/data/coco128.yaml' # yolo神经网络训练集
        self.half = False # yolo参数
        self.model = DetectMultiBackend(self.weights, dnn=self.dnn, data=self.data, fp16=self.half) # yolo模型
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt # yolo参数

        self.connect() # 运行控件连接函数


    def create_WorkIdandName(self):  # 用户注册第一部分 工号与姓名
        # 新建一个游标对象，用来执行sql语句
        cursor = self.db.cursor()
        # SQL语句, 创建一个新表
        sql = "CREATE TABLE IF NOT EXISTS Accounts (work_id INT ,name VARCHAR(255),birth_day DATE, sex VARCHAR(255),user VARCHAR(255),password VARCHAR(255),root VARCHAR(255));"
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 如果发生错误则回滚事务
            self.db.rollback()
        # print("over")
        # 收集数据
        work_id = self.login_window.workerIdLineEdit.text() # 获取用户输入的工号
        name = self.login_window.nameLineEdit.text() # 获取用户输入的姓名
        if work_id != "" and name != "": # 确保用户进行了输入
            if work_id.isdigit(): # 再进行一次判断，如果用户输入的工号是全数字并且姓名是中文才会进行下一步操作
                self.worker.work_id = eval(work_id) # 获取用户输入的工号
                """此处工号应为数字"""
            else: # 否则清楚用户的输入, 让其重新输入
                self.login_window.workerIdLineEdit.clear()
                self.login_window.warningLabel2.setText("工号输入错误")
            if is_Chinese(name):
                self.worker.name = name
            else:
                self.login_window.nameLineEdit.clear()
                self.login_window.warningLabel2.setText("姓名格式错误")

        if work_id.isdigit() and is_Chinese(name):
            # print(self.worker.work_id)
            # print(self.worker.name)
            self.login_window.stackedWidget_2.setCurrentIndex(1)

        cursor.close() # 关闭游标对象


    def create_BirthdayandSex(self):  # 用户注册，生日性别
        year = self.login_window.yearlineEdit.text() # 年份
        month = self.login_window.monthlineEdit.text() # 月份
        day = self.login_window.daylineEdit.text() # 日
        sex = self.login_window.sexlineEdit.text() # 性别
        if year != "" and month != "" and day != "" and sex != "": # 输入不为空
            if not year.isdigit(): # 判断填写年份格式
                self.login_window.yearlineEdit.clear()
                self.login_window.warningLabel3.setText("年份格式有误")
                return
            if not month.isdigit() and is_month(month): # 判断月份格式
                self.login_window.monthlineEdit.clear()
                self.login_window.warningLabel3.setText("月份格式有误")
                return
            if not day.isdigit() and is_day(day): # 判断日期格式
                self.login_window.daylineEdit.clear()
                self.login_window.warningLabel3.setText("日期格式有误")
                return
            if not len(sex) == 1:
                self.login_window.sexlineEdit.clear()
                self.login_window.warningLabel3.setText("性别信息有误")
            if year.isdigit() and month.isdigit() and day.isdigit() and is_month(month) and is_day(day) and len(sex) == 1: # 判断日期格式是否有问题
                if len(self.login_window.monthlineEdit.text()) != 2: # 在月份前面补0
                    month = "0" + month
                if len(self.login_window.daylineEdit.text()) != 2: # 在日期前面补0
                    day = "0" + day
                # 生成生日日期
                birth_day = year + "-" + month + "-" + day
                self.worker.birth_day = birth_day
                self.worker.sex = sex
                self.login_window.stackedWidget_2.setCurrentIndex(2) # 跳转到下一界面


    # 创建用户账号与密码
    def create_UserandPassword(self):
        """缺少判断用户权限密码"""
        if self.login_window.createUserLineEdit.text() != "" and self.login_window.createPassLineEdit.text() != "":
            self.worker.user = self.login_window.createUserLineEdit.text() # 获取用户
            self.worker.password = self.login_window.createPassLineEdit.text() # 获取密码

            # 创建游标，执行mysql代码
            cursor = self.db.cursor()
            sql = f"INSERT INTO accounts(work_id, name, birth_day, sex, user, password, root) VALUES ({self.worker.work_id}, '{self.worker.name}', '{self.worker.birth_day}', '{self.worker.sex}', '{self.worker.user}', '{self.worker.password}', '{self.worker.root}')"
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
            except:
                # 如果发生错误则回滚
                self.db.rollback()
            cursor.close()
            self.login_window.stackedWidget.setCurrentIndex(0)

    def log_in(self):  # 密码登录
        # 获取用户的账号与密码
        user = self.login_window.user_linedit.text()
        print(user)
        password = self.login_window.password_linedit.text()
        # print(type(user)) type函数打印变量数据类型
        # 连接数据库
        # 创建游标，执行mysql代码
        cursor = self.db.cursor()
        # 写mysql语句
        sql = f"select password, name from accounts where user = {user}"  # 一定给变量加入单引号，因为sql与python字符串格式不一样
        # 执行sql代码
        respnese2 = cursor.execute(sql)  # 返回查询结果的数量，如果是0，则表示什么都没有查到
        if respnese2 != 0:
            response1 = cursor.fetchall()#返回sql语句，返回查询的结果
            password_right = response1[0][0]
            name_right = response1[0][1] # 用户的名字
            # print(name_right)
            # print(password_right)
            if password == password_right:
                if self.login_window.radioButton.isChecked():
                    self.main_window.show()
                    self.login_window.close()
                elif self.login_window.radioButton_2.isChecked():
                    self.main_window.show()
                    self.login_window.close()
                    self.main_window.toCamButton.setEnabled(False) # 将toCamButton按钮设置为不可用
                    self.main_window.toCamButton.setDisabled(True) # 将按钮变成灰色
                    self.main_window.openCamButton.setEnabled(False) # 将openCamButton按钮设置为不可用
                    self.main_window.openCamButton.setDisabled(True) # 将openCamButton按钮设置为灰色
                else:
                    self.login_window.warningLabel.setText("请选择模式")
                    cursor.close()
                    return
            else:
                # print("账号或密码出现错误")
                self.login_window.warningLabel.setText("账号或者密码错误")
                cursor.close() # 用过的游标对象需要关闭, 否则会报错
                return
        else:
            # print("账号不存在")
            self.login_window.warningLabel.setText("输入账号不存在")
            cursor.close()
            return
        # 关闭游标
        cursor.close()
        # 关闭连接
        self.db.close()

    # 打开样例照片
    def open_image(self):
        # 创建选择文件窗口
        file_dialog = QFileDialog()
        # 支持三种格式
        file_dialog.setNameFilter("(*.png *.jpg *bmp)")  # 设置选取的图片的格式，绝对路径没有中文
        if file_dialog.exec_():
            try:
                self.image_path = file_dialog.selectedFiles()[0] # 获取选取图片的路径
                self.main_window.mainScreen.setScaledContents(True)  # 设置放的图片和label一样大
                self.main_window.img = cv2.imread(self.image_path)
                self.main_window.img_copy = self.main_window.img.copy()
                height, width, _ = self.main_window.img.shape
                bytesPerline = 3 * width
                self.qimg = QImage(self.main_window.img_copy.data, width, height, bytesPerline,
                                   QImage.Format_RGB888).rgbSwapped()
                self.main_window.mainScreen.setPixmap(QPixmap.fromImage(self.qimg))
            except:
                print("图像格式有问题")

    # 截图功能
    def get_screen(self):
        self.main_window.mainScreen.shape = "rect"

    # 打开文件夹
    def open_dir(self):
        self.index = 0  # 重置索引=0
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹")  # 起始路径
        if directory:
            dir_files_name = sorted(os.listdir(directory)) # 获取该文件夹下所有文件的名字
            dir_image_name = []  # 存储图片名字列表
            for i in dir_files_name:
                if i.endswith(".png") or i.endswith(".bmp") or i.endswith(".jpg"): # 提取出复合图片格式的文件
                    dir_image_name.append(i)
            # print(dir_image_name)
            self.dir_image_data = []  # 存储图片数据列表
            try:
                for image_name in dir_image_name:
                    image_path = os.path.join(directory, image_name)
                    image_data = cv2.imread(image_path)
                    self.dir_image_data.append(image_data)

            except:
                print("图片数据读取有问题, 可能存在中文")

            # 选取文件夹中第一张图片作为展示
            self.main_window.img = self.dir_image_data[self.index]
            self.main_window.img_copy = self.main_window.img.copy()
            height, width, _ = self.main_window.img_copy.shape
            bytesPerline = 3 * width
            self.qimg = QImage(self.main_window.img_copy.data, width, height, bytesPerline,
                               QImage.Format_RGB888).rgbSwapped()
            self.main_window.mainScreen.setScaledContents(True)
            self.main_window.mainScreen.setPixmap(QPixmap.fromImage(self.qimg))
            self.main_window.dirScreen.setScaledContents(True)
            self.main_window.dirScreen.setPixmap(QPixmap.fromImage(self.qimg))

    # 向上选取图片
    def up_image(self):
        self.index += 1
        if self.index > len(self.dir_image_data) - 1:
            self.index = 0
        self.main_window.img = self.dir_image_data[self.index]
        self.main_window.img_copy = self.main_window.img.copy()
        height, width, _ = self.main_window.img_copy.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.main_window.img_copy.data, width, height, bytesPerline,
                           QImage.Format_RGB888).rgbSwapped()
        self.main_window.mainScreen.setScaledContents(True)
        self.main_window.mainScreen.setPixmap(QPixmap.fromImage(self.qimg))
        self.main_window.dirScreen.setScaledContents(True)
        self.main_window.dirScreen.setPixmap(QPixmap.fromImage(self.qimg))

    # 向下选取图片
    def down_image(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.dir_image_data) - 1
        self.main_window.img = self.dir_image_data[self.index]
        self.main_window.img_copy = self.main_window.img.copy()
        height, width, _ = self.main_window.img_copy.shape
        bytesPerline = 3 * width
        self.qimg = QImage(self.main_window.img_copy.data, width, height, bytesPerline,
                           QImage.Format_RGB888).rgbSwapped()
        self.main_window.mainScreen.setScaledContents(True)
        self.main_window.mainScreen.setPixmap(QPixmap.fromImage(self.qimg))
        self.main_window.dirScreen.setScaledContents(True)
        self.main_window.dirScreen.setPixmap(QPixmap.fromImage(self.qimg))

    # 图片预处理
    def image_process(self):
        # 如果用户已经进行了截图, 就对截图进行处理
        if self.main_window.image_cut is not None:
            self.main_window.img_copy = self.main_window.image_cut
        # method表示使用哪一种图像预处理方法
        method = self.main_window.imgprocesscomboBox.currentText()
        if self.main_window.img_copy is None:
            # print("warning:没有选择照片")
            self.main_window.imgProcessWarningLabel.setText("Error: 没有选择图像预处理对象")
            return
        if method == "复原":
            try:
                self.main_window.img_copy = self.main_window.img.copy()
            except:
                # print("Warning: 复原图片出现问题, 请重试")
                self.main_window.imgProcessWarningLabel.setText("Error: 复现图像有误, 请重试")
                return
        elif method == "灰度值处理":
            try:
                self.main_window.img_copy = IPM.process_grayscale(self.main_window.img_copy)
            except:
                # print("Warning: 已经进行了灰度处理")
                self.main_window.imgProcessWarningLabel.setText("Error: 当前图像格式无法进行灰度化")
                return
        elif method == "均值滤波":
            try:
                self.main_window.img_copy = IPM.mean_filter(self.main_window.img_copy)
            except:
                # print("均值滤波操作出现问题")
                self.main_window.imgProcessWarningLabel.setText("Error: 均值滤波操作有误")
                return
        elif method == "高斯滤波":
            try:
                self.main_window.img_copy = IPM.gaussian_filter(self.main_window.img_copy)
            except:
                # print("高斯滤波操作出现问题")
                self.main_window.imgProcessWarningLabel.setText("Error: 高斯滤波操作有误")
                return
        elif method == "腐蚀":
            try:
                self.main_window.img_copy = IPM.erode_image(self.main_window.img_copy)
            except:
                # print("腐蚀操作出现问题")
                self.main_window.imgProcessWarningLabel.setText("Error: 腐蚀操作有误")
                return
        elif method == "膨胀":
            try:
                self.main_window.img_copy = IPM.dilate_image(self.main_window.img_copy)
            except:
                # print("膨胀操作出现问题")
                self.main_window.imgProcessWarningLabel.setText("Error: 膨胀操作有误")
                return
        elif method == "开运算":
            try:
                self.main_window.img_copy = IPM.opening(self.main_window.img_copy)
            except:
                # print("开运算操作出现问题")
                self.main_window.imgProcessWarningLabel.setText("Error: 开运算操作有误")
                return
        elif method == "闭运算":
            try:
                self.main_window.img_copy = IPM.closing(self.main_window.img_copy)
            except:
                # print("闭运算操作出现问题")
                self.main_window.imgProcessWarningLabel.setText("Error: 闭运算操作有误")
                return
        elif method == "RGB转BGR":
            try:
                self.main_window.img_copy = IPM.rgb_to_bgr(self.main_window.img_copy)
            except:
                # print("Error: 图像不是RGB格式图像")
                self.main_window.imgProcessWarningLabel.setText("Error: 图像格式不为BGR格式, 请调整")
                return
        elif method == "BGR转HSV(需要先转化为BGR图像)":
            try:
                self.main_window.img_copy = IPM.bgr_to_hsv(self.main_window.img_copy)
            except:
                # print("Error: 需要将图像先转换成BGR格式")
                self.main_window.imgProcessWarningLabel.setText("Error: 图像格式不为BGR格式, 请调整")
                return
        elif method == "平移图像":
            self.ipw = IPW.Params_Window(IPM.translate)
            self.ipw.pushButton.clicked.connect(lambda: self.image_button(IPM.translate))
            return # 为了防止运行以下图像展示代码

        elif method == "旋转图像":
            self.ipw = IPW.Params_Window(IPM.rotate)
            self.ipw.pushButton.clicked.connect(lambda: self.image_button(IPM.rotate))
            return

        elif method == "图像镜像":
            self.ipw = IPW.Params_Window(IPM.flip)
            self.ipw.pushButton.clicked.connect(lambda: self.image_button(IPM.flip))
            return

        elif method == "变为黑白图像":
            self.ipw = IPW.Params_Window(IPM.convert_text_to_black_sharpen_and_denoise_with_outline)
            self.ipw.pushButton.clicked.connect(
                lambda: self.image_button(IPM.convert_text_to_black_sharpen_and_denoise_with_outline))
            return
            # 表示图像为彩色
        self.main_window.imgprocessScreen.setScaledContents(True)
        if self.main_window.img_copy.ndim == 3:
            self.qimg2 = QImage(self.main_window.img_copy.data, self.main_window.img_copy.shape[1],
                                self.main_window.img_copy.shape[0], QImage.Format_BGR888)
            self.main_window.imgprocessScreen.setPixmap(QPixmap.fromImage(self.qimg2))
            # 表示图像为灰色
        else:
            self.qimg2 = QImage(self.main_window.img_copy.data, self.main_window.img_copy.shape[1],
                                self.main_window.img_copy.shape[0], QImage.Format_Grayscale8)
            self.main_window.imgprocessScreen.setPixmap(QPixmap.fromImage(self.qimg2))

    def image_process_ok(self):
        self.main_window.mainScreen.setPixmap(QPixmap.fromImage(self.qimg2))

    def image_button(self, function):  # 绑定有参数的图像预处理函数，在选择完参数后，点击后可以进行变换
        self.main_window.imgprocessScreen.setScaledContents(True)
        # 创建参数字典, 用于之后的传参操作
        self.params_dict = {}
        # 收集用户填写的参数
        for i in range(len(self.ipw.params_list)):
            if self.ipw.lineEdit[i].text().isdigit():
                self.params_dict[self.ipw.params_list[i]] = eval(self.ipw.lineEdit[i].text())
            self.params_dict[self.ipw.params_list[i]] = self.ipw.lineEdit[i].text()

        try:
            self.main_window.img_copy = function(self.main_window.img_copy, **self.params_dict)  # 传入字典的方法
        except:
            # print("参数填入有误")
            self.main_window.imgProcessWarningLabel.setText("Error: 参数输入有误, 或超出正常参数范围")
            self.ipw.close()
            return
        # 关闭参数窗口
        self.ipw.close()
        # 展现图像
        if self.main_window.img_copy.ndim == 3:
            self.qimg2 = QImage(self.main_window.img_copy.data, self.main_window.img_copy.shape[1],
                                self.main_window.img_copy.shape[0], QImage.Format_BGR888)
            self.main_window.imgprocessScreen.setPixmap(QPixmap.fromImage(self.qimg2))
            # 表示图像为灰色
        else:
            self.qimg2 = QImage(self.main_window.img_copy.data, self.main_window.img_copy.shape[1],
                                self.main_window.img_copy.shape[0], QImage.Format_Grayscale8)
            self.main_window.imgprocessScreen.setPixmap(QPixmap.fromImage(self.qimg2))

    # 摄像头槽函数
    def set_video(self):
        ret, frame = self.cam.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qt_image)
            self.main_window.camLabel.setPixmap(pixmap)

    # 打开摄像头
    def open_cam(self):
        self.main_window.camLabel.setScaledContents(True)
        self.main_window.stackedWidget.setCurrentIndex(1) # 跳转到摄像头界面
        self.timer.start() # 开启计时器

    # 停止摄像头
    def stop_cam(self):
        self.timer.stop()

    # 开启摄像头
    def start_cam(self):
        self.timer.start()

    # 切换主题
    def to_theme(self):
        self.main_window.stackedWidget_2.setCurrentIndex(0)

    def to_security(self):
        self.main_window.stackedWidget_2.setCurrentIndex(2)

    # 常规设置
    def to_general(self):
        self.main_window.stackedWidget_2.setCurrentIndex(1)

    # yolo识别函数，只能识别选择的图片
    def run_model(self):
        imgsz = check_img_size([640, 640], s=self.stride)  # check image size
        self.img_res = run2(source=self.main_window.img_copy, model=self.model, img_size=imgsz) 
        height, width, channel = self.img_res.shape
        bytes_per_line = 3 * width
        qt_image = QImage(self.img_res.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qt_image)
        self.main_window.mainScreen.setPixmap(pixmap) # 显示结果

    # yolo视频检测函数
    def video_decet(self):
        self.timer.timeout.connect(self.video_object_decetion_image) # 切换成目标识别函数

    # yolo视频目标检测
    def video_object_decetion_image(self):
        ret, frame = self.cam.read()
        imgsz = check_img_size([640, 640], s=self.stride)  # check image size
        if ret:
            frame = run2(source=frame, model=self.model, img_size=imgsz)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(qt_image)
            self.main_window.camLabel.setPixmap(pixmap)



    # 控件连接函数
    def connect(self):
        self.login_window.login_button.clicked.connect(self.log_in) # 登录功能
        self.main_window.openImgButton.clicked.connect(self.open_image) # 打开样例图片
        self.main_window.cutImgButton.clicked.connect(self.get_screen) # 开启截图
        self.main_window.openDirButton.clicked.connect(self.open_dir) # 打开文件夹
        self.main_window.dirupButton.clicked.connect(self.up_image) # 向上选取图片
        self.main_window.dirdownButton.clicked.connect(self.down_image) # 向下选取图片
        self.main_window.viewButton.clicked.connect(self.image_process) # 图片预处理
        self.main_window.imgprocessokButton.clicked.connect(self.image_process_ok) #
        # 注册界面
        self.login_window.nextButton.clicked.connect(self.create_WorkIdandName)
        self.login_window.nextButton_2.clicked.connect(self.create_BirthdayandSex)
        self.login_window.okButton.clicked.connect(self.create_UserandPassword)
        # 摄像头界面操作
        self.main_window.openCamButton.clicked.connect(self.open_cam)
        self.timer.timeout.connect(self.set_video) # 打开摄像头
        # self.timer.timeout.connect(self.video_object_decetion) # 视频目标检测
        self.main_window.camsearchButton.clicked.connect(self.video_decet)
        self.main_window.stopButton.clicked.connect(self.stop_cam) # 停止摄像头
        self.main_window.playButton.clicked.connect(self.start_cam) # 开启摄像头
        # 设置界面
        self.main_window.themeButton.clicked.connect(self.to_theme)
        self.main_window.safeButton.clicked.connect(self.to_security)
        self.main_window.generalButton.clicked.connect(self.to_general)
        # 模型识别
        self.main_window.moudleokButton.clicked.connect(self.run_model)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_demo = Ocr_demo()
    sys.exit(app.exec_())












