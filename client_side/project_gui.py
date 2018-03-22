import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import datetime
import json
import requests
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import tkinter as tk
from tkinter import ttk


conversion_type = 'RGB'   # 'RGB' or 'L'


# here we read it from raspberry
img = Image.open("picture.jpeg").convert(conversion_type)
arr = np.array(img)
shape = arr.shape
imageList = arr.flatten().tolist()
# ----
arrback = np.zeros(shape, dtype=np.uint8)
rect = patches.Rectangle((0,0),0,0,linewidth=1,edgecolor='r',facecolor='none')


LARGE_FONT= ("Verdana", 15)
#style.use("ggplot")

f = Figure(dpi=100)
a = f.add_subplot(211)
b = f.add_subplot(212)


def animate(i):
    a.clear()
    a.imshow(arr)
    b.clear()
    b.imshow(arrback)
    b.add_patch(rect)




    
    
               

class CloudOffloadModule(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Offload Face Detection")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (FirstPage, SingleImageOffload, ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        

class FirstPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="CLOUD OFFLOAD TEST MODULE", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(   self, 
                                text="Single Image Offload",
                                command=lambda: controller.show_frame(SingleImageOffload)
                            )
        button1.pack()





class SingleImageOffload(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="OFFLOAD FACE DETECTION", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        L1 = ttk.Label(self, text="IP")
        L1.pack()
        self.E1 = ttk.Entry(self)
        self.E1.pack()
    


        button1 = ttk.Button(   self, 
                                text="Offload",
                                command=self.offloadImage
                            )
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    def offloadImage(self):
        global arrback
        global rect 
        location = self.E1.get()
        serveradd = 'http://' + location + '/cgi-bin/calculate_offload_RGB.py'
        payload = {'image': imageList, 'shape': shape, 'type': conversion_type}
        mydata = json.JSONEncoder().encode(payload)

        #t1 = datetime.datetime.now()
        for i in range(1):
            r = requests.post(serveradd, data=mydata)
            backData = json.loads(r.text)
            backImage = backData['image']
            coord = backData['coord']
        #t2 = datetime.datetime.now()
        #tdif = t2 - t1
        #print(str(tdif.microseconds/1e6) + ' seconds')

        arrback = np.array(backImage, dtype=np.uint8).reshape(shape)
        rect = patches.Rectangle((coord[0],coord[1]),coord[2],coord[3],linewidth=1,edgecolor='r',facecolor='none')



app = CloudOffloadModule()
ani = animation.FuncAnimation(f, animate, interval=100)
app.mainloop()