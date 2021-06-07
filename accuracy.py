import os
import algorithm

# train
algorithm.train()

start = algorithm.trainingThreshold

def testing():
    print("Testing ...")
    testingDic = {}
    for entry in algorithm.entries:
        personDir = algorithm.faceDatasetDir + entry
        imgFilenameList = os.listdir(personDir)
        imgFilenameList.sort(key=algorithm.number_cmp_key)
        imgFilenameList = imgFilenameList[start:]

        testingDic[entry] = {"total": len(imgFilenameList), "correct": 0}
        for imgFilename in imgFilenameList:
            personImgFilePath = personDir + "/" + imgFilename
            _, personName = algorithm.findPerson(personImgFilePath)
            if personName == entry:
                testingDic[entry]["correct"] = testingDic[entry]["correct"] + 1
    print("Done testing!")
    return testingDic

testingDic = testing()
totalImg = 0
totalCorrect = 0

for key in testingDic:
    item = testingDic[key]
    totalImg+=item["total"]
    totalCorrect+=item["correct"]

accuracyScore = totalCorrect / totalImg
print("\nAccuracy score: ", round(accuracyScore, 2))
print("\nDetails:\n", testingDic)

