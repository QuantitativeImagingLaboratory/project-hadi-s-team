import tkinter
from tkinter import filedialog
from tkinter import *
import numpy as np

import cv2


class Application(Frame):

    img=0

    def call_show_erosion(self):

        global img
        self.erosion()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def call_show_dilation(self):

        global img
        self.dilation()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def call_show_open(self):

        global img
        self.open()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def call_show_close(self):

        global img
        self.close()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def call_show_open_close(self):

        global img
        self.open_close()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def call_show_close_open(self):

        global img
        self.close_open()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def erosion(self):

        global img
        global E1
        global E2

        h = img.shape





        iteration = (E1.get())
        dim= int(E2.get())

        it=int(iteration)




        kernel = np.ones((dim, dim), np.uint8)
        output = np.zeros((h[0], h[1]), np.uint8)
        flag=0

        for py in range(0, h[1]):
            for px in range(0, h[0]):

                if (img[px,py]>0) and (img[px,py]<255) :
                    flag=1

                    break



        if (flag==0):
            for i in range(0, it):
                for py in range(int(dim / 2), h[1] - int(dim / 2)):
                    for px in range(int(dim / 2), h[0] - int(dim / 2)):

                        sum = 0

                        for ky in range(py - int(dim / 2), py + int(dim / 2) + 1):
                            for kx in range(px - int(dim / 2), px + int(dim / 2) + 1):
                                sum = sum + img[kx, ky]

                        if (sum == (dim * dim * 255)):
                            output[px, py] = 255

            img = output

        else:

            for i in range(0, it):
                for py in range(int(dim / 2), h[1] - int(dim / 2)):
                    for px in range(int(dim / 2), h[0] - int(dim / 2)):

                        min = 300

                        for ky in range(py - int(dim / 2), py + int(dim / 2) + 1):
                            for kx in range(px - int(dim / 2), px + int(dim / 2) + 1):
                                if(img[kx, ky]<min) :
                                    min= img[kx, ky]


                        output[px, py] = min

            img = output






    def dilation(self):
        global img
        global E1
        global E2

        h = img.shape

        iteration = (E1.get())
        dim = int(E2.get())

        it = int(iteration)

        kernel = np.ones((dim, dim), np.uint8)
        output = np.zeros((h[0], h[1]), np.uint8)
        flag = 0

        for py in range(0, h[1]):
            for px in range(0, h[0]):

                if (img[px, py] > 0) and (img[px, py] < 255):
                    flag = 1

                    break


        if (flag == 0):
            for i in range(0, it):
                for py in range(int(dim / 2), h[1] - int(dim / 2)):
                    for px in range(int(dim / 2), h[0] - int(dim / 2)):

                        sum = 0

                        for ky in range(py - int(dim / 2), py + int(dim / 2) + 1):
                            for kx in range(px - int(dim / 2), px + int(dim / 2) + 1):
                                sum = sum + img[kx, ky]

                        if (sum > (255)):
                            output[px, py] = 255

            img = output

        else:

            for i in range(0, it):
                for py in range(int(dim / 2), h[1] - int(dim / 2)):
                    for px in range(int(dim / 2), h[0] - int(dim / 2)):

                        max = 0

                        for ky in range(py - int(dim / 2), py + int(dim / 2) + 1):
                            for kx in range(px - int(dim / 2), px + int(dim / 2) + 1):
                                if (img[kx, ky] > max):
                                    max = img[kx, ky]

                        output[px, py] = max

            img = output



    def open(self):

            global img


            self.erosion()
            self.dilation()





    def close(self):

            global img

            self.dilation()
            self.erosion()



    def open_close(self):

            global img
            global E1
            global E2

            self.open()
            self.close()


    def close_open(self):

            global img

            self.close()
            self.open()





    def hitmiss(self):

        global img

        #enter your code here




    def Skeletonization(self):

            global img
            global img
            global E1
            global E2

            it = int(E1.get())




            cv2.imshow('image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def open_file(self):



        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("PNG files", "*.png"),("jpeg files", "*.jpg"), ("all files", "*.*")))

        global img
        img = cv2.imread(root.filename, 0)






    def initUI(self):



        self.master.title("Morphological Operations")

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        operation=Menu(menubar)

        submenu = Menu(fileMenu)


        submenu2 = Menu(operation)


        fileMenu.add_command(label="Open", underline=0, command=self.open_file)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", underline=0, command=self.quit())
        menubar.add_cascade(label="File", underline=0, menu=fileMenu)
        menubar.add_cascade(label="Operation", underline=0, menu=operation)
        operation.add_command(label='Erosion', underline=0, command=self.call_show_erosion)
        operation.add_separator()
        operation.add_command(label='Dilation', underline=0, command=self.call_show_dilation)
        operation.add_separator()
        operation.add_command(label='Open', underline=0, command=self.call_show_open)
        operation.add_separator()
        operation.add_command(label='Close', underline=0, command=self.call_show_close)
        operation.add_separator()
        operation.add_command(label='Open-Close', underline=0, command=self.call_show_open_close)
        operation.add_separator()
        operation.add_command(label='Close-Open', underline=0, command=self.call_show_close_open)
        operation.add_separator()
        operation.add_command(label='Hit and Miss', underline=0, command=self.hitmiss)
        operation.add_separator()
        operation.add_command(label='Skeletonization', underline=0, command=self.Skeletonization)

        label1 = Label(root, text="Number of Iterations")
        global E1
        global E2
        E1 = Entry(root, bd=5)

        label2 = Label(root, text="Kernel Size (N)")
        E2 = Entry(root, bd=5)







        #submit = Button(root, text="Submit", command=getDate)

        label1.pack()
        E1.pack()
        label2.pack()
        E2.pack()



        #submit.pack(side=BOTTOM)







    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi



    def form(self):
        labelText = StringVar()
        labelText.set("Enter directory of log files")
        labelDir = Label(root, textvariable=labelText, height=4)
        labelDir.pack(side="left")

        directory = StringVar(None)
        dirname = Entry(root, textvariable=directory, width=10)
        dirname.pack(side="left")





        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.show_entry_fields("sasaa")
        self.hi_there.pack({"side": "left"})


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.initUI()

root = Tk()



app = Application(master=root)


app.mainloop()
root.destroy()
