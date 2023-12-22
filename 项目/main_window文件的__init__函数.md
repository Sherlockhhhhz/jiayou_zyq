```python
main_window.py
    def __init__(self):
        super(MainWindow, self).__init__()
        self.img = None
        self.img_copy = None
        self.image_cut = None
        self.frame = None
        self.detect_model = None
        self.text_model = None
        self.setupUi()
        # self.show()
        self.connect()

```

```python
1. super(MainWindow, self).__init__()
```
用于使MainWindow继承QWudget的功能(如self.show(), self.close()等)🦌

```python
    self.img = None
    self.img_copy = None
    self.image_cut = None
    self.frame = None
    self.detect_model = None
    self.text_model = None
```
2. `self.img`指的是我们点击选择图片按钮后的所选图片的原始数据, 此处是为了实现复原的操作。🎄🎄🎄

3. `self.img_copy`指的是我们对原始图片数据的副本, 此变量的作用是代替对原始图像进行操作(如数字图像处理，模型识别等), 为了保证原始图像不被改变。💐💐💐

4. `self.frame`和`self.cut_img`暂时没用, 可以忽略🎁🎁🎁

5. `self.detect_model`指的是我们的yolo识别模型🎅🎅🎅

6. `self.text_model`指的是我们的文字识别模型🎶🎶🎶