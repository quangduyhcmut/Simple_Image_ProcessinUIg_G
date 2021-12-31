import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def avg_filter(img,size):
    kernel = np.ones((size,size),np.float32)
    kernel = kernel / (size**2)
    img_avg = cv2.filter2D(img,-1,kernel)
    cv2.imwrite("output/avg_result.jpg",img_avg)
    return img_avg

def weighted_avg_filter(img,b):
    kernel = np.array([[1,b,1],[b,b*b,b],[1,b,1]],dtype= float) 
    kernel /=  (b+2)*(b+2)
    print(kernel)
    result = cv2.filter2D(img, -1, kernel)      
    cv2.imwrite("output/wavg_result.jpg",result)
    return result

def gaussian_filter(img,size,sigma):
    # k = size // 2
    # x, y = np.mgrid[-k:k+1, -k:k+1]
    # normal = 1 / (2.0 * np.pi * sigma**2)
    # kernel =  np.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
    # print(kernel)
    # result = cv2.filter2D(img,-1,kernel)
    result = cv2.GaussianBlur(img,(size,size),0)
    cv2.imwrite("output/gauss_result.jpg",result)
    return result

def median_filter(img,size):
    denoise_img = cv2.medianBlur(img,size)
    cv2.imwrite("output/median_result.jpg",denoise_img)
    return denoise_img

def laplacian_filter(img,size):
    result = cv2.Laplacian(img,cv2.CV_8U, None, size)
    cv2.imwrite("output/laplace_result.jpg",result)
    return result

def gab_filter(img,size,lamda=10,theta=1,phi=0,sigma=5,gamma=1):
    kernel = cv2.getGaborKernel((size,size), sigma, theta, lamda, gamma, phi, cv2.CV_32F)
    kernel /= math.sqrt((kernel * kernel).sum())
    filtered = cv2.filter2D(img, -1, kernel)
    cv2.imwrite("output/gabor_result.jpg",filtered)
    return filtered

def sob_filter(img,ksize):
    ddepth = cv2.CV_16S 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    # grad_y = cv.Scharr(gray,ddepth,0,1)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    print(ksize)
    cv2.imwrite("output/sobel_result.jpg",grad)
    return grad

def pre_filter(img):
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    img_prewittx = cv2.filter2D(img, -1, kernelx)
    img_prewitty = cv2.filter2D(img, -1, kernely)
    result = img_prewittx + img_prewitty
    cv2.imwrite("output/prewitt_result_gray.jpg",result)
    return result


def arguments_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='', required=False, help='Path to image')
    parser.add_argument('-f', '--function', choices=['average', 'w_average', 'gaussian', 'median', 'laplacian', 'gabor', 'sobel', 'prewitt'], required=True, help='Chosse filter function')
    return parser.parse_args()

def main():
    args = arguments_parser()
    img = cv2.imread(args.path,1)
    cv2.imshow("img",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

    





