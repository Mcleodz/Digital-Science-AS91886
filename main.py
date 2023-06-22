from tkinter import *
import json

root = Tk()
root.title("Aterio")
root.config(bg="#F2EFE9")
root.attributes("-fullscreen", True)

aterio_text = Button(root, text="Aterio")

table_manager_button = Button(root, text="Table Manager", command=lambda:print("hi"), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
table_manager_button.place(x=0, y=303)

reservation_manager_button = Button(root, text="Reservation manager", command=lambda:print("hi"), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
reservation_manager_button.place(x=0, y=562)

quit_button = Button(root, text= "Quit", command=lambda:quit(), width=84, height=5, bg="#690500", fg="#F2EFE9", font=("Arial", 30))
quit_button.place(x=0, y=821)

root.mainloop()