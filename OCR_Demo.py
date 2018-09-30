#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import *
from tkinter import filedialog
import tkinter.messagebox #这个是消息框，对话框的关键
from OCR_Location import *
import numpy as np
import cv2 as cv
import OCR_Global as gl
import os
from PIL import Image, ImageDraw, ImageFont

root = Tk()
root.title("OCR文字识别") #在这里修改窗口的标题
frame = Frame(root, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=1, column=0, sticky=E+W)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)
text = Text(frame,bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
text.grid(row=0, column=0, sticky=N+S+E+W)
xscroll.config(command=text.xview)
yscroll.config(command=text.yview)
frame.grid(row=0,columnspan=2)

def imageGray():
    img_rgb = filedialog.askopenfilename(parent=root,title='Choose an image.')
    print(img_rgb)
    if img_rgb != "":
        if '.png' in img_rgb or '.jpg' in img_rgb:
            clear()
            img_gray = cv.cvtColor(cv.imread(img_rgb),cv.COLOR_BGR2GRAY)
            kernel = np.array([
                [-1, -1, -1, -1, -1],
                [-1, 2, 2, 2, -1],
                [-1, 2, 5, 2, -1],
                [-1, 2, 2, 2, -1],
                [-1, -1, -1, -1, -1]]) / 6.11
            dst = cv.filter2D(img_gray, 0, kernel=kernel)
            cv.imwrite("C:/temp_ocr.png", dst)
            gl.gPicturePath = "C:/temp_ocr.png"
            gl.gFirstPicturePath = img_rgb
            findAll()
        else:
            tkinter.messagebox.showinfo('提示', '请选择格式为jpg或png的图片')
    else:
        tkinter.messagebox.showinfo('提示', '请正确选择图片')

def findAll():
    if gl.gFirstPicturePath:
        isExist = os.path.exists(gl.gPicturePath)
        text.delete(0.0, END)
        if gl.gAllResult:
            resultStr = get_all_str()
            text.insert(END, resultStr)
        elif isExist:
            img_to_str(gl.gPicturePath)
            resultStr = get_all_str()
            text.insert(END, resultStr)
        findPictureAll()
    else:
        tkinter.messagebox.showinfo('提示', '请先读取图片')

def findOne():
    if gl.gFirstPicturePath:
        containsStr = entry.get()
        if containsStr.strip() != "":
            isExist = os.path.exists(gl.gPicturePath)
            text.delete(0.0, END)
            if gl.gAllResult:
                resultStr = get_one_str(containsStr)
                text.insert(END, resultStr)
            elif isExist:
                img_to_str(gl.gPicturePath)
                resultStr = get_one_str(containsStr)
                text.insert(END, resultStr)
            findPictureOne()
        else:
            tkinter.messagebox.showinfo('提示', '请输入想要搜索的关键词')
    else:
        tkinter.messagebox.showinfo('提示', '请先读取图片')

def findPictureAll():
    gl.gAllFileName = gl.gFirstPicturePath.split("/")
    root.title(gl.gAllFileName[len(gl.gAllFileName)-1])  # 在这里修改窗口的标题
    cv.namedWindow("Target", cv.WINDOW_NORMAL)
    cv.imshow("Target",cv.imread(gl.gFirstPicturePath))

def findPictureOne():
    left = []
    top = []
    height = []
    width = []
    for w in gl.gOneResult:
        left.append(w['left'])
        top.append(w['top'])
        height.append(w['height'])
        width.append(w['width'])
    img_rgb = cv.imread(gl.gPicturePath)
    merged = cv.GaussianBlur(np.uint8(np.clip((1.0 * img_rgb - 60), 0, 200)), (0, 0), 3)
    for i in range(0,len(left)):
        cv.rectangle(img_rgb, (left[i] - 5, top[i] - 5,),(left[i] + width[i] + 5, top[i] + height[i] + 5), (0, 30, 255), 5)
        cropImg = img_rgb[top[i] - 5:top[i] + height[i] + 5,left[i] - 5:left[i] + width[i] + 5]
        merged[top[i] - 5:top[i] + height[i] + 5,left[i] - 5:left[i] + width[i] + 5] = cropImg
    for j in range(0,len(left)):
        if j == 0:
            pil_im = Image.fromarray(merged)
        else:
            pil_im = Image.fromarray(cv_text_im)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("FZYTK.TTF", 40, encoding="utf-8")
        draw.text((left[j], top[j] + height[j] + 20), "坐标位：%s,%s" % (left[j], top[j]), (220, 40, 1), font=font)
        cv_text_im = cv.cvtColor(np.array(pil_im), cv.COLOR_RGB2BGR)
        cv.imwrite("C:/temp_opencv.png", cv_text_im)
    root.title("temp_opencv.png")  # 在这里修改窗口的标题
    cv.namedWindow("Target", cv.WINDOW_NORMAL)
    cv.imshow("Target",cv.imread("C:/temp_opencv.png"))

def clear():
    text.delete(0.0,END)
    entry.delete(0, END)
    gl.gPicturePath = ""
    gl.gOneResult = []
    gl.gAllResult = []

buttonReadPicture = Button(root, text="读取图片", command=imageGray, font=16).grid(row=1,columnspan=2)
buttonAll = Button(root, text="搜索全部", command=findAll, font=16).grid(row=2,rowspan=2)
entry = Entry()
entry.grid(row=2,column=1)
buttonOne = Button(root, text="搜索单词", command=findOne, font=16,fg="blue").grid(row=3,column=1)

# 进入消息循环
root.mainloop()

