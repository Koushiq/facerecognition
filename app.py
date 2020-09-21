import tkinter as tk
from tkinter import filedialog,ttk
import get_files
import shutil
from PIL import ImageTk,Image
import glob
import os

root = tk.Tk()
root.title("Smart Security Camera")
root.resizable(False, False)
root.geometry("+150+200")

name = tk.StringVar()
time = tk.IntVar()
msg = tk.StringVar()
msg2 = tk.StringVar()
image_list = []
res_list = []
sysmail = tk.StringVar()
mymail = tk.StringVar()
pw = tk.StringVar()

def switchOn():
    for widget in frame.winfo_children():
        widget.destroy()
    modeOn.place_forget()
    modeOff.place_forget()
    label1 = tk.Label(frame,text="In Secure Mode", pady=50,fg="#b50000",bg="white")
    label1.config(font=("Calibri",24))
    label1.pack()
    stop = tk.Button(frame,text="Back", padx=10 , pady=5, fg="white", bg="grey", command=stopMode)
    stop.place(x=215, y=90)
def switchOff():
    for widget in frame.winfo_children():
        widget.destroy()
    modeOn.place_forget()
    modeOff.place_forget()
    label2 = tk.Label(frame,text="In Default Mode", pady=50, fg="#002ae3",bg="white")
    label2.config(font=("Calibri", 24))
    label2.pack()
    stop = tk.Button(frame,text="Back", padx=10 , pady=5, fg="white", bg="grey", command=stopMode)
    stop.place(x=215, y=90)
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
def viewImages():
    for filename in glob.glob('/home/pi/Desktop/habiba-dev/img/known/*.jpg'):
        img = Image.open(filename)
        image_list.append(img)
    newWindow3 = tk.Toplevel(root)
    newWindow3.title("Known Faces")
    newWindow3.resizable(False, False)
    newWindow3.geometry("+150+20")
    canvas4 = tk.Canvas(newWindow3,height=500,width=500,bg="white")
    canvas4.pack()
    frame4 = tk.Frame(newWindow3,bg="white")
    frame4.place(relwidth=1, relheight=1)
    
    for im in image_list:
        h=400
        w=int(h/im.height*im.width)
        im = im.resize((w,h))
        res_list.append(im)
        
    global photo
    photo = ImageTk.PhotoImage(res_list[0])
    
    global label7
    label7 = tk.Label(frame4,image=photo)
    label7.image = photo
    label7.place(x=140,y=20)
    
    global prevbtn
    prevbtn = tk.Button(frame4,text="<<", padx=10 , pady=5, fg="white", bg="grey", command=prevImg)
    prevbtn.place(x=140, y=445)
    prevbtn["state"] = "disabled"
    
    remove = tk.Button(frame4,text="Delete Known", padx=10 , pady=5, fg="white", bg="grey", command=lambda: removeImg(0,frame4))
    remove.place(x=195, y=445)
    remove["state"] = "normal"
    
    global nextbtn
    nextbtn = tk.Button(frame4,text=">>", padx=10 , pady=5, fg="white", bg="grey", command=lambda: nextImg(1,frame4))
    nextbtn.place(x=320, y=445)
    
def prevImg(num,frame):
    global label7
    global photo
    global prevbtn
    global nextbtn
    global remove
    
    try:
        label7.place_forget()
        photo = ImageTk.PhotoImage(res_list[num])
        
        label7 = tk.Label(frame,image=photo)
        label7.image = photo
        label7.place(x=140,y=20)
        
        nextbtn = tk.Button(frame,text=">>", padx=10 , pady=5, fg="white", bg="grey", command=lambda: nextImg(num+1,frame))
        nextbtn.place(x=320, y=445)
        
        prevbtn = tk.Button(frame,text="<<", padx=10 , pady=5, fg="white", bg="grey", command=lambda: prevImg(num-1,frame))
        prevbtn.place(x=140, y=445)
        
        remove = tk.Button(frame,text="Delete Known", padx=10 , pady=5, fg="white", bg="grey", command=lambda: removeImg(num,frame))
        remove.place(x=195, y=445)
        
        if num <= 0:
            prevbtn["state"] = "disabled"
            print(prevbtn["state"])
        
    except:
        label8 = tk.Label(frame,text="No more known faces",bg="white",fg="red")
        label8.config(font=("Calibri", 12))
        label8.place(x=180, y=230)
        
def nextImg(num,frame):
    global label7
    global photo
    global prevbtn
    global nextbtn
    global remove
    
    try:
        label7.place_forget()
        photo = ImageTk.PhotoImage(res_list[num])
        
        label7 = tk.Label(frame,image=photo)
        label7.image = photo
        label7.place(x=140,y=20)
        
        nextbtn = tk.Button(frame,text=">>", padx=10 , pady=5, fg="white", bg="grey", command=lambda: nextImg(num+1,frame))
        nextbtn.place(x=320, y=445)
        
        prevbtn = tk.Button(frame,text="<<", padx=10 , pady=5, fg="white", bg="grey", command=lambda: prevImg(num-1,frame))
        prevbtn.place(x=140, y=445)
        
        remove = tk.Button(frame,text="Delete Known", padx=10 , pady=5, fg="white", bg="grey", command=lambda: removeImg(num,frame))
        remove.place(x=195, y=445)
        
        if num <= 0:
            prevbtn["state"] = "disabled"
            print(prevbtn["state"])
    except:
        label8 = tk.Label(frame,text="No more known faces",bg="white",fg="red")
        label8.config(font=("Calibri", 12))
        label8.place(x=180, y=230)
        prevbtn = tk.Button(frame,text="<<", padx=10 , pady=5, fg="white", bg="grey", command=lambda: prevImg(num-1,frame))
        prevbtn.place(x=140, y=445)
        
        if num >= len(res_list):
            remove["state"] = "disabled"

def removeImg(num,frame):
    global label7
    global photo
    global nextbtn
    global remove

    try:
        im = image_list[num].filename
        os.remove(im)
        label7.place_forget()
        del res_list[num]
            
        label9 = tk.Label(frame,text="Known Face Deleted",bg="white",fg="red")
        label9.config(font=("Calibri", 12))
        label9.place(x=185, y=250)
    except:
        label9 = tk.Label(frame,text="Oops! Something Went Wrong!",bg="white",fg="red")
        label9.config(font=("Calibri", 12))
        label9.place(x=150, y=250)
def setMail():
    newWindow4 = tk.Toplevel(root)
    newWindow4.title("Set Sender & Reciever Email")
    newWindow4.resizable(False, False)
    newWindow4.geometry("+150+200")
    canvas4 = tk.Canvas(newWindow4,height=200,width=500,bg="white")
    canvas4.pack()
    frame5 = tk.Frame(newWindow4,bg="white")
    frame5.place(relwidth=1, relheight=1)
    label10 = tk.Label(frame5,text="Sender Email: ",bg="white")
    label10.config(font=("Calibri", 16))
    label10.place(x=100, y=20)
    text2 = ttk.Entry(frame5,width=15,textvariable=sysmail)
    text2.place(x=230, y=20)
    label11 = tk.Label(frame5,text="Password: ",bg="white")
    label11.config(font=("Calibri", 16))
    label11.place(x=120, y=50)
    text3 = ttk.Entry(frame5,width=15,textvariable=pw)
    text3.place(x=230, y=50)
    label12 = tk.Label(frame5,text="Your Email: ",bg="white")
    label12.config(font=("Calibri", 16))
    label12.place(x=110, y=80)
    text4 = ttk.Entry(frame5,width=15,textvariable=mymail)
    text4.place(x=230, y=80)
    submit = tk.Button(frame5,text="Submit", padx=10 , pady=5, fg="white", bg="grey", command=lambda:submitMail(frame5))
    submit.place(x=200, y=110)
    label5 = tk.Label(frame5,textvariable=msg,bg="white",fg="red")
    label5.config(font=("Calibri", 12))
    label5.place(x=100, y=150)
def submitMail(frame):
    try:
        #here you can access the email credentials and sender email
        smail = sysmail.get()
        password = pw.get()
        mail = mymail.get()
        msg.set(sysmail.get()+" "+pw.get()+" "+mymail.get())
        print(msg.get())
    except:
        msg.set("Something went wrong!")
        print(msg.get())
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
addKnown.place(x=30, y=130)

viewKnown = tk.Button(root,text="View Known", padx=10 , pady=5, fg="white", bg="grey", command=viewImages)
viewKnown.place(x=137, y=130)

delay = tk.Button(root,text="Select Delay", padx=10 , pady=5, fg="white", bg="grey", command=selectDelay)
delay.place(x=250, y=130)

setEmail = tk.Button(root,text="Set Email", padx=10 , pady=5, fg="white", bg="grey", command=setMail)
setEmail.place(x=366, y=130)

root.mainloop()