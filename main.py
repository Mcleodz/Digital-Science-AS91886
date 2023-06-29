# pylint: disable=W0212, W0601, W0108, C0114
from tkinter import Button, Label, Tk, Text, END
import json


def make_draggable(widget):
    """Drag and Drop Function - 1"""
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)


def on_drag_start(event):
    """Drag and Drop Function - 2"""
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y


def on_drag_motion(event):
    """Drag and Drop Function - 3"""
    widget = event.widget
    x_pos = widget.winfo_x() - widget._drag_start_x + event.x
    y_pos = widget.winfo_y() - widget._drag_start_y + event.y
    if x_pos > boundry_object.winfo_x() and y_pos > boundry_object.winfo_y() and x_pos < (boundry_object.winfo_x() + boundry_object.winfo_width())-widget.winfo_width() and y_pos < boundry_object.winfo_y() + boundry_object.winfo_height():
        widget.place(x=x_pos, y=y_pos)


def load_home_page():
    """Home page creation code"""
    # Create Main Root
    home_page_root = Tk()
    home_page_root.title("Aterio")
    home_page_root.config(bg="#F2EFE9")
    home_page_root.attributes("-fullscreen", True)

    # Makes program name text
    aterio_text = Label(home_page_root, text="Aterio", width=71,
                        height=6, bg="#F06233", fg="#F2EFE9", font=("Arial", 35))
    aterio_text.pack()

    # Makes button to load table manager software
    table_manager_button = Button(home_page_root, text="Table Manager", command=lambda: load_table_managment(
        home_page_root), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    table_manager_button.pack()

    # Makes button to load reservation manager software
    reservation_manager_button = Button(home_page_root, text="Reservation manager", command=lambda: print(
        "hi"), width=84, height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    reservation_manager_button.pack()

    # Makes button to quit program
    quit_button = Button(home_page_root, text="Quit", command=lambda: quit(),
                         width=84, height=5, bg="#690500", fg="#F2EFE9", font=("Arial", 30))
    quit_button.pack()

    home_page_root.mainloop()


def close_page(page_to_close):
    """Closes currently opened tab"""
    page_to_close.destroy()
    load_home_page()


def load_table_managment(home_page_root):
    """Loads the table manager page"""
    # Creates Table Management root
    table_manager_root = Tk()
    table_manager_root.title("Aterio - Table Management")
    table_manager_root.attributes("-fullscreen", True)
    home_page_root.destroy()

    # Creates Orders widget
    orders_widget = Text(table_manager_root, height=34, width=40, bg="#655A7C",
                         fg="#F2EFE9", font=("Arial", 20), insertbackground="#F2EFE9")
    orders_widget.place(x=0, y=0)

    # Creates Boundry object for table drag and drop
    global boundry_object
    boundry_object = Text(table_manager_root, blockcursor=True,
                          state="disabled", bg="#F06233", height=80, width=150)
    boundry_object.place(x=800, y=75)

    generate_floorplan_buttons(table_manager_root, orders_widget)

    # Makes Back button
    back_button = Button(table_manager_root, text="Back", command=lambda: close_page(
        page_to_close=table_manager_root), bg="#690500", fg="#F2EFE9")
    back_button.place(x=0, y=1054)


def generate_tables(table_manager_root, orders_widget, floorplan):
    """Generates each table from selected floorplan"""
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        # Loads table json file
        tables_object = json.load(tables_file)
        # Iterates through floorplans
        for floorplans in tables_object:
            # Checks if floorplan is specified floor
            if floorplans == floorplan:
                # Iterates through each table on floor plan
                for tables in tables_object[floorplans]:
                    orders_widget.insert(END, f"{tables}:\n\n")
                    new_table = Button(table_manager_root, text=tables, fg="white",
                                       bg=tables_object[floorplans][tables]["colour"])
                    new_table.place(
                        x=tables_object[floorplans][tables]["x"], y=tables_object[floorplans][tables]["y"])
                    make_draggable(new_table)


def generate_floorplan_buttons(table_manager_root, orders_widget):
    """Generates buttons to load each saved floorplan"""
    iterating_x_pos = 0
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        tables_object = json.load(tables_file)
        for floorplan_to_generate in tables_object:
            #! Floorplan that loads is always the last floorplan in tables
            new_floorplan_button = Button(table_manager_root, text=floorplan_to_generate,
                                          command=lambda: generate_tables(table_manager_root, orders_widget, floorplan=floorplan_to_generate), font=("Arial", 15))
            new_floorplan_button.place(x=(800 + iterating_x_pos), y=15)
            iterating_x_pos += (new_floorplan_button.winfo_reqwidth() + 15)


load_home_page()
