from cv2 import cv2
import os

keyword = input("Enter the name of keyword this video belong to: ")
if not os.path.exists(keyword):
    os.makedirs(keyword)

file_name = ""+".mp4"       #in the blank section enter the name of the video
vidcap = cv2.VideoCapture(file_name)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("data/image"+str(count)+".jpg", image)     # save frame as JPG file
    return hasFrames
sec = 0
frameRate = 2 #//it will capture image in each 2 second
count=1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)