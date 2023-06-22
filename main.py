from tkinter import *
import json


"""Create Main Root"""
root = Tk()
root.title("Aterio")
root.config(bg="#F2EFE9")
root.attributes("-fullscreen", True)

"""Home page creation code"""
def load_home_page(root):
    # Makes home frame for hompage GUI
    home_page = Frame(root)
    home_page.pack()

    # Makes program name text
    aterio_text = Label(home_page, text="Aterio", width=71, height=6, bg="#F06233", fg="#F2EFE9", font=("Arial", 35))
    aterio_text.pack()

    # Makes button to load table manager software
    table_manager_button = Button(home_page, text="Table Manager", command=lambda:load_table_managment(root, home_page), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    table_manager_button.pack()

    # Makes button to load reservation manager software
    reservation_manager_button = Button(home_page, text="Reservation manager", command=lambda:print("hi"), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    reservation_manager_button.pack()

    # Makes button to quit program
    quit_button = Button(home_page, text= "Quit", command=lambda:quit(), width=84, height=5, bg="#690500", fg="#F2EFE9", font=("Arial", 30))
    quit_button.pack()

"""Close page"""
def close_page(root, page_to_close):
    page_to_close.destroy()
    load_home_page(root)

"""Table Manager code"""
def load_table_managment(root, home_page):
    # Makes table manager page and destroys old page
    home_page.destroy()
    table_management_page = Frame(root)
    table_management_page.pack()

    back_button = Button(table_management_page, text="Back", command=lambda:close_page(root, page_to_close=table_management_page))
    back_button.place(x=0, y=0)

load_home_page(root)

root.mainloop()