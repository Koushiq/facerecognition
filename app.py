import tkinter as tk
from tkinter import filedialog,ttk
import get_files
import shutil

root = tk.Tk()
root.title("Smart Security Camera")
root.resizable(False, False)
root.geometry("+390+250")

name = tk.StringVar()

def switchOn():
    for widget in frame.winfo_children():
        widget.destroy()
    label1 = tk.Label(frame,text="In Secure Mode", pady=50,fg="#b50000")
    label1.config(font=("Calibri",24))
    label1.pack()
def switchOff():
    for widget in frame.winfo_children():
        widget.destroy()
    label2 = tk.Label(frame,text="In Default Mode", pady=50, fg="#002ae3")
    label2.config(font=("Calibri", 24))
    label2.pack()
def add():
    newWindow = tk.Toplevel(root)
    newWindow.title("Add New Known Face")
    newWindow.resizable(False, False)
    newWindow.geometry("+390+250")
    canvas2 = tk.Canvas(newWindow,height=200,width=500,bg="white")
    canvas2.pack()
    frame2 = tk.Frame(newWindow,bg="white")
    frame2.place(relwidth=1, relheight=1)
    label3 = tk.Label(frame2,text="Name: ")
    label3.config(font=("Calibri", 16))
    label3.place(x=150, y=80)
    # name = tk.StringVar()
    text = ttk.Entry(frame2,width=15,textvariable=name)
    text.place(x=210, y=80)
    uploadFile = tk.Button(frame2,text="Upload Image", padx=10 , pady=5, fg="white", bg="grey", command=upload)
    uploadFile.place(x=160, y=110)
    submit = tk.Button(frame2,text="Submit", padx=10 , pady=5, fg="white", bg="grey", command=submitFace)
    submit.place(x=270, y=110)
def upload():
    root.filename = filedialog.askopenfilename(initialdir="/img", title="Select A File", filetypes=[("jpg files", "*.jpg"), ])
def submitFace():
    imgId = get_files.get_next_file_id("img/known") - 1
    newName = name.get()
    dst = "img/known/"+str(imgId)+"-"+newName+".jpg"
    newPath = shutil.copy(root.filename, dst)


canvas = tk.Canvas(root,height=200,width=500,bg="grey")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=1, relheight=1)

title = tk.Label(frame,text="Smart Security Camera", pady=50)
title.config(font=("Calibri", 24))
title.pack()

modeOn = tk.Button(root,text="Secure Mode", padx=10 , pady=5, fg="white", bg="grey", command=switchOn)
modeOn.place(x=150, y=80)

modeOff = tk.Button(root,text="Default Mode", padx=10 , pady=5, fg="white", bg="grey", command=switchOff)
modeOff.place(x=260, y=80)

addKnown = tk.Button(root,text="Add Known", padx=10 , pady=5, fg="white", bg="grey", command=add)
addKnown.place(x=210, y=110)

root.mainloop()