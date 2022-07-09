import numpy as np
import cv2
import matplotlib.pyplot as plt
#numpy实现傅里叶变换
img = cv2.imread("C:/Users/spike/Desktop/picture/2.jpg",0)

f = np.fft.fft2(img)

fshift = np.fft.fftshift(f)

magnitude_spectrum = 20*np.log(np.abs(fshift))

#opencv实现傅里叶变换
img1 = cv2.imread("C:/Users/spike/Desktop/picture/1.jpg",0)

dft = cv2.dft(np.float32(img1),flags=cv2.DFT_COMPLEX_OUTPUT)

dftshift = np.fft.fftshift(dft)

magnitude_spectrum1 = 20*np.log(cv2.magnitude(dftshift[:,:,0],dftshift[:,:,1]))

#显示图像
plt.subplot(221),plt.imshow(img,cmap="gray"),plt.title("original1"),plt.axis("off")
plt.subplot(222),plt.imshow(magnitude_spectrum,cmap="gray"),plt.title("result1"),plt.axis("off")
plt.subplot(223),plt.imshow(img1,cmap="gray"),plt.title("original2"),plt.axis("off")
plt.subplot(224),plt.imshow(magnitude_spectrum1,cmap="gray"),plt.title("result2"),plt.axis("off")
plt.show()

#逆傅里叶变换
ifshift = np.fft.ifftshift(fshift)
iimg = np.fft.ifft2(ifshift)
iimg = np.abs(iimg)

ishift = np.fft.ifftshift(dftshift)
ilmg = cv2.idft(ishift)
ilmg = cv2.magnitude(ilmg[:,:,0],ilmg[:,:,1])
plt.subplot(121),plt.imshow(iimg,cmap="gray"),plt.title("original"),plt.axis("off")
plt.subplot(122),plt.imshow(ilmg,cmap="gray"),plt.title("result"),plt.axis("off")
plt.show()


