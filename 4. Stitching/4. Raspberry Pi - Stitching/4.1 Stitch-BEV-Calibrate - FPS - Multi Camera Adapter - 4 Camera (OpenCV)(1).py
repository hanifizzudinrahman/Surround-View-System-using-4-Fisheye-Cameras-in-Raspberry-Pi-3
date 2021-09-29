import RPi.GPIO as gp
from datetime import datetime as dtm
import cv2
import time
import os
import numpy as np

# =============== [ P A R A M E T E R ] - [ F U L L ]
#=========================================================
# Calibrate Fish Eye
DIM=(640, 480)
K=np.array([[183.40960550714848, 0.0, 317.9915709633227], [0.0, 183.27059290430077, 229.7739640549374], [0.0, 0.0, 1.0]])
D=np.array([[0.0643628313155956], [-0.014811743124422176], [-0.02257099687818543], [0.009516432693973089]])
# Bird's Eye View (BEV)
pathResultImages = r"Result_Images/"
heightBEV = 785
widthBEV = 657
# Camera Filename Images
Camera_Name = "Camera Bird's Eye View"
#  Matrix Camera -> BEV
MatrixA = np.zeros((3,3), np.float)
MatrixB = np.zeros((3,3), np.float)
MatrixC = np.zeros((3,3), np.float)
MatrixD = np.zeros((3,3), np.float)
MatrixA[0:3] = [[ 2.36588339e-01, -9.79616203e-01,  2.31036674e+02], [-9.26623812e-03, -1.35976221e+00,  4.85950598e+02], [-6.85560659e-05, -3.12789910e-03,  1.00000000e+00]]
MatrixB[0:3] = [[-2.19189956e+00,  1.08059785e-01,  4.30714845e+02], [-2.98505403e+00, -4.48153295e-01,  6.36091901e+02], [-7.19621378e-03,  4.49285188e-04,  1.00000000e+00]]
MatrixC[0:3] = [[-1.06122502e+00, -5.80395453e-02,  3.81511526e+02], [-1.29407427e+00,  2.14188277e-01,  3.27761048e+02], [-3.18749314e-03, -1.48513790e-04,  1.00000000e+00]]
MatrixD[0:3] = [[-6.56100043e-01, -2.23582382e+00,  4.97126571e+02], [-4.64843971e-02, -2.77641520e+00,  5.24733577e+02], [-1.21516486e-04, -7.20435663e-03,  1.00000000e+00]]
print("=> MatrixA = ", MatrixA)
print("=> MatrixB = ", MatrixB)
print("=> MatrixC = ", MatrixC)
print("=> MatrixD = ", MatrixD)
print("="*50)
print()
#  Coordinate Small Square [BEST] Inside
pointXMin = 225
pointXMax = 411
pointYMin = 290
pointYMax = 519
print("=> pointXMin = ", pointXMin)
print("=> pointXMax = ", pointXMax)
print("=> pointYMin = ", pointYMin)
print("=> pointYMax = ", pointYMax)
print("="*50)
print()
# =============== Masking Parameter 
Parameter_Masking_NameX = r"_PARAMS_MASKING_HORIZONTAL_.jpg"
Parameter_Masking_NameY = r"_PARAMS_MASKING_VERTICAL_.jpg"
#=========================================================
# =============== [ P A R A M E T E R ] - [ F U L L ]

# =============== [ P I N O U T - R A S P B E R R Y  P I  3 ]
#=========================================================
gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, True)
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)
#=========================================================
# =============== [ P I N O U T - R A S P B E R R Y  P I  3 ]

done = 0
trigger = 0

# =============== [ M A I N - F U N C T I O N ] -  [R A S P B E R R Y  P I  3 ]
#=========================================================
def main():
    global done
    print("==> 1. Size BEV")
    print("Height: ", heightBEV)
    print("Width: ", widthBEV)
    print() 
    while True:
        saat_ini = dtm.now() #tgl dan jam saat ini
        now = dtm.strftime(saat_ini, '%d-%b-%Y_%H:%M:%S') # tpye = string
        if done == 1:
            print('F I N I S H')
            break
        startTime = time.time()
        i2c = "i2cset -y 1 0x70 0x00 0x07"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)
        imgCameraD = captureCamera("D")     # Camera D
        i2c = "i2cset -y 1 0x70 0x00 0x06"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)
        imgCameraC = captureCamera("C")     # Camera C
        i2c = "i2cset -y 1 0x70 0x00 0x04"
        os.system(i2c)
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)
        imgCameraA = captureCamera("A")     # Camera A
        i2c = "i2cset -y 1 0x70 0x00 0x05"
        os.system(i2c)
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)
        imgCameraB = captureCamera("B")     # Camera B
        # Stitching Camera A-B-C-D
        imgStitch = stitchCamera(imgCameraA,imgCameraB,imgCameraC,imgCameraD, Parameter_Masking_NameX,Parameter_Masking_NameY)
        # Calculate FPS
        FPS = calculateFPS(imgStitch,startTime)
        print(".")
        
        # Show Image Stitch
        cv2.imshow('Stitching ', imgStitch)
        # Save Image or Stop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == ord("d"):
            done = 1
        elif key == ord("s"):
            saveName = "Stitching (FPS) %s.jpg" % now
            cv2.imwrite(pathResultImages+saveName, imgStitch)
            print("=> Save", saveName)
    cv2.destroyAllWindows()   
# =========================================================
# =============== [ M A I N - F U N C T I O N ] -  [R A S P B E R R Y  P I  3 ]

# =============== [ F U N C T I O N ]
#=========================================================      
def captureCamera(cam):
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        # Resolution
        # Default = 640x480
        # Raspberry Pi Camera v2 (8 megapixel): 3280 x 2464
        # video at 1080p30, 720p60, 640x480p90
        # width =  #1920 - 1280 - 640 - 320 - 160 - 80 - 40 [BEST = 3280]
        # height = #1080 - 720 - 480 - 240 - 120 - 60 - 30  [BEST = 2464]
        width = 640        
        height = 480        
        cap.set(3, width)
        cap.set(4, height)
        startTime = time.time()
        # Window
        ret_val, img = cap.read()
        # Rotate 180
        #img = cv2.rotate(img, cv2.ROTATE_180)
        # Fish Eye Calibrated
        img = fishEyeCalibrated(img)
        # Read Camera & Rotate
        img = readCamera(img,cam, Camera_Name)
        # Show  BEV Result
        if cam == "A":
            img = showBEV_Result(img,Camera_Name,MatrixA, widthBEV,heightBEV)
        elif cam == "B":
            img = showBEV_Result(img,Camera_Name,MatrixB, widthBEV,heightBEV)
        elif cam == "C":
            img = showBEV_Result(img,Camera_Name,MatrixC, widthBEV,heightBEV)
        elif cam == "D":
            img = showBEV_Result(img,Camera_Name,MatrixD, widthBEV,heightBEV)
        # Remove Small Square [BEST] Inside
        img = removeSmallSquareFull(cam, img, pointXMin,pointXMax,pointYMin,pointYMax)
        # Show Line to Divided and Removes
        img = showLineDividedRemove(cam,img,Camera_Name, heightBEV,widthBEV)
        return img
    else:
        print("Unable to open camera")
#=========================================================
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def fishEyeCalibrated(oriImg):
    h,w = oriImg.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(oriImg, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def readCamera(img,cameraName, Camera_Filename):
    if (cameraName == "D"):
        # Rotate D - No Rotate
        pass
    elif (cameraName == "B"):
        # Camera B - Rotate 90 COUNTERCLOCKWISE
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif (cameraName == "C"):
        # Camera C - Rotate 90 CLOCKWISE
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
    elif (cameraName == "A"):
        # Camera A - Rotate 180 
        img = cv2.rotate(img, cv2.cv2.ROTATE_180)
    '''
    cv2.imshow(Camera_Filename, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return img
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showBEV_Result(img,Camera_Filename,matrix, width,height):
    imgBEV = cv2.warpPerspective(img,matrix, (width,height))
    '''
    cv2.imshow("-BEV-" + Camera_Filename, imgBEV)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return imgBEV
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def removeSmallSquareFull(cameraName, imgBEVCamera, xMin,xMax,yMin,yMax):
    thickness = -1
    color = (0,0,0)
    img = cv2.rectangle(imgBEVCamera, (xMin,yMin), (xMax,yMax), color, thickness)
    '''
    cv2.imshow("removeSmallSquareFull", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return img
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def showLineDividedRemove(cameraName,imgBEVCamera,BEV_Camera_Name, heightBEV,widthBEV):
    color = (0,0,255)
    thickness = 1
    # Divided Into 2 Parts
    halfHeight = int(heightBEV/2)
    halfWidth = int(widthBEV/2)
    if cameraName == "A" or cameraName == "D":
        imgBEVCamera = cv2.line(imgBEVCamera, (0,halfHeight), (widthBEV,halfHeight), color, thickness)
        if cameraName == "D":
            # Removes Buttom Parts
            imgBEVCamera = cv2.rectangle(imgBEVCamera, (0,halfHeight), (widthBEV,halfHeight*2), (0,0,0), -1)
        elif cameraName == "A":
            # Removes Top Parts
            imgBEVCamera = cv2.rectangle(imgBEVCamera, (0,0), (widthBEV,halfHeight), (0,0,0), -1)
    elif cameraName == "C" or cameraName == "B":
        imgBEVCamera = cv2.line(imgBEVCamera, (halfWidth,0), (halfWidth,heightBEV), color, thickness)
        if cameraName == "C":
            # Removes Left Parts
            imgBEVCamera = cv2.rectangle(imgBEVCamera, (0,0), (halfWidth,heightBEV), (0,0,0), -1)
        elif cameraName == "B":
            # Removes Right Parts
            imgBEVCamera = cv2.rectangle(imgBEVCamera, (halfWidth,0), (halfWidth*2,heightBEV), (0,0,0), -1)
    '''
    cv2.imshow("Remove Parts" + BEV_Camera_Name, imgBEVCamera)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return imgBEVCamera
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def stitchCamera(imgA,imgB,imgC,imgD, imgMaskX_Name, imgMaskY_Name):
    # Read Masking Parameter
    imgMaskX = cv2.imread(imgMaskX_Name, 0)
    imgMaskY = cv2.imread(imgMaskY_Name, 0)
    # ADD
    img_add_Ver = cv2.add(imgA,imgD)
    img_add_Hor = cv2.add(imgB,imgC)
    #  BITWISE AND & MASKING [VERTICAL]
    img_add_Ver = cv2.bitwise_and(img_add_Ver,img_add_Ver,mask = imgMaskX)
    # ERASE THE ERROR WITH LINE (BLACK DOTS)
    color = (0,0,0)
    thickness = 10
    img_add_Ver = cv2.line(img_add_Ver,(407,290),(592,0),color,thickness)
    img_add_Ver = cv2.line(img_add_Ver,(227,290),(62,0),color,thickness)
    img_add_Ver = cv2.line(img_add_Ver,(235,519),(84,785),color,thickness)
    img_add_Ver = cv2.line(img_add_Ver,(389,519),(508,785),color,thickness)
    #  BITWISE AND & MASKING [HORIZONTAL]
    #img_add_Hor = cv2.bitwise_and(img_add_Hor,img_add_Hor,mask = imgMaskY)
    #  ADD - FINAL
    imgStitching = cv2.add(img_add_Ver,img_add_Hor)        
    return imgStitching
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def calculateFPS(img,startTime):
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    endTime = time.time()
    fps = 1/(endTime - startTime)
    # converting the fps into 2 decimal pint
    fps = format(fps, ".2f")
    cv2.putText(img, fps, (0, 30), font, 1, (100, 255, 0), 3, cv2.LINE_AA)
    return fps
#=========================================================
# =============== [ F U N C T I O N ]

if __name__ == "__main__":
    main()

    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)





