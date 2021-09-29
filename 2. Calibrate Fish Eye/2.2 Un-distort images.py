import numpy as np
import cv2
import os
import glob

DIM=(640, 480)
K=np.array([[183.40960550714848, 0.0, 317.9915709633227], [0.0, 183.27059290430077, 229.7739640549374], [0.0, 0.0, 1.0]])
D=np.array([[0.0643628313155956], [-0.014811743124422176], [-0.02257099687818543], [0.009516432693973089]])

folderFinalImages = "Result_Images/"

def undistort(img_path, save_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

    # Show
    cv2.imshow("original image", img)
    cv2.imshow("undistorted", undistorted_img)
    # Save
    cv2.imwrite(save_path, undistorted_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    for filename in glob.glob('*.jpg'):
        print(filename)
        savePath = folderFinalImages + filename

        undistort(filename, savePath)

    # Click Enter
    print('Click Enter!')
    x = input()