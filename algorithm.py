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

def getFullFilePath(filePath):
    for ext in imgExtension:
        path = filePath +"." + ext
        if os.path.isfile(path):
            return path
    return None

def showImages(imgList):
    if len(imgList) > 0:
        for i in range(len(imgList)):
            plt.subplot(1, len(imgList), i + 1)
            plt.imshow(imgList[i])
        plt.show()


# Downsampled, concatenation, normalized image
o = 1

def preprocessimg(imgGray):
    # Downsampled
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


trainingThreshold = 5
imgExtension = ["pgm", "jpg", "png"]
# Read images in folder dataset
entries = os.listdir("FaceDataset/")
hatList = []
labelList = []
# Training part
def train():
    print("Processing...")
    for entry in entries:
        personDir = "FaceDataset/" + entry
        imgFilenameList = os.listdir(personDir)
        imgGallery = []
        # Iterative through gallery image of this person folder
        for imgFilename in imgFilenameList:
            imgDir = personDir + "/" + imgFilename

            # Train only first (trainingThreshold - 1) images
            if imgFilename[: imgFilename.index(".")] == str(trainingThreshold):
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
    print("done processing!")

def findPerson(src):
    # Read input image
    imgInput = cv2.imread(src)

    # Convert input image to gray level
    imgInputGray = cv2.cvtColor(imgInput, cv2.COLOR_BGR2GRAY)

    # Pre-process input image
    imgInputPreProcessed = preprocessimg(imgInputGray).to_numpy()
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
        print("Match person: " + personNameFound)
        imgFoundPath = "FaceDataset/" + personNameFound + "/1"
        fullFilePath = getFullFilePath(imgFoundPath)
        return fullFilePath, personNameFound
    else:
        return None, None

# train
train()