import io
import time
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog
from os_demo.windows.login_window import Login_window
import pymysql
from windows.main_window import MainWindow
import os
from os_demo.tools import image_process_methods as IPM
from os_demo.windows import params_window as IPW
from work import worker
import sys
sys.path.insert(0, './yolov7')
sys.path.append("./windows/MvImport")



# 判断是否是中文
def is_Chinese(word):
    for ch in word:
        if '\u4e00' > ch or ch > '\u9fff':
            return False
    return True


# 判读是否是月份(1-12个月)
def is_month(month):
    return 1 <= eval(month) <= 12


# 判断是否是日期, 有一个问题就是因为不是每一个月都是31天，这里后面还需要修改
def is_day(day):
    return 1 <= eval(day) <= 31




class Ocr_demo():
    def __init__(self):
        self.login_window = Login_window()  # 登录界面窗口
        self.main_window = MainWindow()  # 主界面窗口
        self.worker = worker()  # 用户
        self.index = 0  # 索引
        try:
            self.db = pymysql.connect(  # 连接数据库, 这里作为属性的原因是, 有很多函数都需要连接数据库, 直接作为属性, 可以减小程序开销
                host='localhost',
                user="root",
                password='123456789',
                database='db1'
            )
        except:
            self.db = None # 数据库连接失


        self.connect()  # 运行控件连接函数


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
        work_id = self.login_window.workerIdLineEdit.text()  # 获取用户输入的工号
        name = self.login_window.nameLineEdit.text()  # 获取用户输入的姓名
        if work_id != "" and name != "":  # 输入不能为空, 确保用户进行了输入
            self.worker.name = name
            if work_id.isdigit():  # 再进行一次判断，如果用户输入的工号是全数字并且姓名是中文才会进行下一步操作
                self.worker.work_id = eval(work_id)  # 获取用户输入的工号
                """此处工号应为数字"""
            else:  # 否则清除用户的输入, 让其重新输入
                self.login_window.workerIdLineEdit.clear()
                self.login_window.warningLabel2.setText("工号格式错误, 必须全为数字")  # 提示用户输入错误
        if work_id.isdigit():  # 如果工号和姓名输入正确, 则跳转到下一个界面
            self.login_window.stackedWidget_2.setCurrentIndex(1)

        cursor.close()  # 关闭游标对象

    def create_BirthdayandSex(self):  # 用户注册第二部分, 生日与性别
        year = self.login_window.yearlineEdit.text()  # 获取用户输入的年份
        month = self.login_window.monthlineEdit.text()  # 获取用户输入的月份
        day = self.login_window.daylineEdit.text()  # 获取用户输入的日期
        sex = self.login_window.sexlineEdit.text()  # 获取用户输入的性别性别
        if year != "" and month != "" and day != "" and sex != "":  # 输入不为空
            if not year.isdigit():  # 判断填写年份格式是否正确, 如果不正确, 则会运行下面的代码, 注意这个not
                self.login_window.yearlineEdit.clear()
                self.login_window.warningLabel3.setText("请输入正确的年份格式")
                return
            if not month.isdigit() and is_month(month):  # 判断月份格式
                self.login_window.monthlineEdit.clear()
                self.login_window.warningLabel3.setText("请输入正确的月份格式")
                return
            if not day.isdigit() and is_day(day):  # 判断日期格式
                self.login_window.daylineEdit.clear()
                self.login_window.warningLabel3.setText("请输入正确的日期格式")
                return
            if not len(sex) == 1 and is_Chinese(sex):  # 判断性别格式, 只能是中文且为一个字符
                self.login_window.sexlineEdit.clear()
                self.login_window.warningLabel3.setText("性别信息有误")
            if year.isdigit() and month.isdigit() and day.isdigit() and is_month(month) and is_day(day) and len(
                    sex) == 1:  # 判断日期格式是否有问题
                if len(self.login_window.monthlineEdit.text()) != 2:  # 在月份前面补0, 补0的原因是MySQL的日期格式有要求, 必须是"xxxx-xx-xx"
                    month = "0" + month
                if len(self.login_window.daylineEdit.text()) != 2:  # 在日期前面补0
                    day = "0" + day
                # 生成生日日期
                birth_day = year + "-" + month + "-" + day
                self.worker.birth_day = birth_day
                self.worker.sex = sex
                self.login_window.stackedWidget_2.setCurrentIndex(2)  # 跳转到下一界面

    # 用户注册第三部分, 创建用户账号与密码
    def create_UserandPassword(self):
        """缺少判断用户的权限密码, 后期再加"""
        if self.login_window.createUserLineEdit.text() != "" and self.login_window.createPassLineEdit.text() != "":  # 输入的账号和密码不为空
            self.worker.user = self.login_window.createUserLineEdit.text()  # 获取用户
            self.worker.password = self.login_window.createPassLineEdit.text()  # 获取密码

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

    # 登录
    def log_in(self):
        # 获取用户的账号与密码
        user = self.login_window.user_linedit.text()
        # print(user)
        password = self.login_window.password_linedit.text()
        if user == "123" and password == "123":
            self.login_window.close()
            self.main_window.show()
        # # print(type(user)) type函数打印变量数据类型
        # # 创建游标，执行mysql代码
        # cursor = self.db.cursor()
        # # 写mysql语句
        # sql = f"select password, name from accounts where user = {user}"  # 一定给变量加入单引号，因为sql与python字符串格式不一样
        #
        # # 执行sql代码
        # respnese2 = cursor.execute(sql)  # 返回查询结果的数量，如果是0，则表示什么都没有查到
        # cursor.close()
        # if respnese2 != 0:
        #     response1 = cursor.fetchall()  # 返回sql语句，返回查询的结果
        #     password_right = response1[0][0]  # 用户的正确密码
        #     name_right = response1[0][1]  # 用户的正确名字
        #     self.worker.name = name_right
        #     if password == password_right:  # 如果密码正确
        #         if self.login_window.radioButton.isChecked():  # 如果选择了在线模式
        #             self.main_window.show()  # 打开主界面
        #             self.login_window.close()
        #             # 创建用户专属的表
        #             sql1 = f"CREATE TABLE IF NOT EXISTS {self.worker.name}_data ( image_name VARCHAR(255) NOT NULL,image_data LONGBLOB NOT NULL, upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
        #             cursor1 = self.db.cursor()
        #             try:
        #                 # 执行sql语句
        #                 cursor1.execute(sql1)
        #                 # 提交到数据库执行
        #                 self.db.commit()
        #                 cursor1.close()
        #             except:
        #                 # 如果发生错误则回滚
        #                 self.db.rollback()
        #                 cursor1.close()
        #                 return
        #
        #         elif self.login_window.radioButton_2.isChecked():  # 如果选择了离线模式
        #             self.main_window.show()
        #             self.login_window.close()
        #             self.main_window.toCamButton.setEnabled(False)  # 将toCamButton按钮设置为不可用
        #             self.main_window.toCamButton.setDisabled(True)  # 将按钮变成灰色
        #             self.main_window.openCamButton.setEnabled(False)  # 将openCamButton按钮设置为不可用
        #             self.main_window.openCamButton.setDisabled(True)  # 将openCamButton按钮设置为灰色
        #         else:  # 如果没有选择模式
        #             self.login_window.warningLabel.setText("请选择模式")
        #             return
        #     else:
        #         self.login_window.warningLabel.setText("账号或者密码错误")
        #         return
        # else:
        #     self.login_window.warningLabel.setText("输入账号不存在")
        #     return
        # # 关闭游标
        # cursor.close()

    # 图片像展示
    def show_pic(self, dis, img_source):
        height, width, _ = img_source.shape
        bytesPerline = 3 * width
        self.qimg = QImage(img_source.data, width, height, bytesPerline,
                               QImage.Format_RGB888).rgbSwapped()

        for d in dis:
            d.setScaledContents(True)

            d.setPixmap(QPixmap.fromImage(self.qimg))

    # 灰色图像展示
    def show_gray_pic(self,dis,img_source):
        height, width = img_source.shape
        self.qimg = QImage(img_source.data, width, height,
                           QImage.Format_Grayscale8)

        for d in dis:
            d.setScaledContents(True)
            d.setPixmap(QPixmap.fromImage(self.qimg))

    # 打开样例照片
    def open_image(self):
        # 创建选择文件窗口
        file_dialog = QFileDialog()
        # 支持三种格式
        file_dialog.setNameFilter("(*.png *.jpg *bmp *.svg)")  # 设置选取的图片的格式，绝对路径不能有中文
        if file_dialog.exec_():
            try:
                self.image_path = file_dialog.selectedFiles()[0]  # 获取选取图片的路径
                self.main_window.img = cv2.imread(self.image_path)
                self.main_window.img_copy = self.main_window.img.copy()  # 思考一下为什么需要self.main_window.img_copy
                self.show_pic([self.main_window.mainScreen], self.main_window.img_copy)

            except:
                self.addStringToTable("Error: 图片格式错误")

    # 在输出端里添加文字
    def addStringToTable(self, text):
        # 获取表格的行数
        rowPosition = self.main_window.tableWidget.rowCount()

        # 插入新的行
        self.main_window.tableWidget.setColumnCount(1)
        self.main_window.tableWidget.setRowCount(rowPosition + 1)
        print(text)
        # 在新行的第一列中添加表格项

        self.main_window.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(text))
        self.main_window.tableWidget.setColumnWidth(0, 800)

    # 截图功能
    def get_screen(self):
        self.main_window.mainScreen.shape = "rect"

    # 打开文件夹
    def open_dir(self):
        self.index = 0  # 重置索引=0
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹")  # 起始路径
        self.main_window.textBrowser_4.setText(directory)
        if directory:
            dir_files_name = sorted(os.listdir(directory))  # 获取该文件夹下所有文件的名字
            dir_image_name = []  # 存储图片名字列表
            for i in dir_files_name:
                if i.endswith(".png") or i.endswith(".bmp") or i.endswith(".jpg") or i.endswith(".svg"):  # 提取出复合图片格式的文件
                    dir_image_name.append(i)

            self.dir_image_data = []  # 存储图片数据列表
            try:
                for image_name in dir_image_name:  # 将文件夹图片数据存入dir_iamge_data列表中, 方便后面函数的使用
                    image_path = os.path.join(directory, image_name)
                    image_data = cv2.imread(image_path)
                    self.dir_image_data.append(image_data)


            except:
                self.addStringToTable("Error: 图片文件读取有问题, 可能存在中文")

            # 选取文件夹中第一张图片作为展示, self.index = 0
            self.main_window.img = self.dir_image_data[self.index]
            self.main_window.img_copy = self.main_window.img.copy()
            self.show_pic([self.main_window.dirScreen], self.main_window.img_copy)



    # 向上选取图片
    def up_image(self):
        self.index += 1
        if self.index > len(self.dir_image_data) - 1:
            self.index = 0
        self.main_window.img = self.dir_image_data[self.index]
        self.main_window.img_copy = self.main_window.img.copy()
        self.show_pic([self.main_window.dirScreen], self.main_window.img_copy)

    def ok_image(self):
        self.show_pic([self.main_window.mainScreen], self.main_window.img_copy)

    # 向下选取图片
    def down_image(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.dir_image_data) - 1
        self.main_window.img = self.dir_image_data[self.index]
        self.main_window.img_copy = self.main_window.img.copy()
        self.show_pic([self.main_window.dirScreen], self.main_window.img_copy)

    # 图片预处理
    def image_process(self):
        if self.main_window.img_copy is None:
            self.addStringToTable("Error: 未选择图像")
            return
        # 如果用户已经进行了截图, 就对截图进行处理
        if self.main_window.image_cut is not None:
            self.main_window.img_copy = self.main_window.image_cut
        # method表示使用哪一种图像预处理方法
        method = self.main_window.imgprocesscomboBox.currentText()
        if self.main_window.img_copy is None:
            # print("warning:没有选择照片")
            self.addStringToTable("Error: 没有选择图像预处理对象")
            return
        if method == "复原":
            try:
                self.main_window.img_copy = self.main_window.img.copy()
            except:
                # print("Warning: 复原图片出现问题, 请重试")
                self.addStringToTable("Error: 复现图像有误, 请重试")
                return
        elif method == "灰度值处理":
            try:
                self.main_window.img_copy = IPM.process_grayscale(self.main_window.img_copy)
            except:
                # print("Warning: 已经进行了灰度处理")
                self.addStringToTable("Error: 当前图像格式无法进行灰度化")
                return
        elif method == "均值滤波":
            try:
                self.main_window.img_copy = IPM.mean_filter(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 均值滤波操作有误")
                return
        elif method == "高斯滤波":
            try:
                self.main_window.img_copy = IPM.gaussian_filter(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 高斯滤波操作有误")
                return
        elif method == "腐蚀":
            try:
                self.main_window.img_copy = IPM.erode_image(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 腐蚀操作有误")
                return
        elif method == "膨胀":
            try:
                self.main_window.img_copy = IPM.dilate_image(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 膨胀操作有误")
                return
        elif method == "开运算":
            try:
                self.main_window.img_copy = IPM.opening(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 开运算操作有误")
                return
        elif method == "闭运算":
            try:
                self.main_window.img_copy = IPM.closing(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 闭运算操作有误")
                return
        elif method == "RGB转BGR":
            try:
                self.main_window.img_copy = IPM.rgb_to_bgr(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 图像格式不为BGR格式, 请调整")
                return
        elif method == "BGR转HSV(需要先转化为BGR图像)":
            try:
                self.main_window.img_copy = IPM.bgr_to_hsv(self.main_window.img_copy)
            except:
                self.addStringToTable("Error: 图像格式不为BGR格式, 请调整")
                return
        elif method == "平移图像":
            self.ipw = IPW.Params_Window(IPM.translate)
            self.ipw.pushButton.clicked.connect(lambda: self.image_process_with_args(IPM.translate))
            return  # 为了防止运行以下图像展示代码

        elif method == "旋转图像":
            self.ipw = IPW.Params_Window(IPM.rotate)
            self.ipw.pushButton.clicked.connect(lambda: self.image_process_with_args(IPM.rotate))
            return

        elif method == "图像镜像":
            self.ipw = IPW.Params_Window(IPM.flip)
            self.ipw.pushButton.clicked.connect(lambda: self.image_process_with_args(IPM.flip))
            return

        elif method == "变为黑白图像":
            self.ipw = IPW.Params_Window(IPM.convert_text_to_black_sharpen_and_denoise_with_outline)
            self.ipw.pushButton.clicked.connect(
                lambda: self.image_process_with_args(IPM.convert_text_to_black_sharpen_and_denoise_with_outline))
            return
            # 表示图像为彩色
        if self.main_window.img_copy.ndim == 3:
            self.show_pic([self.main_window.imgprocessScreen], self.main_window.img_copy)
        else:            # 表示图像为灰色
            self.show_gray_pic([self.main_window.imgprocessScreen], self.main_window.img_copy)

        self.save_img()

    # 保存图片
    def save_img(self):
        if self.main_window.imgprocessSaveButton.isChecked():
            img_binary_data = self.convert_numpy_to_binary(self.main_window.img_copy)
            # 插入数据到数据库
            insert_query = f"INSERT INTO {self.worker.name}_data (image_name, image_data) VALUES (%s, %s)"
            cursor = self.db.cursor()
            try:
                # 执行sql语句
                cursor.execute(insert_query, (f'{time.time()}', img_binary_data))
                # 提交到数据库执行
                self.db.commit()
                cursor.close()
                self.addStringToTable("保存成功")
            except Exception as e:
                print(f"发生错误: {str(e)}")
                self.addStringToTable("保存失败")
                # 如果发生错误则回滚事务
                self.db.rollback()
                cursor.close()



    # 将NumPy数组转换为二进制数据
    def convert_numpy_to_binary(self, numpy_data:np.ndarray):
        binary_data = io.BytesIO()
        np.save(binary_data, numpy_data)
        binary_data.seek(0)  # 将文件指针移到开头
        return binary_data

    # 点击预览只会在小窗口中显示处理好图片, 如果想要在大窗口显示处理好的图片, 需要点击"确认"按钮
    def image_process_ok(self):
        if self.main_window.img_copy is None:
            self.addStringToTable("未选择图像")
            return
        if self.main_window.imgprocessScreen.pixmap():
            self.main_window.mainScreen.setPixmap(QPixmap.fromImage(self.qimg))
        else:
            self.addStringToTable("请先点击预览按钮")

    # 绑定有参数的图像预处理函数，在选择完参数后，点击后可以进行变换
    def image_process_with_args(self, function):
        self.main_window.imgprocessScreen.setScaledContents(True)
        # 创建参数字典, 用于之后的传参操作
        self.params_dict = {}
        # 获取用户输入的参数
        for i in range(len(self.ipw.params_list)):
            if self.ipw.lineEdit[i].text().isdigit():
                self.params_dict[self.ipw.params_list[i]] = eval(self.ipw.lineEdit[i].text())
            self.params_dict[self.ipw.params_list[i]] = self.ipw.lineEdit[i].text()

        try:
            self.main_window.img_copy = function(self.main_window.img_copy, **self.params_dict)  # 传入字典的方法
        except:  # 如果运行有误, 则说明用户输入的参数格式用问题
            # print("参数填入有误")
            self.addStringToTable("Error: 参数输入有误, 或超出正常参数范围")
            self.ipw.close()  # 关闭参数输入窗口
            return
        # 关闭参数窗口
        self.ipw.close()
        # 展现图像
        if self.main_window.img_copy.ndim == 3:
            self.show_pic([self.main_window.imgprocessScreen], self.main_window.img_copy)
            # 表示图像为灰色
        else:
            self.show_pic([self.main_window.imgprocessScreen], self.main_window.img_copy)
        if self.main_window.imgprocessSaveButton.clicked:
            self.save_img() # 保存图片文件至数据库





    # 切换主题
    def to_theme(self):
        self.main_window.stackedWidget_2.setCurrentIndex(0)

    # 切换到设置中的安全设置界面
    def to_security(self):
        self.main_window.stackedWidget_2.setCurrentIndex(2)

    # 常规设置
    def to_general(self):
        self.main_window.stackedWidget_2.setCurrentIndex(1)

    # 摄像头捕捉
    def video_catch(self):
        self.main_window.camLabel.shape = 'rect'

    def sql_check(self):
        cursor = self.db.cursor()
        if self.main_window.databaseButton.currentText() == "切换数据库":
            query = "SHOW TABLES"
            cursor.execute(query)
            tables = cursor.fetchall()
            for i in range(len(tables)):
                self.main_window.databaseButton.addItem("")
                self.main_window.databaseButton.setItemText(i+1,tables[i][0])
        else:
            table_name = self.main_window.databaseButton.currentText()
            sql3 = f"select * from {table_name}"
            sql4 = f"show columns from {table_name}"
            cursor.execute(sql3)

            self.data = cursor.fetchall()
            cursor.execute(sql4)
            columns = cursor.fetchall()
            self.columns_list = []
            data_row = len(self.data[0])
            self.main_window.logtableWidget.setColumnCount(data_row)
            self.main_window.logtableWidget.clear()
            for i in range(len(columns)):
                self.columns_list.append(columns[i][0])
            self.main_window.logtableWidget.setHorizontalHeaderLabels(self.columns_list)
            for row in range(len(self.data)):
                self.main_window.logtableWidget.insertRow(row)
                for col in range(len(self.data[row])):
                    item = QTableWidgetItem(str(self.data[row][col]))
                    self.main_window.logtableWidget.setItem(row,col, item)
            cursor.close()

    def sql_clear(self):
        self.main_window.logtableWidget.clear()

    def csv_file(self):
        csv_data = pd.DataFrame(columns = self.columns_list, index = None)
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                csv_data.loc[row,self.columns_list[col]] = self.data[row][col]
        csv_data.to_csv(f"./data/{time.time()}.csv", index=False)


    # 控件连接函数
    def connect(self):
        self.login_window.login_button.clicked.connect(self.log_in)  # 登录功能
        self.main_window.openImgButton.clicked.connect(self.open_image)  # 打开样例图片
        self.main_window.cutImgButton.clicked.connect(self.get_screen)  # 开启截图
        self.main_window.openDirButton.clicked.connect(self.open_dir)  # 打开文件夹

        self.main_window.openCamButton.clicked.connect(self.main_window.closeCam)
        self.main_window.dirupButton.clicked.connect(self.up_image)  # 向上选取图片
        self.main_window.dirdownButton.clicked.connect(self.down_image)  # 向下选取图片
        self.main_window.viewButton.clicked.connect(self.image_process)  # 图片预处理
        self.main_window.imgprocessokButton.clicked.connect(self.image_process_ok)  #
        self.main_window.dirokButton.clicked.connect(self.ok_image)
        # 注册界面
        self.login_window.nextButton.clicked.connect(self.create_WorkIdandName)
        self.login_window.nextButton_2.clicked.connect(self.create_BirthdayandSex)
        self.login_window.okButton.clicked.connect(self.create_UserandPassword)
        # 摄像头界面操作

        # 设置界面
        self.main_window.themeButton.clicked.connect(self.to_theme)
        self.main_window.safeButton.clicked.connect(self.to_security)
        self.main_window.generalButton.clicked.connect(self.to_general)
        self.main_window.roieditButton.clicked.connect(self.video_catch)
        # 模型识别样例图片
        # self.main_window.moudleokButton.clicked.connect(self.run_model)
        self.main_window.cleanButton.clicked.connect(self.sql_clear)
        self.main_window.loadButton.clicked.connect(self.csv_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_demo = Ocr_demo()
    sys.exit(app.exec_())
