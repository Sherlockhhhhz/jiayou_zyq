我们在应用界面的下部做了一个输出端

<img src="../img/222.bmp"></img>

当应用报错会识别出来的信息会打印在"终端"上, 这个打印的代码就需要我们来写。首先我们这个终端用的控件是TableWidget, 如名字一样, 它其实就是一个table, 像数据库的表一样, 这个table可以有很多列很多行, 但我们每次只输出一个信息, 像上图一样, 所以我们的table=需要一列, 可以看到下面代码的第2行, setColumnCount函数(set是设置的意思, Column是列的意思, Count是数量的意思), 所以不能看出setColumnCount(1)是用来将我们的table设置为1列。

```python
# 获取表格的行数
        1. rowPosition = self.main_window.tableWidget.rowCount()

        # 插入新的行
        2. self.main_window.tableWidget.setColumnCount(1)
        3. self.main_window.tableWidget.setRowCount(rowPosition + 1)
        4. print(text)
        # 在新行的第一列中添加表格项

        5. self.main_window.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(text))
        6. self.main_window.tableWidget.setColumnWidth(0, 800)
```
如上图我们可以看到, 我们的输出端有很多行的输出, 由于TableWidget只有setItem函数可以往表里添加信息, 它需要传入你向插入哪一列, 哪一行, 以及什么数据(都是从0开始)。列肯定是第一列, 所以是0, 至于行我们可以通过tableWidget类所带的rowCount函数返回现在表里所含有的行数, 而我们想要输出的文字需要先被QTableWidgetItem()转换为TableWidget的格式才能添加(上网查到的, 必须要转化要不然会报错)。而最后一行的setColumnWidth则是设置第几列的宽度是多少, 此时我们设置第一列的宽度为800, 具体可以看运行的结果来更改。