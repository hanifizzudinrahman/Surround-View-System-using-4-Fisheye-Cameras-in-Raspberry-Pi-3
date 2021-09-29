import cv2
import numpy as np
import glob
import os
import math

# =============== [ P A R A M E T E R ] - [ F U L L ]
#=========================================================
pathResultImages = r"Result_Images\\"
BEV_Name = "1.Rectangle-BEV Camera Show (Crop).jpg"
heightBEV = 706
widthBEV = 1040
# =============== Camera Filename Images
Camera_A_Name = "Camera_A_1.jpg"
Camera_B_Name = "Camera_B_1.jpg"
Camera_C_Name = "Camera_C_1.jpg"
Camera_D_Name = "Camera_D_1.jpg"
print("=> Filename: ", Camera_A_Name,Camera_B_Name,Camera_C_Name,Camera_D_Name)
print()
# =============== Matrix Camera -> BEV
MatrixA = np.zeros((3,3), np.float)
MatrixB = np.zeros((3,3), np.float)
MatrixC = np.zeros((3,3), np.float)
MatrixD = np.zeros((3,3), np.float)
MatrixA[0:3] = [[-3.97331246e-01, -3.35970227e+00,  7.07705644e+02], [ 2.13662752e-02, -1.88831907e+00,  3.86122305e+02], [ 1.58521856e-05, -5.91162509e-03,  1.00000000e+00]]
MatrixB[0:3] = [[-3.70282162e+00,  1.35447487e-01,  6.77917664e+02], [-2.42284350e+00, -3.40403340e-01,  5.08361784e+02], [-6.71155256e-03, 3.64932494e-04,  1.00000000e+00]]
MatrixC[0:3] = [[-1.76856484e+00, -4.01966105e-03,  6.30668332e+02], [-1.06914569e+00,  2.12590700e-01,  2.83023659e+02], [-3.03334633e-03, -1.59576052e-05,  1.00000000e+00]]
MatrixD[0:3] = [[ 2.93275532e-01, -1.75818320e+00,  4.90120234e+02], [ 1.44451663e-02, -1.17911738e+00,  4.31525305e+02], [ 6.99898154e-05, -3.08305253e-03,  1.00000000e+00]]
print("=> MatrixA = ", MatrixA)
print("=> MatrixB = ", MatrixB)
print("=> MatrixC = ", MatrixC)
print("=> MatrixD = ", MatrixD)
print("="*50)
print()
# =============== Coordinate Small Square [BEST] Inside
pointXMin = 450
pointXMax = 655
pointYMin = 249
pointYMax = 438
print("=> pointXMin = ", pointXMin)
print("=> pointXMax = ", pointXMax)
print("=> pointYMin = ", pointYMin)
print("=> pointYMax = ", pointYMax)
print("="*50)
print()
#=========================================================
# =============== [ P A R A M E T E R ] - [ F U L L ]

# =============== [ F U N C T I O N ] - [ F U L L ]
#=========================================================
def readCamera(cameraName, Camera_Filename):
    img = cv2.imread(Camera_Filename)
    if (cameraName == "A"):
        # Rotate A - No Rotate
        pass
    elif (cameraName == "B"):
        # Camera B - Rotate 90 COUNTERCLOCKWISE
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif (cameraName == "C"):
        # Camera C - Rotate 90 CLOCKWISE
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
    elif (cameraName == "D"):
        # Camera D - Rotate 180 
        img = cv2.rotate(img, cv2.cv2.ROTATE_180)
    cv2.imshow(Camera_Filename, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img
#=========================================================
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
    if cameraName == "A":
        img = cv2.rectangle(imgBEVCamera, (0,yMin), (imgBEVCamera.shape[1],yMax), color, thickness)
    elif cameraName == "B":
        img = cv2.rectangle(imgBEVCamera, (xMin,0), (xMax,imgBEVCamera.shape[0]), color, thickness)
    elif cameraName == "C":
        img = cv2.rectangle(imgBEVCamera, (xMin,imgBEVCamera.shape[0]), (xMax,0), color, thickness)
    elif cameraName == "D":
        img = cv2.rectangle(imgBEVCamera, (imgBEVCamera.shape[1],yMin), (0,yMax), color, thickness)
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
        if cameraName == "A":
            # Removes Buttom Parts
            imgBEVCamera = cv2.rectangle(imgBEVCamera, (0,halfHeight), (widthBEV,halfHeight*2), (0,0,0), -1)
        elif cameraName == "D":
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
def cropBEVRemovaCamera(cameraName,img,BEVRemove_Camera_Name):
    height = img.shape[0]
    width = img.shape[1]
    if cameraName == "A":
        x = 0
        h = int(height/2)
        y = 0
        w = width
        img = img[y:y+h, x:x+w]
        imgRotate = img
    elif cameraName == "B":
        x = 0
        h = height
        y = 0
        w = int(width/2)
        img = img[y:y+h, x:x+w]
        # Rotate 
        imgRotate = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif cameraName == "C":
        x = int(width/2)
        h = height
        y = 0
        w = int(width/2)
        img = img[y:y+h, x:x+w]
        imgRotate = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif cameraName == "D":
        x = 0
        h = int(height/2)
        y = int(height/2)
        w = width
        img = img[y:y+h, x:x+w]
        imgRotate = cv2.rotate(img, cv2.ROTATE_180)
    cv2.imshow("-Crop-" + BEVRemove_Camera_Name, img)
    cv2.imshow("-Rotate-" + BEVRemove_Camera_Name, imgRotate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img, imgRotate
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#=========================================================
def writeNewImage(img, pathWriteImg):
    cv2.imwrite(pathWriteImg, img)
#=========================================================
# =============== [ F U N C T I O N ] - [ F U L L ]

# =============== [ M A I N - F U N C T I O N ] - [ F U L L ]
#=========================================================
def main():
    print("==> 1. Size BEV")
    print("Height: ", heightBEV)
    print("Width: ", widthBEV)
    print()

    print("==> 2. Read Camera & Rotate")
    print()
    # ==================== Read Camera & Rotate
    imgCameraA = readCamera("A", Camera_A_Name)
    imgCameraB = readCamera("B", Camera_B_Name)
    imgCameraC = readCamera("C", Camera_C_Name)
    imgCameraD = readCamera("D", Camera_D_Name)

    print("==> 2. Show  BEV Result")
    print()
    # Show  BEV Result
    imgCameraA = showBEV_Result(imgCameraA,Camera_A_Name,MatrixA, widthBEV,heightBEV)
    imgCameraB = showBEV_Result(imgCameraB,Camera_B_Name,MatrixB, widthBEV,heightBEV)
    imgCameraC = showBEV_Result(imgCameraC,Camera_C_Name,MatrixC, widthBEV,heightBEV)
    imgCameraD = showBEV_Result(imgCameraD,Camera_D_Name,MatrixD, widthBEV,heightBEV)

    print("==> 3. Remove Small Square [BEST] Inside - [ F U L L ]")
    print()
    # Remove Small Square [BEST] Inside - [ F U L L ]
    imgCameraA = removeSmallSquareFull("A", imgCameraA, pointXMin,pointXMax,pointYMin,pointYMax)
    imgCameraB = removeSmallSquareFull("B", imgCameraB, pointXMin,pointXMax,pointYMin,pointYMax)
    imgCameraC = removeSmallSquareFull("C", imgCameraC, pointXMin,pointXMax,pointYMin,pointYMax)
    imgCameraD = removeSmallSquareFull("D", imgCameraD, pointXMin,pointXMax,pointYMin,pointYMax)

    print("==> 3. Show Line to Divided and Removes")
    print()
    # Show Line to Divided and Removes
    imgCameraA = showLineDividedRemove("A",imgCameraA,Camera_A_Name, heightBEV,widthBEV)
    imgCameraB = showLineDividedRemove("B",imgCameraB,Camera_B_Name, heightBEV,widthBEV)
    imgCameraC = showLineDividedRemove("C",imgCameraC,Camera_C_Name, heightBEV,widthBEV)
    imgCameraD = showLineDividedRemove("D",imgCameraD,Camera_D_Name, heightBEV,widthBEV)

    print("==> 4. Show Line to Divided and Removes")
    print()
    # Read BEV Remove Camera & Crop
    imgCameraA, imgCameraRotateA = cropBEVRemovaCamera("A", imgCameraA,Camera_A_Name)
    imgCameraB, imgCameraRotateB = cropBEVRemovaCamera("B", imgCameraB,Camera_B_Name)
    imgCameraC, imgCameraRotateC = cropBEVRemovaCamera("C", imgCameraC,Camera_C_Name)
    imgCameraD, imgCameraRotateD = cropBEVRemovaCamera("D", imgCameraD,Camera_D_Name)

    print("==> 4. Write new Images - [ F U L L ]")
    print()
    # Write new Images
    filenameImage = "5.1.BEV-FINAL-FULL-"
    filenameImage = pathResultImages + filenameImage
    writeNewImage(imgCameraA, filenameImage+Camera_A_Name)
    writeNewImage(imgCameraB, filenameImage+Camera_B_Name)
    writeNewImage(imgCameraC, filenameImage+Camera_C_Name)
    writeNewImage(imgCameraD, filenameImage+Camera_D_Name)
    # Write new Images Rotate
    filenameImage = "5.2.R.BEV-FINAL-FULL-"
    filenameImage = pathResultImages + filenameImage
    writeNewImage(imgCameraRotateA, filenameImage+Camera_A_Name)
    writeNewImage(imgCameraRotateB, filenameImage+Camera_B_Name)
    writeNewImage(imgCameraRotateC, filenameImage+Camera_C_Name)
    writeNewImage(imgCameraRotateD, filenameImage+Camera_D_Name)
#=========================================================
# =============== [ M A I N - F U N C T I O N ] - [ F U L L ]

if __name__ == '__main__':       
    # Calling main() function 
    main()