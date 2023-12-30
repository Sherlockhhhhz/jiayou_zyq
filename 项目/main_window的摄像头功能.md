摄像头的连接到操作总共分为三步, 第一步创建一个摄像头类, 第二步用这个类连接已有的摄像头
第三步再是开启摄像头。

### 第一步: 创建摄像头类
```python
class MainWindow(QWidget):
    sendAddDeviceName = pyqtSignal()
    deviceList = MV_CC_DEVICE_INFO_LIST()
    g_bExit = False
    # ch:创建相机实例 | en:Creat Camera Object
    try:
        cam = MvCamera()
    except:
        cam = None
    try:
        ser = serial.Serial(
            port='COM2',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE
        )
    except:
        ser = None
```
MainWindow类中`__init__`初始化函数上面的是连接摄像头必要的变量(其中ser是连接报警, cam是摄像头的实例), 不需要理解其原理，知道就行
紧接着`cam = MvCamera()`是创造出一个实例的摄像头类, 我们可以通过对cam进行操作来控制摄像头。

### 第二步: 连接摄像头
```python
    def SelectDevice(self):
        '''
        选择所有能用的相机到列表中，
        gige相机需要配合 sdk 得到。
        '''
        # 得到相机列表
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, self.deviceList)
        if ret != 0:

                self.addStringToTable("enum devices fail! ret[0x%x]" % ret)
                # sys.exit()
        if self.deviceList.nDeviceNum == 0:

                self.addStringToTable("find no device!")
                # sys.exit()
            
    def connect_and_emit_sendAddDeviceName(self):
        # Connect the sendAddDeviceName signal to a slot.
        self.sendAddDeviceName.connect(self.SelectDevice)
        # Emit the signal.
        self.sendAddDeviceName.emit()
```
`connect_and_emit_sendAddDeviceName`和`SelectDevice`这两个函数是来检测附近有哪些摄像头可以连接, 然后连接检测到的第一个摄像头, 这部分代码不用也不会需要做任何修改。

### 第三步: 开启摄像头
```python
# 打开摄像头。
    def openCam(self, camid):
        self.hThreadHandle = []
        self.connect_and_emit_sendAddDeviceName()
        self.g_bExit = False
        # ch:选择设备并创建句柄 | en:Select device and create handle
        stDeviceList = cast(self.deviceList.pDeviceInfo[int(camid)], POINTER(MV_CC_DEVICE_INFO)).contents
        ret = self.cam.MV_CC_CreateHandle(stDeviceList)
        if ret != 0:
                self.addStringToTable("create handle fail! ret[0x%x]" % ret)
                sys.exit()
                # ch:打开设备 | en:Open device

        ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
                self.addStringToTable("open device fail! ret[0x%x]" % ret)
                sys.exit()

                # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
        if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
                nPacketSize = self.cam.MV_CC_GetOptimalPacketSize()
                if int(nPacketSize) > 0:
                        ret = self.cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                        if ret != 0:
                                self.addStringToTable("Warning: Set Packet Size fail! ret[0x%x]" % ret)
                else:
                        self.addStringToTable("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)

            # ch:设置触发模式为off | en:Set trigger mode as off
        ret = self.cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
                self.addStringToTable("set trigger mode fail! ret[0x%x]" % ret)
                sys.exit()
                # ch:获取数据包大小 | en:Get payload size
        stParam = MVCC_INTVALUE()
        memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))

        ret = self.cam.MV_CC_GetIntValue("PayloadSize", stParam)
        if ret != 0:
                self.addStringToTable("get payload size fail! ret[0x%x]" % ret)
                sys.exit()
        nPayloadSize = stParam.nCurValue



        # ch:开始取流 | en:Start grab image
        ret = self.cam.MV_CC_StartGrabbing()
        if ret != 0:
                self.addStringToTable("start grabbing fail! ret[0x%x]" % ret)
                sys.exit()

        data_buf = (c_ubyte * nPayloadSize)()


        try:
            hThreadHandle1 = threading.Thread(target=self.work_thread, args=(self.cam, data_buf, nPayloadSize))
            hThreadHandle1.start()

        except Exception as e:
            self.addStringToTable(str(Exception))
```
这三步的所有代码完全不用进行任何修改, 你可以当成固定模板, 要连接摄像头就这么写就行了, 这部分是不会出现问题的。需要记住的是我们通过摄像头捕获到的图片数据在`openCam`函数中倒数第四行, 第三行`hThreadHandle1 = threading.Thread(target=self.work_thread, args=(self.cam, data_buf, nPayloadSize))
            hThreadHandle1.start()`thread是线程的意思, 这段代码就是开启一个叫做work_thread的线程, 我们的所有图片数据就在work_thread这个线程中, 注意这两行也是固定的python使用线程的模板, 首先使用`threading.Thread`创建一个线程, 其中有两个参数, 一个是target你要运行的函数, 另外一个是args你要运行这个函数的参数, 其中需要注意的是, 参数你要放在元组里传进去, 可以看到这里就有三个参数`(self.cam, data_buf, nPayloadSize)`
紧接着我们来看看work_thread这个函数/线程, 这也是摄像头部分我们唯一需要做修改的函数。

```python
    def work_thread(self, cam=0, pData=0, nDataSize=0):
        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))

        while True:
                QIm = np.asarray(pData)  # 将c_ubyte_Array转化成ndarray得到（3686400，）
                # print(QIm.shape)
                QIm = QIm.reshape((1080, 1440, -1))  # 根据自己分辨率进行转化
                # QIm = cv2.cvtColor(QIm, cv2.COLOR_GRAY2RGB)  # 这一步获取到的颜色不对，因为默认是BRG，要转化成RGB，颜色才正常
                # QIm = cv2.cvtColor(QIm, cv2.COLOR_BGR2RGB)
                if self.detect_model is not None:
                        torch.cuda.empty_cache()  # 停止自动计算梯度
                        torch.set_grad_enabled(False)  # 释放CUDA缓存
                        result, names = self.detect_model.detect1([QIm])
                        QIm = result[0][0]

                pyrD1 = cv2.pyrDown(QIm)  # 向下取样
                pyrD2 = cv2.pyrDown(pyrD1, borderType=cv2.BORDER_DEFAULT)  # 向下取样
                image_height, image_width, image_depth = pyrD2.shape  # 读取图像高宽深度
                pyrD3 = QImage(pyrD2, image_width, image_height, image_width * image_depth, QImage.Format_RGB888)
                self.camLabel.setScaledContents(True)
                self.camLabel.setPixmap(QPixmap.fromImage(pyrD3))
                if self.text_model is not None:
                    # result = self.text_model.ocr(pyrD2, cls=True)
                    # if result == [None]:
                    #     self.addStringToTable("None")
                    # else:
                    #     text_res = []
                    #     for line in result:
                    #         for text in line:
                    #             t = text[-1][0]
                    #             text_res.append(t)
                    #     res = ' '.join(text_res)
                    #     self.addStringToTable(res)
                    try:
                        self.hThreadHandle.append(threading.Thread(target=self.text_thread, args=([pyrD2])))
                        self.hThreadHandle[-1].start()
                        self.hThreadHandle.pop(0)

                    except Exception as e:
                        self.addStringToTable(str(Exception))

                ret = cam.MV_CC_GetOneFrameTimeout(pData, nDataSize, stFrameInfo, 1000)
                if ret == 0:
                    if self.checkBox.checkState() == 2 and self.detect_model is not None:
                        pyrD1 = cv2.pyrDown(QIm)  # 向下取样
                        pyrD2 = cv2.pyrDown(pyrD1, borderType=cv2.BORDER_DEFAULT)  # 向下取样
                        image_height, image_width, image_depth = pyrD2.shape  # 读取图像高宽深度
                        pyrD3 = QImage(pyrD2, image_width, image_height, image_width * image_depth,
                                       QImage.Format_RGB888)
                        self.camLabel.setScaledContents(True)
                        self.camLabel.setPixmap(QPixmap.fromImage(pyrD3))
                    if self.checkBox.checkState() == 2 and self.checkSaveBox.checkState() == 2:
                        image = Image.fromarray(pyrD2)
                        # 获取当前时间并直接格式化为字符串
                        formatted_date_time = time.strftime('%Y-%m-%d %H-%M-%S')
                        res_path = os.path.join("../log",
                                                f"Image_{formatted_date_time}.jpg")
                        image.save(res_path)
                        self.addStringToTable(f'{res_path}已保存')
                    else:
                        pass
                    if self.detect_model is not None and self.checkWarnBox.checkState() == 2: # 如果yolo模型打开并且警报功能勾选了
                            if self.ser.isOpen() and names == []:
                                self.warn()
                                self.addStringToTable("Warning: Detect Nothing !")
                else:
                        self.addStringToTable("no data[0x%x]" % ret)
                if self.g_bExit == True:
                        del pData
                        break
        # 获得所有相机的列表存入cmbSelectDevice中
```
这个函数只需要知道两个部分就行, 第一个在函数的第三行, 可以看到它是一个无限循环, 也就是说这个线程它会不停地运行下去获得捕获到的图像数据。第二个就是注意这个`QIm`(紧接着无限循环), 从名字我们不难看出它就是我们捕获到的图像数据, 我们可以看到(先忽略`if self.detect_model和if self.text_model is not None`这个条件语句, 后面再做解释),我们可以看到这个函数对QIm进行了一些处理, 比如向下采样之类的,
再通过`self.camlabel.setPixmap(QPixmap.fromImage(pyrD3)`这行代码, 我们可以清楚的知道pyrD3就是我们最终处理好的图片数据, 并展现在camlabel这个控件上。摄像头开启代码就需要知道这么多, 要变化我们看到的图片就更改QIm这个变量就行。

### 4. 关闭摄像头
```python

 # 关闭相机
    def closeCam(self):
        if self.deviceList.nDeviceNum == 0:
            self.addStringToTable("Error: The Cam not connect")
            return
        self.g_bExit = True
        # ch:停止取流 | en:Stop grab image
        ret = self.cam.MV_CC_StopGrabbing()
        if ret != 0:
                self.addStringToTable("stop grabbing fail! ret[0x%x]" % ret)
                sys.exit()

        # ch:关闭设备 | Close device
        ret = self.cam.MV_CC_CloseDevice()
        if ret != 0:
                self.addStringToTable("close deivce fail! ret[0x%x]" % ret)

        # ch:销毁句柄 | Destroy handle
        ret = self.cam.MV_CC_DestroyHandle()
        if ret != 0:
                self.addStringToTable("destroy handle fail! ret[0x%x]" % ret)

```
这段代码是关闭摄像头, 运行这个函数摄像头就会关闭, 这段代码也不需要做任何修改, 直接绑定控件调用就行。

### 5. 模型识别
```python
    def set_yolov7_on_off(self):
        if self.yolo_model_tone.checkState() == 0:
            self.detect_model = None
        else:
            try:
                self.detect_model = detect_with_API.detectapi(
                    weights='..\\yolov7\\models\\yolov7.pt')
            except Exception as e:
                self.addStringToTable(str(e))

    def set_text_on_off(self):
        if self.text_model_tone.checkState() == 0:
            self.text_model = None
        else:
            self.text_model = PaddleOCR(use_angle_cls=True, lang="ch")
            paddle.fluid.dygraph.cleanup()
            
            
----以下截取自work_thread
    if self.detect_model is not None:
                        torch.cuda.empty_cache()  # 停止自动计算梯度
                        torch.set_grad_enabled(False)  # 释放CUDA缓存
                        result, names = self.detect_model.detect1([QIm])
                        QIm = result[0][0]

                pyrD1 = cv2.pyrDown(QIm)  # 向下取样
                pyrD2 = cv2.pyrDown(pyrD1, borderType=cv2.BORDER_DEFAULT)  # 向下取样
                image_height, image_width, image_depth = pyrD2.shape  # 读取图像高宽深度
                pyrD3 = QImage(pyrD2, image_width, image_height, image_width * image_depth, QImage.Format_RGB888)
                self.camLabel.setScaledContents(True)
                self.camLabel.setPixmap(QPixmap.fromImage(pyrD3))
                if self.text_model is not None:
                    # result = self.text_model.ocr(pyrD2, cls=True)
                    # if result == [None]:
                    #     self.addStringToTable("None")
                    # else:
                    #     text_res = []
                    #     for line in result:
                    #         for text in line:
                    #             t = text[-1][0]
                    #             text_res.append(t)
                    #     res = ' '.join(text_res)
                    #     self.addStringToTable(res)
                    try:
                        self.hThreadHandle.append(threading.Thread(target=self.text_thread, args=([pyrD2])))
                        self.hThreadHandle[-1].start()
                        self.hThreadHandle.pop(0)
```
首先看上面两个函数`set_yolov7_on_off`, `set_text_on_off`, 他们分别是创建和删除(将它们的值改为None)self.detect_model和self.text_model，这两个是我们的目标检测模型和字符识别模型, 知道这些就够了。然后继续看下面的代码,我们可以知道, 因为work_thread是一个线程, 它会单独地无限循环下去, 直到我们关闭摄像头, 然后如果我们在它循环的过程中, 运行了`set_yolov7_on_off`函数
, 我们会有一个self.detect_model的变量, 他不为None, 紧接着它就会运行if条件句下面的代码, 对我们的QIm这个图片数据进行目标检测, 然后返回结果result, 然后我们对result进行索引, 就可以获得我们新的有识别结果带框的QIm了, 之后在展示巴拉巴拉的。后面的text_model一个道理。
