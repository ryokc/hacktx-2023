import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from roboflow import Roboflow
import json
import threading

import customtkinter

class CameraApp:
    def __init__(self, root):

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.root = root
        self.root.title("Camera App")
        
        self.cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera
        
        self.main_frame = customtkinter.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0)
        
        self.video_label = ttk.Label(self.main_frame)
        self.video_label.grid(row=0, column=0)

        self.integer_label = customtkinter.CTkLabel(self.main_frame, text="Balance: 0", text_color="white")
        self.integer_label.grid(row=3, column=0, pady=10)
        
        self.capture_button = customtkinter.CTkButton(self.main_frame, text="Input", command=self.input)
        self.capture_button.grid(row=1, column=0, pady=10)
        
        self.exit_button = customtkinter.CTkButton(self.main_frame, text="Output", command=self.output)
        self.exit_button.grid(row=2, column=0, pady=10)

        self.rf = Roboflow(api_key="fTR9oznM3hehEtAWXLzL")
        self.project = self.rf.workspace("alex-hyams-cosqx").project("dollar-bill-detection")
        self.model = self.project.version(20).model

        self.amount = 0
        self.value_dictionary = {'penny': .01, 'nickel': .05, 'dime': .1, 'quarter': .25, 'one': 1, 'five': 5, 'ten': 10, 'twenty': 20, 'fifty': 50, 'hundred': 100}
        self.lock = threading.Lock()

        self.update()

    def update_amount(self, deposit):
        ret, frame = self.cap.read()
        if ret:
            file_path = "snapshot.jpg"  # Default file name
            cv2.imwrite(file_path, frame)
            print(f"Snapshot saved as {file_path} in the current directory")

        package = self.model.predict("snapshot.jpg", confidence=50, overlap=50).json()

        for p in package['predictions']:
            x = p['class'].split("-")[0].lower()
            print(x)
            #with self.lock:
            if deposit:
                self.amount = self.amount + self.value_dictionary[x]
            else:
                self.amount = self.amount - self.value_dictionary[x]

    

    def update(self):
        #with self.lock:
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video_label.config(image=self.photo)
            self.video_label.image = self.photo
            self.integer_label.configure(text=f"Balance: {self.amount}")
        self.video_label.after(10, self.update)

    
    
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
