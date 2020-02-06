import astropy.io.fits as fits
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import ndimage


def mean(data):
    new_data = np.mean(data, axis=0)
    plt.imsave('mean.png', new_data, cmap='gray')


def fourier_transform(data):
    sum = 0
    for i in range(len(data)):
        sum += np.abs(np.fft.fft2(data[i]))**2
    result1 = np.abs(np.fft.fftshift(sum))
    plt.imsave('fourier.png', result1, vmax=100000000000, cmap='gray')

    return result1


def fourier_rotate(data):
    k, result2 = 0, 0
    for i in range(1, 100):
        k += 1
        alpha = 3.6*k
        s = np.abs(np.fft.fft2(data[i])) ** 2
        m = np.abs(np.fft.fftshift(s))
        result2 += ndimage.rotate(m, alpha, reshape=False)
    plt.imsave('rotaver.png', result2, vmax=100000000000, cmap='gray')

    return result2


def frequency(result1, result2):
    new_data = result1/result2
    r = 45
    for i in range(len(result1)):
        for j in range(len(result2)):
            if  np.abs((i - 100)**2 + (j-100)**2) > r**2:
                new_data[i][j] = 0

    inverse_fourier = np.abs(np.fft.ifft2(new_data))
    inverse_fourier = np.abs(np.fft.ifftshift(inverse_fourier))
    plt.imsave('binary.png', inverse_fourier, cmap='gray')


data = fits.open('speckledata.fits')[2].data

mean(data)

result1 = fourier_transform(data)
result2 = fourier_rotate(data)

frequency(result1, result2)
