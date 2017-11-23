from tkinter import *
import numpy as np
import cv2
from tkinter import filedialog

#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk


class Window(Frame):



    def showImg(self,f):


        load = Image.open( f)
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=180)

    def call_show_erosion(self):

        global img
        self.erosion()
        self.render()

    def call_show_dilation(self):

        global img
        self.dilation()
        self.render()

    def call_show_open(self):

        global img
        self.open()
        self.render()

    def call_show_close(self):

        global img
        self.close()
        self.render()

    def call_show_open_close(self):

        global img
        self.open_close()
        self.render()

    def call_show_close_open(self):

        global img
        self.close_open()
        self.render()

    def render(self):
        global img
        cv2.imwrite('result.png', img)
        # labels can be text or images

        load = Image.open("result.png")
        render = ImageTk.PhotoImage(load)
        imgg = Label(self, image=render)
        imgg.image = render
        imgg.place(x=300, y=180)



    def erosion(self):

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
                                if (img[kx, ky] < min):
                                    min = img[kx, ky]

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

        # enter your code here

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
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("PNG files", "*.png"), ("jpeg files", "*.jpg"),
                                                              ("all files", "*.*")))

        global img
        img = cv2.imread(filename, 0)
        self.showImg(filename)

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        operation = Menu(menubar)

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

        label1.pack()
        E1.pack()
        E1.place(x=140, y=10)
        label1.place(x=10, y=10)

        label2.pack()
        E2.pack()
        E2.place(x=140, y=50)
        label2.place(x=10, y=50)



    def showText(self):
        text = Label(self, text="Hey there good lookin!")
        text.pack()

    def client_exit(self):
        exit()


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("600x400")

# creation of an instance
app = Window(root)

# mainloop
root.mainloop()
