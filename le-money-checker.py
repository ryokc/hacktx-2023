import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from roboflow import Roboflow
import json

import asyncio
import threading
import time

import customtkinter

import pyttsx3

class CameraApp:
    def __init__(self, root):

        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        self.root = root
        self.root.title("Camera App")
        self.root.configure(background="#2b2b2b")
        self.root.geometry("1600x1100")
        self.cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(self.root, bg_color="black")



        self.main_frame.grid(row=0, column=0)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        title_label = tk.Label(self.main_frame, text="Scaney Money", font=("Helvetica", 24),foreground="white",background="#2b2b2b")
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        self.video1_label = ttk.Label(self.main_frame, width= 700)
        self.video1_label.grid(row=1, column=0)

        self.video2_label = ttk.Label(self.main_frame, width= 700)
        self.video2_label.grid(row=1, column=1)

        self.integer_label = customtkinter.CTkLabel(self.main_frame, text="Total: 0", text_color="#FFFFFF", font=("Helvetica", 24))
        self.integer_label.grid(row=2, column=0, pady=10)

        self.integer_label2 = customtkinter.CTkLabel(self.main_frame, text="Classification Output: 0", text_color="#FFFFFF", width= 700, font=("Helvetica", 24))
        self.integer_label2.grid(row=2, column=1, pady=10)
        
        self.capture_button = customtkinter.CTkButton(self.main_frame, text="Input", command=self.input)
        self.capture_button.grid(row=3, column=0, pady=10,ipadx=100, ipady=50)
        
        self.exit_button = customtkinter.CTkButton(self.main_frame, text="Output", command=self.output)
        self.exit_button.grid(row=4, column=0, pady=10,ipadx=100, ipady=50)

        self.rf = Roboflow(api_key="fTR9oznM3hehEtAWXLzL")
        self.project = self.rf.workspace("alex-hyams-cosqx").project("cash-counter")
        self.model = self.project.version(10).model

        self.engine = pyttsx3.init()

        self.amount = 0
        self.value_dictionary = {'penny': .01, 'nickel': .05, 'dime': .1, 'quarter': .25, 'one': 1, 'five': 5, 'ten': 10, 'twenty': 20, 'fifty': 50, 'hundred': 100}
        self.lock = threading.Lock()

        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (660, 540))
        self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.video2_label.config(image=self.photo2)
        self.video2_label.image = self.photo2
        self.update()

    def talk(self, message):
        with self.lock:
            self.engine.say(message)
            self.engine.runAndWait()

    def update_amount(self, deposit):

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (660, 540))
            file_path = "snapshot.jpg"  # Default file name
            cv2.imwrite(file_path, frame)
            print(f"Snapshot saved as {file_path} in the current directory")

        package = self.model.predict("snapshot.jpg", confidence=50, overlap=50).json()
        print(package)

        toadd = 0
        s = ""
        for i in range(len(package['predictions'])):
            p = package['predictions'][i]
            x = p['class'].split("-")[0].lower()
            if i == 0:
                s = s + p['class'].replace("-", " ")
            else:
                s = s + ", and " + p['class'].replace("-", " ")
            print(x)
            #with self.lock:
            w2 = p['width']//2
            h2 = p['height']//2
            frame = cv2.rectangle(frame, (p['x']-w2, p['y']-h2),(p['x']+w2, p['y']+h2), color=(255, 0, 0), thickness=2)
            frame = cv2.putText(frame, p['class'], (p['x']-w2+2, p['y']-h2+12), cv2.FONT_HERSHEY_COMPLEX_SMALL , .5, (255, 0, 0), 1, cv2.LINE_AA) 

            toadd = self.value_dictionary[x] + round(toadd,2)
        
        t = threading.Thread(target=self.talk, args=(s,))
        t.daemon = True
        t.start()
        self.integer_label2.configure(text=f"Classification Output: {round(toadd,2)}")  
        
        if deposit:
            self.amount = self.amount + toadd
        else:
            self.amount = self.amount - toadd
        
        self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.video2_label.config(image=self.photo2)
        self.video2_label.image = self.photo2
        


    

    def update(self):
        #with self.lock:
        ret, frame = self.cap.read()
        if ret:
           
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (660, 540))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video1_label.config(image=self.photo)
            self.video1_label.image = self.photo
            self.integer_label.configure(text=f"Total: {round(self.amount,2)}")
            
        self.video1_label.after(10, self.update)

    
    
    def input(self):      
        background_thread = threading.Thread(target=self.update_amount(True))
        background_thread.daemon = True  # This allows the thread to exit when the main program exits
        background_thread.start()
        
       
    
    def output(self):
        background_thread = threading.Thread(target=self.update_amount(False))
        background_thread.daemon = True  # This allows the thread to exit when the main program exits
        background_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()