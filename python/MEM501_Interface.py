import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageFont, ImageDraw, ImageTk
import serial
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sched, time
import threading
import os.path
from os import path
import numpy as np
import struct

matplotlib.rcParams.update(
    {
        'text.usetex': False,
        'font.family': 'stixgeneral',
        'mathtext.fontset': 'stix',
    }
)

Connected = False
data = 0
Reading = False
MicrocontrollerSerial = serial.Serial()

root = Tk() 
root.title("Soğuk Hava Deposu Uygulaması") 
root.maxsize(900, 600) 
root.config(bg="#008000") 
left_frame = Frame(root, width=200, height=500, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)
right_frame = Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

def PrintScreen(textString):
        img = Image.new('RGBA' ,(650,400), 'grey')
        font= ImageFont.truetype("arial.ttf",15)
        w,h= font.getsize(textString)
        draw = ImageDraw.Draw(img)
        draw.text(((650-w)/2,(400-h)/2), textString,font=font, fill='white')
        image = ImageTk.PhotoImage(img)
        schedule.enter(5, 1, DrawImageBox(image))
        schedule.run()

def DrawImageBox(image):
    for widget in right_frame.winfo_children():
        widget.destroy()
    Label(right_frame, image=image).grid(row=0,column=0, padx=5, pady=5)

def float64_to_str(var):
    if type(var) is list:
        return str(var)[1:-1] 
    if type(var) is np.ndarray:
        try:
            return str(list(var[0]))[1:-1]
        except TypeError:
            return str(list(var))[1:-1] 
    return str(var) 

img = Image.new('RGBA' ,(650,400), 'white')
textString = "Hoş geldiniz...\nBağlantı ayarlarını yaparak \nKontrol modülüne bağlanınız.."
font= ImageFont.truetype("arial.ttf",15)
w,h= font.getsize(textString)
draw = ImageDraw.Draw(img)
draw.text(((650-w)/2,(400-h)/2), textString,font=font, fill='black')
image = ImageTk.PhotoImage(img)
DrawImageBox(image)


Label(left_frame, text="Eren OKUR 21908613\nMEMYL 501 Proje Çalışması").grid(row=0, column=0, padx=5, pady=5)
studentRawimage = Image.open("data/erenokur.jpg")
studentRawimage = studentRawimage.resize((150, 150), Image.ANTIALIAS)
studentImage = ImageTk.PhotoImage(studentRawimage)
Label(left_frame, image=studentImage).grid(row=1, column=0, padx=5, pady=5)

tool_bar = Frame(left_frame, width=180, height=185)
tool_bar.grid(row=2, column=0, padx=5, pady=5)


def Drawing():
    i=0
    x=list()
    y=list()
    while True:
        for widget in right_frame.winfo_children():
            widget.destroy() 
        figure3 = plt.Figure(figsize=(5,4), dpi=100)
        ax3 = figure3.add_subplot(111)
        x.append(i)
        y.append(data)
        scatter3 = FigureCanvasTkAgg(figure3, right_frame) 
        scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        ax3.set_xlabel('Zaman')
        ax3.set_ylabel('Sıcaklık')
        ax3.set_title('Sıcaklık Zaman Grafigi')
        ax3.grid()
        ax3.plot( x, y, marker='o', color='orange') 
        i += 1
        time.sleep(3)

def StartListening():
    global data
    global Reading
    if not Reading:
        global MicrocontrollerSerial
        Reading = True
        while True:
            data = MicrocontrollerSerial.readline()
            data = data.decode()
            if(data):
                print(data)

def CheckMicrocontrollerCom():
    global Connected
    global MicrocontrollerSerial
    if not Connected:
        portName = "COM" + str(comPort.get())
        MicrocontrollerSerial = serial.Serial(portName, 9600)
        MicrocontrollerSerial.close()
        MicrocontrollerSerial.open()
        time.sleep(1)
        Connected = True
        firstMessage = threading.Thread( target=StartListening, args= ( ))
        firstMessage.start()

def StartDrawing():
    drawer = threading.Thread( target=Drawing, args= ( ))
    drawer.start()

def StartEmbeded():
    CheckMicrocontrollerCom()

def SendSetValue():
    CheckMicrocontrollerCom()
    global MicrocontrollerSerial
    sendValueis = int(setValue.get())
    #MicrocontrollerSerial.write(sendValueis.encode)
    MicrocontrollerSerial.write(struct.pack('>B',sendValueis))

comPort = tk.StringVar()
Button(tool_bar, text="Gömülü Sistem Ayarla",command=StartEmbeded,bg='brown',fg='white').grid(row=0, column=0, padx=5, pady=5)
e1 = tk.Entry(tool_bar, textvariable=comPort).grid(row=0, column=1, padx=5, pady=5)

setValue = tk.StringVar()
Button(tool_bar, text="Depo Değeri Ata",command=SendSetValue,bg='brown',fg='white').grid(row=1, column=0, padx=5, pady=5)
e2 = tk.Entry(tool_bar, textvariable=setValue).grid(row=1, column=1, padx=5, pady=5)

Button(tool_bar, text="Çizdirmeye Başla",command=StartDrawing,bg='brown',fg='white').grid(row=2, column=0, padx=5, pady=5)

root.mainloop()