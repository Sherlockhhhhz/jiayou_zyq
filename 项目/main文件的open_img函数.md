```python
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

```
```python
1. file_dialog = QFileDialog()
```
这里是初始化一个文件选择窗口, 这里跟我们在main文件自己写的self.login_window = LoginWindow()一样，LoginWindow初始化自带self.show()，所以我们只要初始化窗口就会自动show出来, 这里的QFileDialog也是只要初始化, 就会自动show出来。

```python
2.file_dialog.setNameFilter("(*.png *.jpg *bmp *.svg)") 
 ```
 因为如果把所有的文件都显示出来, 会很多, 而我们只需要图片格式的文件, 所以我们可以用QFileFialog类自带的setNameFilter函数, 规定我们只显示什么样格式的图片, 此处我们规定只显示.png, .jpg, .bmp, .svg这四种图片格式, 如下图右下角

<img src="../img/11.png"></img>


```python

if file_dialog.exec_():
            try:
                self.image_path = file_dialog.selectedFiles()[0]  # 获取选取图片的路径
                self.main_window.img = cv2.imread(self.image_path)
                self.main_window.img_copy = self.main_window.img.copy()  # 思考一下为什么需要self.main_window.img_copy
                self.show_pic([self.main_window.mainScreen], self.main_window.img_copy)
```
`if file_dialog.exec_()`file_dialog.exec_()函数会在文件选择窗口关闭之后, 返回True, 因为我们选择完文件之后, 文件选择窗口就没用了, 我们会把它关闭。程序怎么知道我们选择好图片了呢，它可以通过判断窗口是否关闭，所以只要exec_()函数返回True, 它就知道我们已经选择好图片，开始运行下面的代码。

`file_dialog.selectedFiles()`函数会返回一个列表, 列表里面的第一个值就是我们所选择图片文件的路径

接着用cv2.imread函数通过文件路径读取出图像的numpy数据, 赋值给img, 然后调用copy()函数生成一个副本赋值给img_copy, 最后再用show_pic(我们自己写的, 详情请看[show_pic]("./main文件的show_pic函数.md"))