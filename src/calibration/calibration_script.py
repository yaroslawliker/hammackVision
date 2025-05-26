#
# Code is primerely taken from OpenCV tutorials:
# https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
#

import numpy as np
import pickle
import glob

import cv2 as cv

col, row = 8, 6
 
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
cm_per_block = 1.5

objp = np.zeros((col*row,3), np.float32)
objp[:,:2] = np.mgrid[0:col,0:row].T.reshape(-1,2) * 1.5
 
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images_path = 'data/calibration/galaxyA50/'
images = glob.glob(images_path + '*.jpg')

cv.namedWindow('img', cv.WINDOW_NORMAL)
cv.resizeWindow('img', 800, 600)
 
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
 
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (col,row), None)
 
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
 
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
 
        # Draw and display the corners
        cv.drawChessboardCorners(img, (col,row), corners, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
 
cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

fx = mtx[0, 0]
fy = mtx[1, 1]
u = mtx[0, 2]
v = mtx[1, 2]

matrix_data = [fx, fy, u, v]

with open(images_path + "matrix.pkl", "wb") as file:
    pickle.dump(matrix_data, file)
