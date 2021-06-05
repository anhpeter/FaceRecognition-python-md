import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
import os
from skimage.transform import rescale
from skimage.transform import resize
# from tkinter import filedialog
# from tkinter import *


# Downsampled, concatenation, normalized image
def preprocessimg(imgGray):

    # Downsampled
    imgRescale = rescale(imgGray, scale=(0.1, 0.1))
    #Resize image
    imgResize = resize(imgGray, (50,50))
    # print('imgResize', imgResize)
    # Flatten the image
    imgRavel = np.ravel(imgResize)
    imgRavel = np.ravel(imgRescale)
    # Reshape to column vector
    imgVector = imgRavel.reshape(-1, 1)
    # Convert image to DataFrame
    imgDataFrame = DataFrame(imgVector) 
    # Normalized image
    imgNormalized = (imgDataFrame - imgDataFrame.min()) / (imgDataFrame.max() - imgDataFrame.min())
    return imgNormalized



trainingThreshold = 5
imgExtension = ".pgm"
print("Processing...")
# Read images in folder dataset
entries = os.listdir('FaceDataset/')
hatList = []
labelList = []
# Training part
for entry in entries:
    personDir = 'FaceDataset/' + entry
    imgList = os.listdir(personDir)
    imgGallery = []
    # Iterative through gallery image of this person folder
    for imgName in imgList:
        imgDir = personDir + '/' + imgName
        imgIdx = imgName[:imgName.index('.')]
        
        # Train only first (trainingThreshold - 1) images
        if imgIdx == str(trainingThreshold):
            break
        # Read image
        img = cv2.imread(imgDir)
        # Convert to gray image
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     
        # Append to the image gallery dataframe
        imgPreProcessed = preprocessimg(imgGray)
        imgGallery = pd.concat([imgPreProcessed, imgPreProcessed], axis=1)

    # Convert dataframe to array
    imgGalleryArray = imgGallery.to_numpy()
    # Transpose of the image gallery array
    imgGalleryArrayTranspose = imgGalleryArray.T
    # Calculation
    subCalculate = np.dot(imgGalleryArrayTranspose, imgGalleryArray)
    subCalculate2 = np.dot(imgGalleryArray, np.linalg.pinv(subCalculate))
    hatMatrix = np.dot(subCalculate2, imgGalleryArrayTranspose)
    hatList.append(hatMatrix)
    labelList.append(entry)
# Test part
# for entry in entries:
#     personDir = 'FaceDataset/' + entry + '/' + str(trainingThreshold)+imgExtension
#     print(personDir)
#     # Read input image
#     imgInput = cv2.imread(personDir)
#     # Convert input image to gray level
#     imgInputGray = cv2.cvtColor(imgInput, cv2.COLOR_BGR2GRAY)
#     # Pre-process input image
#     imgInputPreProcessed = preprocessimg(imgInputGray).to_numpy()
#     distanceList = []
#     for hatMatrix in hatList:
#         closestVector = np.dot(hatMatrix, imgInputPreProcessed)
#         # Distance calculation
#         dist = np.linalg.norm(imgInputPreProcessed - closestVector)
#         distanceList.append(dist)
#     # Get index of the image found by finding the min distance
#     idxImgFound = distanceList.index(min(distanceList))
#     # Get the index of the person
#     idxPerson = labelList[idxImgFound]
#     # Show result
#     print("Match person: " + idxPerson)
#     imgFoundDir = 'FaceDataset/' + idxPerson + '/1'+imgExtension
#     imgFound = cv2.imread(imgFoundDir)
#     ax = plt.subplot(1, 2, 1)
#     ax.set_title('Input Image')
#     plt.imshow(imgInput)
#     ax = plt.subplot(1, 2, 2)
#     ax.set_title('Found Image - Person: ' + idxPerson)
#     plt.imshow(imgFound)
#     # plt.show()



