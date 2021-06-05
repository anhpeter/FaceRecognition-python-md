import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import filedialog

appTitle = "Face Recognition"
primaryColor = "#293955"
secondaryColor = "#dddddd"
imgWidth = 250
imgHeight = 250
imageYOffset = 150
noImageSrc = "./assets/images/no_image.png"


# TRIGGER WHEN UPLOAD INPUT IMAGE CLICKED
def uploadFileHandler():
    filename = filedialog.askopenfilename(
        title="selected input image",
        filetypes=(
            ("jpg files", "*.jpg"),
            ("png files", "*.png"),
            ("pgm files", "*.pgm"),
        ),
    )

    # change image by image src
    inputImage.changeImageBySrc(filename)

    # uploaded image src
    # print(inputImage.src)


class ImageWidget:
    def __init__(self, window, src, x=0, y=0):
        self.src = src
        self.x = x
        self.y = y
        self.window = window
        self.loadImage()

    def loadImage(self):
        self.img = PIL.Image.open(self.src)
        self.resized = self.img.resize((imgWidth, imgHeight), PIL.Image.ANTIALIAS)
        self.imgTk = PIL.ImageTk.PhotoImage(self.resized)

    # show image on the screen
    def show(self):
        self.picLabel = Label(window, image=self.imgTk)
        self.picLabel.place(x=self.x, y=self.y)

    def changeImageBySrc(self, src):
        self.src = src
        self.img = PIL.Image.open(self.src)
        self.resized = self.img.resize((imgWidth, imgHeight), PIL.Image.ANTIALIAS)
        self.imgTk = PIL.ImageTk.PhotoImage(self.resized)
        self.picLabel.configure(image=self.imgTk)


def showLabel(win, text, fontsize=16, x=0, y=0):
    label = Label(
        win, text=text, fg=secondaryColor, bg=primaryColor, font=(None, fontsize)
    )
    label.place(x=x, y=y)
    return label


def getButton(win, text, fontsize=16, command=None):
    return Button(
        win,
        text=text,
        fg=primaryColor,
        bg=secondaryColor,
        font=(fontsize),
        command=command,
    )


window = Tk()
window.configure(bg=primaryColor)


# widgets
title = showLabel(window, appTitle, fontsize=25, x=10, y=10)

# input
inputImage = ImageWidget(window, noImageSrc, 150, imageYOffset)
inputImage.show()
inputLabel = showLabel(window, "Input image", x=225, y=imageYOffset + imgHeight + 10)

# output
outputImage = ImageWidget(window, noImageSrc, 500, imageYOffset)
outputImage.show()
inputLabel = showLabel(window, "Output image", x=570, y=imageYOffset + imgHeight + 10)

# upload button
uploadButton = getButton(window, "Upload input image", command=uploadFileHandler)
uploadButton.place(width=350, x=260, y=500)


def test():
    return

#test button
testButton = getButton(window, "Test", command=test)
testButton.place(width=350, x=260, y=570)


# window setup
window.resizable(False, False)
window.title(appTitle)
window.geometry("900x750+10+10")
window.mainloop()
