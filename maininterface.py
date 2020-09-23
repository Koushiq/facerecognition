import tkinter as tk
from tkinter import filedialog,ttk
import get_files
import shutil
import recogniser
import differnce_detector

root = tk.Tk()
root.title("Smart Security Camera")
root.resizable(False, False)
root.geometry("+150+200")

name = tk.StringVar()
time = tk.IntVar()
msg = tk.StringVar()
msg2 = tk.StringVar()
# msg2.set("NULL")
def switchOn():
    for widget in frame.winfo_children():
        widget.destroy()
    modeOn.place_forget()
    modeOff.place_forget()
    label1 = tk.Label(frame,text="In Secure Mode", pady=50,fg="#b50000",bg="white")
    label1.config(font=("Calibri",24))
    label1.pack()
    stop = tk.Button(frame,text="Stop", padx=10 , pady=5, fg="white", bg="grey", command=stopMode)
    stop.place(x=215, y=90)
    differnce_detector.triggerCam()
    
def switchOff():
    for widget in frame.winfo_children():
        widget.destroy()
    modeOn.place_forget()
    modeOff.place_forget()
    label2 = tk.Label(frame,text="In Default Mode", pady=50, fg="#002ae3",bg="white")
    label2.config(font=("Calibri", 24))
    label2.pack()
    stop = tk.Button(frame,text="Stop", padx=10 , pady=5, fg="white", bg="grey", command=stopMode)
    stop.place(x=215, y=90)
    recogniser.triggerFaceDetection()
    
def add():
    msg2.set("")
    newWindow = tk.Toplevel(root)
    newWindow.title("Add New Known Face")
    newWindow.resizable(False, False)
    newWindow.geometry("+150+200")
    canvas2 = tk.Canvas(newWindow,height=200,width=500,bg="white")
    canvas2.pack()
    frame2 = tk.Frame(newWindow,bg="white")
    frame2.place(relwidth=1, relheight=1)
    label3 = tk.Label(frame2,text="Name: ",bg="white")
    label3.config(font=("Calibri", 16))
    label3.place(x=150, y=80)
    text = ttk.Entry(frame2,width=15,textvariable=name)
    text.place(x=220, y=80)
    uploadFile = tk.Button(frame2,text="Upload Image", padx=10 , pady=5, fg="white", bg="grey", command=upload)
    uploadFile.place(x=155, y=110)
    submit = tk.Button(frame2,text="Submit", padx=10 , pady=5, fg="white", bg="grey", command=submitFace)
    submit.place(x=280, y=110)
    label6 = tk.Label(frame2,textvariable=msg2,bg="white",fg="red")
    label6.config(font=("Calibri", 12))
    label6.place(x=160, y=160)
def upload():
    msg2.set("")
    root.filename = filedialog.askopenfilename(initialdir="/home/pi/Desktop", title="Select A File", filetypes=[("jpg files", "*.jpg"), ])
def submitFace():
    try:
        imgId = get_files.get_next_file_id("img/known")
        newName = name.get()
        dst = "img/known/"+str(imgId)+"-"+newName+".jpg"
        newPath = shutil.copy(root.filename, dst)
        msg2.set("New face successfully added!")
    except:
        msg2.set("Something went wrong!")
        
def stopMode():
    for widget in frame.winfo_children():
        widget.destroy()
    modeOn.place(x=130, y=90)
    modeOff.place(x=250, y=90)
    header = tk.Label(frame,text="Smart Security Camera", pady=50,bg="white")
    header.config(font=("Calibri", 24))
    header.place(x=100,y=0)
    
def selectDelay():
    newWindow2 = tk.Toplevel(root)
    newWindow2.title("Select Notification Delay")
    newWindow2.resizable(False, False)
    newWindow2.geometry("+150+200")
    canvas3 = tk.Canvas(newWindow2,height=200,width=500,bg="white")
    canvas3.pack()
    frame3 = tk.Frame(newWindow2,bg="white")
    frame3.place(relwidth=1, relheight=1)
    label4 = tk.Label(frame3,text="Delay:",bg="white")
    label4.config(font=("Calibri", 16))
    label4.place(x=100, y=77)
    text2 = ttk.Entry(frame3,width=15,textvariable=time)
    text2.place(x=160, y=80)
    submit = tk.Button(frame3,text="Submit", padx=10 , pady=5, fg="white", bg="grey", command=setTime)
    submit.place(x=310, y=75)
    label5 = tk.Label(frame3,textvariable=msg,bg="white",fg="red")
    label5.config(font=("Calibri", 12))
    label5.place(x=150, y=110)
    
def setTime():
    try:
        t = int(time.get())
        print(t)
        getTime(t)
        msg.set("Delay set successfully!")
    except:
        t = int(0)
        print(t)
        getTime(t)
        msg.set("Invalid Input. Please try again")
def getTime(t):
    # NOTE: MUST USE THIS t NOT time for delay...
    return(t)
        
canvas = tk.Canvas(root,height=200,width=500,bg="grey")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=1, relheight=1)

header = tk.Label(frame,text="Smart Security Camera", pady=50,bg="white")
header.config(font=("Calibri", 24))
header.place(x=100,y=0)

modeOn = tk.Button(root,text="Secure Mode", padx=10 , pady=5, fg="white", bg="grey", command=switchOn)
modeOn.place(x=130, y=90)

modeOff = tk.Button(root,text="Default Mode", padx=10 , pady=5, fg="white", bg="grey", command=switchOff)
modeOff.place(x=250, y=90)

addKnown = tk.Button(root,text="Add Known", padx=10 , pady=5, fg="white", bg="grey", command=add)
addKnown.place(x=140, y=130)

delay = tk.Button(root,text="Select Delay", padx=10 , pady=5, fg="white", bg="grey", command=selectDelay)
delay.place(x=250, y=130)

root.mainloop()