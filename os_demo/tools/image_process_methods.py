import cv2
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw

# 灰度处理
def process_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

# RGB图像转BGR图像
def rgb_to_bgr(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 平移图像
def translate(image, x, y):

    (h, w) = image.shape[:2]
    M = np.float32([[1, 0, x], [0, 1, y]]) # 平移矩阵
    # 使用Opencv放射变换函数实现平移操作
    shifted = cv2.warpAffine(image, M, (w, h))
    print(1)
    return shifted

# 旋转图片
def rotate(image, angle, center = None, scale = 0.7):
    # 获取图像尺寸
    (h, w) = image.shape[:2]
    # 旋转中心的缺失值为图像中心
    if center is None:
        center = (w / 2, h / 2)
        # 调用计算旋转矩阵函数
    M = cv2.getRotationMatrix2D(center, angle, scale)
    # 使用opencv放射函数进行旋转操作
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

# 图像镜像
def flip(image, direction):
    return cv2.flip(image, direction)

# 图像灰度变化
def linear_trans(image, k, b = 0):
    # 计算灰度线性变化的映射表
    trans_list = [(np.float(x) * k + b) for x in range(256)]
    # 将列表转化为np.array
    trans_table = np.array(trans_list)
    # 将会度值超过[0, 245]的范围进行数值调整
    trans_table[trans_table > 255] = 255
    trans_table[trans_table < 0] = 0
    trans_table = np.round(trans_table).astype(np.uint8)
    return cv2.LUT(image, trans_table)

# 图像锐化
def filter2D(image, sharpen):
    return cv2.filter2D(image, -1, sharpen)

# 把BGR图像转化为HSV图像, 需要先将图片转化为
def bgr_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# 均值滤波
def mean_filter(image):
    blurred_image = cv2.blur(image, (3, 3))
    return blurred_image

#高斯滤波
def gaussian_filter(image):
    blurred_image = cv2.GaussianBlur(image, (3,3), 2)
    return blurred_image

#腐蚀
def erode_image(image):
    kernel = np.ones((3,3), np.uint8)
    eroded_image = cv2.erode(image, kernel, iterations=1)
    return eroded_image

#膨胀
def dilate_image(image):
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(image, kernel, iterations=1)
    return dilated_image
#开运算
def opening(image):
    kernel = np.ones((3,3), np.uint8)
    opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opened_image
#闭运算
def closing(image):
    kernel = np.ones((3, 3), np.uint8)
    closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closed_image


# 将字体变为黑色并应用锐化和去噪，添加黑色文字描边
def convert_text_to_black_sharpen_and_denoise_with_outline(image, th=225):
    # 反转图像
    inverted_image = cv2.bitwise_not(image)
    # 将图像转换为灰度图像
    img_data = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)
    img_data[img_data < th] = 0
    img_data[img_data >= th] = 255  # 将大于等于阈值的像素设为0（黑色）

    new_img = Image.fromarray(img_data)

    # 增强对比度
    enhancer = ImageEnhance.Contrast(new_img)
    enhanced_img = enhancer.enhance(2.5)  # 增强对比度的程度，可以根据需要调整

    # 应用图像锐化（使用增强对比度后的图像进行锐化）
    enhanced_img = enhanced_img.filter(ImageFilter.SHARPEN)

    # 去噪处理（使用中值滤波器）
    denoised_img = enhanced_img.filter(ImageFilter.MedianFilter(size=3))

    # 创建一个绘图对象，添加文字描边
    draw = ImageDraw.Draw(denoised_img)
    outline_width = 1  # 描边宽度
    for i in range(-outline_width, outline_width + 1):
        for j in range(-outline_width, outline_width + 1):
            if i != 0 or j != 0:
                draw.text((i, j), " ", fill=0)  # 使用整数 0 表示黑色描边

    return np.array(denoised_img)
    # denoised_img.save("converted_result.jpg")

#二值化图像
def Binarization(image,threshold_value = 200):
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_image

#逆二值化图像
def Inverse_binarization(image,threshold_value = 28):
    _, inverted_binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)
    return inverted_binary_image





