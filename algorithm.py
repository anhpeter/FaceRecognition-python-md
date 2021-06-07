import os
import cv2
from functools import cmp_to_key
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from skimage.transform import resize

# SUPPORT FUNCTIONS
# create sort key
def number_cmp(a, b):
    try:
        aNumber = int(a[: a.index(".")])
        bNumber = int(b[: b.index(".")])
        return aNumber - bNumber
    except:
        return 0


number_cmp_key = cmp_to_key(number_cmp)


def showImages(imgList):
    if len(imgList) > 0:
        for i in range(len(imgList)):
            plt.subplot(1, len(imgList), i + 1)
            plt.imshow(imgList[i])
        plt.show()


# INITIATE VALUES
trainingThreshold = 5
imgExtension = ["pgm", "jpg", "png"]

faceDatasetDir = 'FaceDataset/'
entries = os.listdir(faceDatasetDir)
hatList = []
labelList = []
arrImgPre = []

# Downsampled, concatenation, normalized image
def preprocessing(imgGray):
    # Resize image
    imgResize = resize(imgGray, (50, 50))

    # Flatten the image
    imgRavel = np.ravel(imgResize)

    # Reshape to column vector
    imgVector = imgRavel.reshape(-1, 1)

    # Convert image to DataFrame
    imgDataFrame = DataFrame(imgVector)

    # Normalized image
    imgNormalized = (imgDataFrame - imgDataFrame.min()) / (
        imgDataFrame.max() - imgDataFrame.min()
    )
    return imgNormalized

# Training part
def train():
    print("Traning ...")
    for entry in entries:
        personDir = faceDatasetDir + entry
        imgFilenameList = os.listdir(personDir)
        imgFilenameList.sort(key=number_cmp_key)
        imgGallery = []

        # Preprocess person's images
        for imgFilename in imgFilenameList[:trainingThreshold]:
            imgDir = personDir + "/" + imgFilename

            # Read image
            img = cv2.imread(imgDir)

            # Convert to gray image
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Append to the image gallery dataframe
            imgPreProcessed = preprocessing(imgGray)
            arrImgPre.append(imgPreProcessed)
        

        for img in arrImgPre:
            # Convert dataframe to array
            imgGalleryArray = img.to_numpy()
        
            # Transpose of the image gallery array
            imgGalleryArrayTranspose = imgGalleryArray.T
            # Calculation
            subCalculate = np.dot(imgGalleryArrayTranspose, imgGalleryArray)
            subCalculate2 = np.dot(imgGalleryArray, np.linalg.pinv(subCalculate))
            hatMatrix = np.dot(subCalculate2, imgGalleryArrayTranspose)
            hatList.append(hatMatrix)
            labelList.append(entry)
    print("Done training!")

# Find person by test image src
def findPerson(src):
    # Read input image
    imgInput = cv2.imread(src)

    # Convert input image to gray level
    imgInputGray = cv2.cvtColor(imgInput, cv2.COLOR_BGR2GRAY)

    # Pre-process input image
    imgInputPreProcessed = preprocessing(imgInputGray).to_numpy()
    distanceList = []

    # create distance list
    for hatMatrix in hatList:
        closestVector = np.dot(hatMatrix, imgInputPreProcessed)
        # Distance calculation
        dist = np.linalg.norm(imgInputPreProcessed - closestVector)
        distanceList.append(dist)

    # Get index of the image found by finding the min distance
    minDintace = min(distanceList)

    # note: after many test I found that: min distace > 13 => not found
    if minDintace < 13:
        imgFoundIndex = distanceList.index(minDintace)

        # Get the index of the person
        personNameFound = labelList[imgFoundIndex]

        # Show result
        #print("Match person: " + personNameFound)
        imgFoundDirPath = faceDatasetDir + personNameFound

        # get first found person's image
        imgFoundFilename = os.listdir(imgFoundDirPath)[0]
        fullFilePath = imgFoundDirPath + "/" + imgFoundFilename
        return fullFilePath, personNameFound
    else:
        return None, None


