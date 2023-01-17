import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
import time


class App:

    def __init__(self, window, cap):
        self.window = window
        self.window.title('ipod ad at home')
        self.cap = cap
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.update_time = 50
        self.brightness_val = 1
        self.color = 0
        self.start = time.time()

        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()

        self.exit_button = tk.Button(self.window, text='exit', command=self.exit)
        self.exit_button.pack(side=tk.RIGHT, fill=tk.Y)
        self.snapshot_button = tk.Button(self.window, text='snapshot', command=self.snapshot)
        self.snapshot_button.pack(side=tk.LEFT, fill=tk.Y)
        self.entry = tk.Entry(self.window)
        self.entry.pack(fill=tk.X)
        self.scale = tk.Scale(self.window, from_=0, to=10, orient=tk.HORIZONTAL, resolution=0.05, command=self.brightness)
        self.scale.pack(fill=tk.X)
        self.scale.set(1)

        self.video()


    def video(self):
        self.gray = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2GRAY)
        self.thresh = cv2.ximgproc.niBlackThreshold(self.gray, maxValue=255, type=cv2.THRESH_BINARY, blockSize=21, k=0.142, binarizationMethod=cv2.ximgproc.BINARIZATION_WOLF)
        #self.imageCV = cv2.adaptiveThreshold(self.imageCV, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 43, 9)
        self.imageCV = (self.gray > self.thresh).astype("uint8") * 255 #Wolf-Julion local binarization
        self.imageCV = cv2.cvtColor(self.imageCV, cv2.COLOR_GRAY2RGB)
        self.imageCV = cv2.blur(self.imageCV, (1,1))
        
        self.imageCV = cv2.floodFill(self.imageCV, None, seedPoint=(0, 240), newVal=self.random_color())[1]        
        self.imagePIL = Image.fromarray(self.imageCV)
        self.brightener = ImageEnhance.Brightness(self.imagePIL)
        self.imagePIL = self.brightener.enhance(self.brightness_val)
        self.imageTk = ImageTk.PhotoImage(self.imagePIL)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imageTk)
        self.window.after(self.update_time, self.video)


    def exit(self):
        self.window.destroy()
        self.cap.release()

    def snapshot(self):
        self.imagePIL.save(self.entry.get()+'.png', "PNG")

    def brightness(self,_):
        self.brightness_val = self.scale.get()

    def random_color(self):        
        if self.color == 0:
            self.color = np.random.randint(0,255,3).tolist()         
# random color 4/4 time 100 bpm
        while True:
            self.now = time.time()
            if self.now - self.start > 2.4:
                self.color = np.random.randint(0,255,3).tolist()
                print(self.now - self.start)
                self.start = time.time()                
            else:
                break             
            
        return self.color


def main():
    root = tk.Tk()
    app = App(root, cv2.VideoCapture(0))
    root.mainloop()


if __name__ == "__main__":
    main()