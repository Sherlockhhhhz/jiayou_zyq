```python
main.py
# 图片像展示
    def show_pic(self, dis, img_source):
        height, width, _ = img_source.shape
        bytesPerline = 3 * width
        self.qimg = QImage(img_source.data, width, height, bytesPerline,
                               QImage.Format_RGB888).rgbSwapped()

        for d in dis:
            d.setScaledContents(True)

            d.setPixmap(QPixmap.fromImage(self.qimg))
```
参数: 
1. `dis`: 将图像展现的控件🕯
2. `img_source`: 所要展现的图像    🕯

此函数的作用是将img_source图像(只支持彩色图像)展现在dis控件上🕯

使用方法:
```python
self.show_pic([self.main_window.mainScreen], self.main_window.img_copy)
```
此处就是将self.main_window.img_copy图像展现在self.main_window.mainScreen上🕯

内部原理:
```python
height, width, _ = img_source.shape # 获取图像的高度和宽度, 其中_表示通道数量(彩色图像的通道数量为3), 但我们不需要通道数量, 所以用_来代替📽️
bytesPerline = 3 * width # 转换为QImage所需的一个参数, 不需要理解什么意思, 我也不知道📽️
```
因为PyQt控件不能防止numpy数据类型的图片, 需要先转换成QImage类型
```python
self.qimg = QImage(img_source.data, width, height, bytesPerline,
                               QImage.Format_RGB888).rgbSwapped() # 只要你是彩色图片, 这一部分是通用的, 里面的参数也是固定的📽️
```
```python
for d in dis:
            d.setScaledContents(True)

            d.setPixmap(QPixmap.fromImage(self.qimg))

```
因为有时候, 我们需要把图片放在多个控件上面, 所以这里的`dis`就是你要存放控件的列表, 例如我要将图片放在mainScreen和camLabel上, 这里的dis=[mainScreen, camLabel], 我们会通过for循环依次遍历每个控件, 来放置图片。🎮

`d.setScaledContents(True)`这行代码的作用是使图片所展现的大小跟我们的控件一样

```python
# 灰色图像展示
    def show_gray_pic(self,dis,img_source):
        height, width = img_source.shape
        self.qimg = QImage(img_source.data, width, height,
                           QImage.Format_Grayscale8)

        for d in dis:
            d.setScaledContents(True)
            d.setPixmap(QPixmap.fromImage(self.qimg))

```
这里的show_gray_pic方法跟show_pic一个原理, 就只是替换了QImage的最后一个参数。