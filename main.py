from tkinter import *
import json

# Declaring global variables
table_count = 0
table_identites = []

"""Drag and Drop Functions:"""
def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    if x > boundry_object.winfo_x() and  y > boundry_object.winfo_y() and  x < (boundry_object.winfo_x() + boundry_object.winfo_width())-widget.winfo_width() and  y < boundry_object.winfo_y() + boundry_object.winfo_height():
        widget.place(x=x, y=y)

"""Home page creation code"""
def load_home_page():
    #Create Main Root
    home_page_root = Tk()
    home_page_root.title("Aterio")
    home_page_root.config(bg="#F2EFE9")
    home_page_root.attributes("-fullscreen", True)

    # Makes program name text
    aterio_text = Label(home_page_root, text="Aterio", width=71, height=6, bg="#F06233", fg="#F2EFE9", font=("Arial", 35))
    aterio_text.pack()

    # Makes button to load table manager software
    table_manager_button = Button(home_page_root, text="Table Manager", command=lambda:load_table_managment(home_page_root), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    table_manager_button.pack()

    # Makes button to load reservation manager software
    reservation_manager_button = Button(home_page_root, text="Reservation manager", command=lambda:print("hi"), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    reservation_manager_button.pack()

    # Makes button to quit program
    quit_button = Button(home_page_root, text= "Quit", command=lambda:quit(), width=84, height=5, bg="#690500", fg="#F2EFE9", font=("Arial", 30))
    quit_button.pack()

    home_page_root.mainloop()

"""Close page"""
def close_page(page_to_close):
    page_to_close.destroy()
    load_home_page()

"""Table Manager Page"""
def load_table_managment(home_page_root):
    # Creates Table Management root
    table_manager_root = Tk()
    table_manager_root.title("Aterio - Table Management")
    table_manager_root.attributes("-fullscreen", True)
    home_page_root.destroy()

    generate_floorplan_buttons(table_manager_root)

    # Creates Boundry object for table drag and drop
    global boundry_object
    boundry_object = Text(table_manager_root, blockcursor=True, state="disabled", bg="#F06233", height=70, width=150)
    boundry_object.place(x=800, y=100)

    # Creates Orders widget
    orders_widget = Text(table_manager_root, height=34, width=40, bg="#655A7C", fg="#F2EFE9", font=("Arial", 20), insertbackground="#F2EFE9")
    orders_widget.insert(END, "Table:")
    orders_widget.place(x=0,y=0)

    # Makes Back button
    back_button = Button(table_manager_root, text="Back", command=lambda:close_page(page_to_close=table_manager_root), bg="#690500", fg="#F2EFE9")
    back_button.place(x=0, y=1054)

"""Getting Table Information"""
def generate_tables(table_manager_root, floorplan):
    with open("tables.json", "r") as tables_file:
        # Loads table json file
        tables_object = json.load(tables_file)
        # Iterates through floorplans
        for floorplans in tables_object:
            # Checks if floorplan is specified floor
            if floorplans == floorplan:
                # Iterates through each table on floor plan
                for tables in tables_object[floorplans]:
                    new_table = Button(table_manager_root, text=tables, fg="white", bg = tables_object[floorplans][tables]["colour"])
                    new_table.place(x=tables_object[floorplans][tables]["x"], y=tables_object[floorplans][tables]["y"])
                    make_draggable(new_table)

def generate_floorplan_buttons(table_manager_root):
    iterating_x_pos = 0
    with open("tables.json", "r") as tables_file:
        tables_object = json.load(tables_file)
        for floorplans in tables_object:
            new_floorplan_button = Button(table_manager_root, text=floorplans, font=("Arial", 15))
            new_floorplan_button.place(x=(1000 + iterating_x_pos), y=25)
            iterating_x_pos += 100
            print(new_floorplan_button["text"])


load_home_page()