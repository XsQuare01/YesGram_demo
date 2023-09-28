import cv2
import sys
import numpy as np
import matplotlib.pylab as plt
import json
from enum import Enum

class Threshold(Enum):
    OTSU=1
    AVERAGE=2
    GAUSSIAN=3

class ImagePreprocessing:
    def __init__(self, src) -> None:
        self.src = src

    # 이미지를 size로 축소하는 함수
    def modifyImageSize(_src, width = 100, height = 100):
        _src = cv2.resize(_src, (width, height))
        return _src
    
        # # 이미지 크기
        # if(gray):
        #     h, w = _src.shape
        # else:
        #     h, w, c = _src.shape

        # 이미지 비율로 자르기
        # if(h > w):
        #     _src = cv2.resize(_src, ((int)(size * w / h), size))
        # else:
        #     _src = cv2.resize(_src, (size, (int)(size * h / w)))
        
    
    # # 이미지를 원래 크기로 복원하는 함수
    # def increaseImageSize(src, h, w):
    #     src = cv2.resize(src, dsize = (w, h), interpolation=cv2.INTER_CUBIC)

    #     return src
    def minMaxStretching(src):
        # 0과 1로 정규화하고 255를 곱해 Stretching함
        src = cv2.normalize(src, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        src = (255*src).astype(np.uint8)

        return src

    def CLAHE(src, clip = 3.0, tsize = 8):
        # src = cv2.cvtColor(src, cv2.COLOR_RGB2HSV)
        
        dst = src.copy()
        
        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tsize, tsize))
        # dst[:, :, 0] = clahe.apply(dst[:, :, 0])
        dst = clahe.apply(dst)

        # dst = clahe.apply(src)
        # dst = cv2.cvtColor(dst, cv2.COLOR_HSV2RGB)

        return dst

    def HE(src):
        dst = src.copy()
        dst= cv2.equalizeHist(src)
        return dst

class ImageVisualization:
    def __init__(self) -> None:
        pass

    # 히스토그램 출력 함수
    def printHist(_src):
        hist = cv2.calcHist([_src], [0], None, [256], [0, 256])
        plt.plot(hist)

    # 0과 1의 비율을 출력하는 함수
    def printPercentage(_src):
        _src = _src.ravel()
        count_0 = 0
        count_1 = 0
        for i in range(0, _src.size):
            if(_src[i] == 0):
                count_0 += 1
            elif(_src[i] == 255):
                count_1 += 1
        
        
        p = count_0 / (count_0 + count_1)

        print("0: ", count_0)
        print("1: ", count_1)
        print("Percentage: ", count_0 / (count_0 + count_1) * 100 ,"%")

        return p
    
    #src1: input image, src2: result image
    def printAverage(_src1, _src2):
        r_src1 = _src1.ravel()
        r_src2 = _Src2.ravel()
        
        black_cnt = 0
        white_cnt = 0
        
        black_sum = 0
        white_sum = 0
        
        for i in range(0, r_src1,size):
            # Black
            if(r_src2[i] == 0):
                black_cnt+= 1
                black_sum+= r_src1[i]
            elif(r_src2[i] == 1):
                white_cnt+= 1
                white_sum+= r_src1[i]
                
        black_aver = (black_sum/black_cnt)
        while_aver = (white_sum/white_cnt)
        
        return black_aver, while_aver
        
    
    # src1: input image, src2: result image
    def printMatchRate(_src1, _src2):
        r_src1 = _src1.ravel()
        r_src2 = _src2.ravel()
        
        total = 0
        cnt = 0
        for i in range(0, r_src1.size):
            if(r_src2[i] == 0):
                total += 1
                if(r_src1[i] == r_src2[i]):
                    cnt += 1
        
        p = round((cnt / total) * 100, 2)
        
        print(f"Edge match rate: {p}%")
        return p

    
    # 2개의 이미지와 히스토그램 출력 함수
    def print2ImageNHist(_src1, name1, _src2, name2):
        _src1, h, w = ImagePreprocessing.modifyImageSize(_src1)
        _src2, h, w = ImagePreprocessing.modifyImageSize(_src2)

        res = {name1 : _src1, name2 : _src2}
        for i , (key, value) in enumerate(res.items()):
            plt.subplot(221 + i)
            plt.title(key)
            plt.imshow(value, cmap= 'gray')
            plt.xticks([]);plt.yticks([]) 
        
        plt.subplot(223)    
        ImageVisualization.printHist(_src1)

        plt.subplot(224)    
        ImageVisualization.printHist(_src2)

        plt.show()
    
    # 3개의 이미지와 1번 이미지의 히스토그램 출력 함수
    def print3Srcs(name1, _src1, name2, _src2, name3, _src3, width = 100, height = 100, Hist_num = True, otsu_t = 0):
        _src1 = ImagePreprocessing.modifyImageSize(_src1, width, height)
        _src1 = cv2.cvtColor(_src1, cv2.COLOR_RGB2GRAY)

        res = {name1 : _src1, name2 : _src2, name3: _src3}
        for i , (key, value) in enumerate(res.items()):
            plt.subplot(221 + i)
            plt.title(key)
            plt.imshow(value, cmap= 'gray')
            plt.xticks([]);plt.yticks([]) 
        
        if(Hist_num):
            plt.subplot(224)
            plt.text(otsu_t, 0,
                    '|',
                    color = 'r',
                    horizontalalignment = 'center',
                    verticalalignment = 'top')
            
            ImageVisualization.printHist(_src1)
        plt.show()
    
    
    # 처리한 이미지 비교 UI - Edge Detection
    def print4Srcs(name1, _src1, name2, _src2, name3, _src3, name4, _src4):
        res = {name1 : _src1, name2 : _src2, name3: _src3, name4: _src4}
        for i , (key, value) in enumerate(res.items()):
            plt.subplot(221 + i)
            plt.title(key)
            plt.imshow(value, cmap= 'gray')
            plt.xticks([]);plt.yticks([]) 
                        
        plt.show()


class ImageOutputProcessor:
    # 흰색(255)값을 1로 변경하는 함수
    def imageOutput(src, path):
        dst = src.astype(float) / 255
        if(path is not None):
            np.savetxt(path, dst, fmt='%d', delimiter=',')
            
        return dst.tolist()

class ImagePostprocessing:
    # 이미지를 반전하는 함수(검은색 -> 흰색)
    def imageReverse(src):
        dst = cv2.bitwise_not(src)
        return dst   

class ImageSegmentation:
    def __init__(self, src) -> None:
        self.src = src

    # K-Means Clustering
    def KMeansClustering(_src, median = False, gaussian = False, ksize = 3, sigma = 1, closing = False, width= 100, height=100):
        # Median Blur
        if(median):
            src = cv2.medianBlur(_src, ksize=3)
        elif(gaussian):
            src = cv2.GaussianBlur(_src, (ksize, ksize), sigma)

        _src = ImageSegmentation.modifyImageSize(_src, width, height)

        _src = cv2.cvtColor(_src, cv2.COLOR_GRAY2BGR)


        # 이미지의 행렬 변환. RGB 타입이라 가정하고 3 대입함
        data = _src.reshape((-1, 3)).astype(np.float32)

        # 최대 10번 반복하고, 1 pixel 이하로 움직이면 종료
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        # k는 2로 고정
        k = 2

        # k means clustering
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, 
                                            cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)

        dst = center[label.flatten()]

        # 입력 영상 형태로 변환
        dst = dst.reshape((_src.shape))

        # Closing
        if(closing):
            kernel = np.ones((3, 3), np.uint8)
            dst = cv2.erode(dst, kernel, iterations=1)
            dst = cv2.dilate(dst, kernel, iterations=1)

        return _src, dst

    # Ostu's Method
    def otsuMethod(_src, dist = 5, sigma = 100, clahe = False, width = 100, height = 100):
        _src = cv2.bilateralFilter(_src, dist, sigma, sigma)
            
        if(clahe):
            _src = ImagePreprocessing.CLAHE(_src)

        _src= ImagePreprocessing.modifyImageSize(_src, width, height)
        # _src = cv2.cvtColor(_src, cv2.COLOR_RGB2GRAY)

        t, res = cv2.threshold(_src, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        print('otsu threshold: ', t)

        return t, res

    # blk_size: 이미지를 몇등분 하는가? (n x n)
    # C: threshold 값에서 가감할 상수
    def adaptiveThreshold(_src, blk_size = 7, C = 4, dist = 3, sigma = 10, closing = False, width = 100, height = 100):
        h, w = _src.shape

        if(closing):
            if(h>= 1000 and w >= 1000):
                _src= ImagePreprocessing.modifyImageSize(_src, (int)(w/2), (int)(h/2))

                w_rat = ((int)(w/2) / width)
                if(w_rat % 2 == 0):
                    w_rat -= 1
                
            elif(h >= 500 and w >= 500):
                _src= ImagePreprocessing.modifyImageSize(_src, (int)(w*1.2), (int)(h*1.2))

                w_rat = ((int)(w*1.2) / width)
                if(w_rat % 2 == 0):
                    w_rat -= 1
            else:
                # 중간값으로 설정
                # h_mid = (int)((h + height) / 2)
                # w_mid = (int)((w + width) / 2)
                
                _src = ImagePreprocessing.modifyImageSize(_src, 500, 500)

                h_rat = (int)(500 / height)
                if(h_rat % 2 == 0):
                    h_rat -= 1
                
                w_rat = (int)(500 / width)
                if(w_rat % 2 == 0):
                    w_rat -= 1
                
                    
                # rat = (int)(rat / 100)
                # if(rat % 2 == 0):
                #     rat = rat - 1
                    
            # bilateral filter
            _src = cv2.bilateralFilter(_src, dist, sigma, sigma)

            # _src = cv2.cvtColor(_src, cv2.COLOR_RGB2GRAY)

            kernel = np.ones((3, 3), np.uint8)
            thr_aver = cv2.adaptiveThreshold(_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blk_size * (int)(w_rat), C)
            thr_gaus = cv2.adaptiveThreshold(_src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blk_size * (int)(w_rat), C)

            # thr_aver = cv2.adaptiveThreshold(_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blk_size, C)
            # thr_gaus = cv2.adaptiveThreshold(_src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blk_size, C)


            thr_aver = cv2.erode(thr_aver, kernel, iterations=1)
            thr_aver = cv2.dilate(thr_aver, kernel, iterations=1)

            thr_aver= ImagePreprocessing.modifyImageSize(thr_aver, width, height)
            thr_gaus= ImagePreprocessing.modifyImageSize(thr_gaus, width, height)

            thr_aver = cv2.adaptiveThreshold(thr_aver, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blk_size, C)
            thr_gaus = cv2.adaptiveThreshold(thr_gaus, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blk_size, C)

        else:
            _src = ImagePreprocessing.modifyImageSize(_src, width, height)
            _src = cv2.bilateralFilter(_src, dist, sigma, sigma)

            # _src = cv2.cvtColor(_src, cv2.COLOR_RGB2GRAY)
        
            thr_aver = cv2.adaptiveThreshold(_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blk_size, C)
            thr_gaus = cv2.adaptiveThreshold(_src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blk_size, C)

        
        return thr_aver, thr_gaus

class ImageEdgeDetection:
    def CannyOperator(_src, low = 0, high = 255, bi= True, dist = 5, sigma = 100, clahe = False, width=100, height=100, color=False):
        _src = cv2.bilateralFilter(_src, dist, sigma, sigma)
        if(clahe):
            _src = ImagePreprocessing.CLAHE(_src)

        _src= ImagePreprocessing.modifyImageSize(_src, width, height)
        if(color):
            _src = cv2.cvtColor(_src, cv2.COLOR_RGB2GRAY)

        canny = cv2.Canny(_src, low, high)
        mask = canny == 0

        # dst = _src * (mask[:, :, None].astype(_src.dtype))

        return mask

# 이미지 테스트 함수입니다.
class ImageTest:
    def imageSegPreview(_src, width=100, height=100):
        t1, otsu = ImageSegmentation.otsuMethod(_src, clahe= True, width = 100, height = 100)
        aver, gaus = ImageSegmentation.adaptiveThreshold(_src, dist = 5, sigma=100, closing=True, width=width, height=height)
        ImageVisualization.print4Srcs('Original: ',ImagePreprocessing.modifyImageSize(_src, width=100, height=100),
                                    'Ostu method: ', otsu, 'Adaptive-Average: ',aver, "Adaptive-Gaussian", gaus)
        
    
    def edgeTest(_src, width, height, method):
        t1, otsu = ImageSegmentation.otsuMethod(_src, clahe= True, width = 100, height = 100)
        if(method == Threshold.OTSU):
            otsu_canny = ImageEdgeDetection.CannyOperator(otsu, t1/2, t1, bi=False, clahe=False)
            src_canny = ImageEdgeDetection.CannyOperator(_src, t1/2, t1, color=True)

            rate = ImageVisualization.printMatchRate(src_canny, otsu_canny)

            ImageVisualization.print4Srcs('Original: ',ImagePreprocessing.modifyImageSize(_src, width=100, height=100),
                                            'Ostu method: ', otsu, 'Original + canny: ',src_canny, "Otsu + canny", otsu_canny)
        elif(method == Threshold.AVERAGE):
            aver, gaus = ImageSegmentation.adaptiveThreshold(_src, dist = 5, sigma=100, closing=True, width=width, height=height)

            aver_canny = ImageEdgeDetection.CannyOperator(aver, t1/2, t1, bi=False, clahe=False)
            src_canny = ImageEdgeDetection.CannyOperator(_src, t1/2, t1, color=True)

            rate = ImageVisualization.printMatchRate(src_canny, aver_canny)

            ImageVisualization.print4Srcs('Original: ',ImagePreprocessing.modifyImageSize(_src, width=100, height=100),
                                            'Adaptive-average: ', aver, 'Original + canny: ',src_canny, "Average + canny", aver_canny)

        elif(method == Threshold.GAUSSIAN):
            aver, gaus = ImageSegmentation.adaptiveThreshold(_src, dist = 5, sigma=100, closing=True, width=width, height=height)

            gaus_canny = ImageEdgeDetection.CannyOperator(gaus, t1/2, t1, bi=False, clahe=False)
            src_canny = ImageEdgeDetection.CannyOperator(_src, t1/2, t1, color=True)

            rate = ImageVisualization.printMatchRate(src_canny, gaus_canny)

            ImageVisualization.print4Srcs('Original: ',ImagePreprocessing.modifyImageSize(_src, width=100, height=100),
                                            'Adaptive-gaussian: ', gaus, 'Original + canny: ',src_canny, "Gaussian + canny", gaus_canny)

    
    def intensityTest(_src, width, height, method):
        if(method==Threshold.OTSU):
            t1, otsu = ImageSegmentation.otsuMethod(_src, clahe= True, width = 100, height = 100)
            b_aver, w_aver = ImageVisualization.printAverage(_src, otsu)
        elif(method==Threshold.AVERAGE):
            aver, gaus = ImageSegmentation.adaptiveThreshold(src, dist = 5, sigma=100, closing=True, width=width, height=height)
            b_aver, w_aver = ImageVisualization.printAverage(_src, otsu)

        
        

def ImageProcessor(src, width, height):
    src = cv2.imread(src, cv2.IMREAD_COLOR)
    if src is None:
        print("Image load failed!")
        sys.exit()
    
    # Gray Scale
    src = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    
    #서버에서 적절한 파일명을 가진 src가 전달되었다고 가정,
    t1, otsu = ImageSegmentation.OtsuMethts(src, clahe=True, width=width, height=height)
    aver, gaus = ImageSegmentation.adaptiveThreshold(src, dist = 5, sigma=100, closing=True, width=width, height=height)
    
    # 255 -> 1
    otsu = ImageOutputProcessor.imageOutput(otsu, None)
    aver = ImageOutputProcessor.imageOutput(aver, None)
    gaus = ImageOutputProcessor.imageOutput(gaus, None)
    
    # json 리턴 - '방식'은 이후 바뀔 수 있음
    json_obj = [
        {'방식 1': otsu},
        {'방식 2': aver},
        {'방식 3': gaus}
    ]

    return json.dumps(json_obj)


if __name__ == '__main__':
    # 원하는 이미지의 경로 - 파일명 입력
    src = cv2.imread("ImageProcessor/image/contrast.png", cv2.IMREAD_COLOR)
    if src is None:
        print("Image load failed!")
        sys.exit()
    
    # Geay Scale
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    
    ImageTest.imageSegPreview(gray)
    
    
    
    
    # t1, otsu = ImageSegmentation.otsuMethod(src, clahe= True, width = 100, height = 100)

    # ImageTest.edgeTest(src, 100, 100, Threshold.OTSU)

    # aver, gaus = ImageSegmentation.adaptiveThreshold(gray, blk_size=7, C=4, dist = 5, sigma=100, closing=True, width = 100, height = 100)
    # aver2, gaus2 = ImageSegmentation.adaptiveThreshold(src,blk_size=7, C=-4, dist = 5, sigma=100, closing=False, width = 100, height = 100)

    # p2 = ImageVisualization.printPercentage(aver)
    # p = ImageVisualization.printPercentage(gaus)


    ImageVisualization.print3Srcs('image: ',src, 'Otsu: ', aver, 'Gaussian: ', gaus, Hist_num=True)
    
    # ImageVisualization.print3Srcs('image: ',src, 'Otsu: ', otsu, 'Gaussian: ', otsu, Hist_num=True)



    cv2.waitKey()
    cv2.destroyAllWindows()
