
from tkinter import *
import numpy as np
import cv2
from tkinter import filedialog

#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk

####################################################################################
# Levent Dane
####################################################################################

# Zhang-Suen Thinning Algorithm
# Ref1 https://github.com/linbojin/Skeletonization-by-Zhang-Suen-Thinning-Algorithm
# Ref2 https://rosettacode.org/wiki/Zhang-Suen_thinning_algorithm#Python
# Ref3 http://rstudio-pubs-static.s3.amazonaws.com/302782_e337cfbc5ad24922bae96ca5977f4da8.html

def neighbours(x,y,image):
    "Return 8-neighbours of image point P1(x,y), in a clockwise order"
    img = image
    x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1
    return [ img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],     # P2,P3,P4,P5
                img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1] ]    # P6,P7,P8,P9

def transitions(neighbours):
    n = neighbours + neighbours[0:1]      # P2, P3, ... , P8, P9, P2
    res = 0
    for i in range(len(n)-1):
        if n[i] == 0 and n[i+1] == 1:
            res+=1
    return res

def thinning(image):
    output = image.copy()
    step1 = []
    rows, columns  = output.shape
    # Step1
    for x in range(1, rows - 1):
        for y in range(1, columns - 1):
            P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, output)
            if (output[x][y] == 1   and # Pixel White? 
                2 <= sum(n) <= 6    and # How many white neighbour?
                transitions(n) == 1 and # How many transitions around?
                P2 * P4 * P6 == 0   and # At least one of the north, east, and south neighbors is white
                P4 * P6 * P8 == 0):     # At least one of east, south, and west neighbors is white
                step1.append((x,y))

    # Clean all the step1 points
    for x, y in step1:
        output[x][y] = 0

    # Step 2
    step2 = []
    for x in range(1, rows - 1):
        for y in range(1, columns - 1):
            P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, output)
            if (output[x][y] == 1   and
                2 <= sum(n) <= 6    and
                transitions(n) == 1 and
                P2 * P4 * P8 == 0   and # At least one of the north, east, and west neighbors is white
                P2 * P6 * P8 == 0):     # At least one of north, south, and west neighbors is white
                step2.append((x,y))

    # Clean all the step2 points
    for x, y in step2:
        output[x][y] = 0
    return output, len(step1) + len(step2)

def skeleton_img(image):
    "the Zhang-Suen Thinning Algorithm"
    done = 1        #  the points to be removed (set as 0)
    while done:     #  iterates until no further changes occur in the image
        image, done = thinning(image)
    return image

####################################################################################
# Levent Dane
####################################################################################


class Window(Frame):



    def showImg(self,f):


        load = Image.open(f)
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

    def call_show_hitmiss(self):

        global img
        self.hitmiss()
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

#########################################################################

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


###################################################################################
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


##########################################################################
    def hitmiss(self):

        global img
        global E1
        global E2

        h = img.shape
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        #print(ret)
        #print(img)

        iteration = 4
        dim = 3

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

                if (it==0):
                    kernel = np.array([[0, 1, 0], [0, 1, 1], [0, 0, 0]])

                if (it==1):
                    kernel = np.array([[0, 1, 0], [1, 1, 0], [0, 0, 0]])

                if (it==2):
                    kernel = np.array([[0, 0, 0], [1, 1, 0], [0, 1, 0]])

                if (it==3):
                    kernel = np.array([[0, 0, 0], [0, 1, 1], [0, 1, 0]])


                for py in range(3, h[1] - 3):
                    for px in range(3, h[0] - 3):

                        sum = 0

                        for ky in range(0,3):
                            #print(ky)
                            for kx in range(0,2):
                                sum = sum + (img[px+kx, py+ky]*kernel[kx][ky])


                        if (sum == (3 * 255)):
                            output[px, py] = 255

            img = output



        #self.render()

####################################################################################
# Levent Dane
####################################################################################

    def get_value(self, x):
        if x.get() == '':
            from tkinter import messagebox
            messagebox.showerror('Ups', 'Please enter a value')
        else:
            return int(x.get())

    def Majority(self):
        global img
        self.showImg(filename,)

        it = self.get_value(E1)
        k = self.get_value(E2)

        n,m = img.shape
        output = np.zeros((n,m), np.uint8)
        for x in range(n):
            for y in range(m):
                px1=max(x-k,0)
                px2=min(x+k,n)
                py1=max(y-k,0)
                py2=min(y+k,m)
                # Using np.median and np slicing
                #output[x,y] = np.median(img[px1:px2,py1:py2])
                # do manually
                values = []
                for i in range(px1,px2):
                    for j in range(py1,py2):
                        values.append(img[i,j])
                values=sorted(values)
                med = int(len(values)/2)
                output[x,y] = values[med]

        img = output

        self.render()


    def Skeletonization(self):
        global img

        img = img/255
        img = skeleton_img(img)
        img = img*255

        self.render()

    def Skel_Distance(self):
        global img
        n,m = img.shape
        output = np.zeros((n,m), np.uint8)

        #Distance Map
        list_zeros = []
        list_ones = []
        for i in range(1,n-1):
            for j in range(1,m-1):
                #all whites
                if img[i,j] == 255:
                    list_ones.append((i,j))
                #zeros with at least one white neighbor
                if (img[i,j] == 0 and
                    sum([img[i-1,j-1],
                        img[i-1,j],
                        img[i-1,j+1],
                        img[i,j+1],
                        img[i+1,j+1],
                        img[i+1,j],
                        img[i+1,j-1],
                        img[i,j-1]]) != 0
                    ):
                    list_zeros.append((i,j))

        for one_x, one_y in list_ones:
            min_distance = [0, 0, 0]
            for zero_x, zero_y in list_zeros:
                #distance = abs(zero_x-one_x)+abs(zero_y-one_y)
                distance = abs(zero_x-one_x)**2+abs(zero_y-one_y)**2
                distance = int(np.sqrt(distance))
                if min_distance[0] == 0 or min_distance[0] > distance:
                    min_distance = [distance, zero_x, zero_y]
            output[one_x,one_y] = min_distance[0]

        max_d = np.max(output)
        img = output*int(255/max_d)
        self.render()

        from tkinter import messagebox
        ans = messagebox.askyesno('Ridge Detection', 'Would you like to see ridge detection?')
        if ans== 'no':
            return

        #Ridge Detecton
        output2 = np.zeros((n,m), np.uint8)
        for one_x, one_y in list_ones:
            if (output[one_x-1,one_y]!=0 and
                output[one_x-1,one_y] < output[one_x,one_y] and
                output[one_x+1,one_y]!=0 and
                output[one_x+1,one_y] < output[one_x,one_y]):
                output2[one_x,one_y] = 255
                continue
            if (output[one_x,one_y-1]!=0 and
                output[one_x,one_y-1] < output[one_x,one_y] and
                output[one_x,one_y+1]!=0 and
                output[one_x,one_y+1] < output[one_x,one_y]):
                output2[one_x,one_y] = 255
                continue
            if (output[one_x-1,one_y-1]!=0 and
                output[one_x-1,one_y-1] < output[one_x,one_y] and
                output[one_x+1,one_y+1]!=0 and
                output[one_x+1,one_y+1] < output[one_x,one_y]):
                output2[one_x,one_y] = 255
                continue
            if (output[one_x-1,one_y+1]!=0 and
                output[one_x-1,one_y+1] < output[one_x,one_y] and
                output[one_x+1,one_y-1]!=0 and
                output[one_x+1,one_y-1] < output[one_x,one_y]):
                output2[one_x,one_y] = 255
                continue
        #Better way
        #calculate the major eigenvalue of the Hessian matrix at each pixel
        #from skimage.feature import hessian_matrix, hessian_matrix_eigvals

        #hxx, hxy, hyy = hessian_matrix(img, sigma=3)
        #i1, i2 = hessian_matrix_eigvals(hxx, hxy, hyy)
        #img = i1

        img = output2
        self.render()
####################################################################################
# Levent Dane
####################################################################################


    def open_file(self):

        global img
        global filename
        load = Image.open('bg.png')
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        filename = filedialog.askopenfilename(initialdir=".", title="Select file",
                                                   filetypes=(("PNG files", "*.png"), ("jpeg files", "*.jpg"),
                                                              ("all files", "*.*")))


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
        operation.add_command(label='Hit and Miss', underline=0, command=self.call_show_hitmiss)
        operation.add_separator()
        operation.add_command(label='Skeletonization', underline=0, command=self.Skeletonization)
        operation.add_command(label='Skel_Distance', underline=0, command=self.Skel_Distance)
        operation.add_command(label='Majority', underline=0, command=self.Majority)

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
