"""Software for table management in restaurants"""
from tkinter import Button, Label, Tk, Text, Entry, OptionMenu, StringVar, END
import json
from functools import partial

# pylint: disable = W0212, W0108, W0601, W0621, C0200, C0301, E1126


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

    if x_pos > boundry_object.winfo_x() and y_pos > boundry_object.winfo_y() and x_pos < (
            boundry_object.winfo_x() + boundry_object.winfo_width()) -\
            widget.winfo_width() and y_pos < boundry_object.winfo_y() + boundry_object.winfo_height():
        widget.place(x=x_pos, y=y_pos)


# GUI Generation Functions:

def load_home_page():
    """Home page creation code"""
    # Create Main Root
    global home_page_root
    home_page_root = Tk()
    home_page_root.title("Aterio")
    home_page_root.config(bg="#F2EFE9")
    home_page_root.attributes("-fullscreen", True)

    # Makes program name text
    aterio_text = Label(home_page_root, text="Aterio", width=71,
                        height=6, bg="#F06233", fg="#F2EFE9", font=("Arial", 35))
    aterio_text.pack()

    # Makes button to load table manager software
    table_manager_button = Button(home_page_root,
                                  text="Table Manager", command=lambda: load_table_managment(home_page_root), width=84,
                                  height=5, bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    table_manager_button.pack()

    # Makes button to load reservation manager software
    reservation_manager_button = Button(home_page_root,
                                        text="Reservation manager", command=lambda: warning_popup("Reservation manager is not currently available"), width=84, height=5, bg="#655A7C",
                                        fg="#F2EFE9", font=("Arial", 30))
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
    # Declares Global Variables
    global table_manager_root, orders_widget, waitstaff_box, table_identities, boundry_object, floorplan_button_identities, COLOUR_CHOICES

    # Creates Table Management root
    table_manager_root = Tk()
    table_manager_root.title("Aterio - Table Management")
    table_manager_root.attributes("-fullscreen", True)
    home_page_root.destroy()

    # Sets table and floorplan button trackers to []
    table_identities = []
    floorplan_button_identities = []

    # Declares List of Colours
    COLOUR_CHOICES = {
        "Blue": "#01295F",
        "Light Blue": "#437F97",
        "Green": "#849324",
        "Yellow": "#FFB30F",
        "Red": "#FD151B",
        "Black": "#393D3F",
        "Grey": "#C6C5B9",
        "Pink": "#EE959E",
        "Purple": "#9E7BB5"
    }

    # Creates widget to manage orders
    orders_widget = Text(table_manager_root, height=34, width=27, bg="#655A7C",
                         fg="#F2EFE9", font=("Arial", 20), insertbackground="#F2EFE9")
    orders_widget.place(x=0, y=0)

    # Creates widget to display waitstaff
    waitstaff_box = Text(table_manager_root, height=34, width=27, bg="#655A7C",
                         fg="#F2EFE9", font=("Arial", 20), insertbackground="#F2EFE9")
    waitstaff_box.place(x=390, y=0)

    # Creates the background bar behind floorplan buttons
    floorplan_buttons_background = Text(table_manager_root, blockcursor=True,
                                        state="disabled", bg="#655A7C", height=5, width=150)
    floorplan_buttons_background.place(x=800, y=0)

    # Creates button to allow user to add a floorplan
    create_new_floorplan_button = Button(table_manager_root,
                                         text="+ Floor", command=lambda: create_floorplan_interface(table_manager_root,
                                                                                                    orders_widget, waitstaff_box, floorplan_button_identities), bg="#AB92BF", fg="#F2EFE9",
                                         font=("Arial", 15))
    create_new_floorplan_button.place(x=1755, y=15)

    # Creates button to allow user to delete a floorplan
    delete_floorplan_button = Button(table_manager_root,
                                     text="- Floor", command=lambda: delete_floorplan_popup(table_manager_root,
                                                                                            orders_widget, waitstaff_box, floorplan_button_identities),
                                     bg="#AB92BF", fg="#F2EFE9", font=("Arial", 15))
    delete_floorplan_button.place(
        x=(1760+create_new_floorplan_button.winfo_reqwidth()), y=15)

    # Creates Boundry object for table drag and drop
    boundry_object = Text(table_manager_root, blockcursor=True,
                          state="disabled", bg="#F06233", height=80, width=150)
    boundry_object.place(x=800, y=75)

    global save_button
    # Creates save button
    save_button = Button(table_manager_root, text="Save", command=lambda:print("test"))
    save_button.place(x=1870, y=1045)

    # Creates buttons to load any exisiting floorplan
    generate_floorplan_buttons(table_manager_root, orders_widget,
                               waitstaff_box, floorplan_button_identities)

    # Creates back button
    back_button = Button(table_manager_root, text="Back", command=lambda: close_page(
        page_to_close=table_manager_root), bg="#690500", fg="#F2EFE9")
    back_button.place(x=10, y=1045)


# Tables functions:
def generate_tables(table_manager_root, floorplan, orders_widget, waitstaff_box, table_identities, save_button):
    """Generates each table from selected floorplan"""

    # Clears page
    clear_page(table_identities, orders_widget,
               floorplan_button_identities, waitstaff_box)

    # Loads "table.json" file
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        tables_object = json.load(tables_file)

        # Places all relevant info into waitstaff box
        waitstaff_box.config(state="normal")
        waitstaff_box.delete(1.0, END)
        waitstaff_box.insert(
            END, get_servers_on_floor(floorplan, "servers_key"))
        waitstaff_box.config(state="disabled")

        # Creates "new table" button
        create_new_table_button = Button(
            table_manager_root, text="Add Table", command=lambda: create_new_table_popup(floorplan))
        create_new_table_button.place(x=825, y=1045)

        # Iterates through floorplans in tables.json to find selected floorplan
        for floorplans in tables_object:
            if floorplans == floorplan:
                # Iterates through tables in chosen floorplan
                for tables in tables_object[floorplans]:
                    # Dispplays current table in orders box
                    orders_widget.insert(END, f"{tables}:\n\n\n")
                    # Creates button for current table at saved coordinates.
                    new_table = Button(table_manager_root, text=tables, fg="white",
                                       bg=tables_object[floorplans][tables]["colour"],
                                       command=partial(config_table_gui, floorplan, tables, tables_object[floorplans][tables]["colour"], tables_object[floorplans][tables]["server"]))
                    new_table.place(x=tables_object[floorplans][tables]["x"],
                                    y=tables_object[floorplans][tables]["y"])
                    # Gives table drag and drop properties
                    make_draggable(new_table)
                    # Adds table to table tracker list
                    table_identities.append(new_table)
    save_button.config(command=lambda: save_tables(floorplan, table_identities))

def create_new_table_popup(floorplan):
    """User Interface for table creation"""
    # Creates table creation prompt
    new_table_prompt = Tk()
    new_table_prompt.title("Create a Table")
    new_table_prompt.geometry("330x100")

    # Creates drop down menu for servers on floor
    server_default = StringVar(new_table_prompt)
    server_default.set(get_servers_on_floor(floorplan, "servers_list")[0])
    options = get_servers_on_floor(floorplan, "servers_list")
    table_server = OptionMenu(
        new_table_prompt, server_default, options[0], * options)
    table_server.place(x=0, y=59)

    # Creates drop down menu for colours on floor
    colour_default = StringVar(new_table_prompt)
    colour_default.set("")
    options2 = COLOUR_CHOICES
    table_colour = OptionMenu(
        new_table_prompt, colour_default, * options2)
    table_colour.place(x=0, y=30)

    # Creates submit button
    submit_button = Button(new_table_prompt, text="Submit", bg="#AB92BF", fg="#F2EFE9",
                           command=lambda: create_new_table(new_table_prompt, floorplan, table_name, server_default,
                                                            table_x, table_y, colour_default))
    submit_button.place(x=280, y=0)

    # Creates cancel button
    cancel_button = Button(new_table_prompt, text="Cancel", bg="#690500",
                           fg="#F2EFE9", command=lambda: new_table_prompt.destroy())
    cancel_button.place(x=280, y=30)

    # Creates button to confirm table creation
    add_server = Button(new_table_prompt, text="Add Server", bg="#AB92BF", fg="#F2EFE9",
                        command=lambda: create_server_for_floor(new_table_prompt, floorplan, table_name,
                                                                table_x, table_y, submit_button, add_server, colour_default, table_server))
    add_server.place(x=table_server.winfo_reqwidth(), y=60)

    # Creates prompt for user to enter tables name
    table_name = Entry(new_table_prompt, width=25, font=("Arial", 15))
    table_name.insert(END, "(New Table Name)")
    table_name.place(x=0, y=0)

    # Sets default coordinates
    table_x = int("825")
    table_y = int("100")


def create_server_for_floor(new_table_prompt, floorplan, table_name, table_x, table_y, submit_button, add_server, colour_default, table_server):
    """Allows user to create a new server for a table through the table creation popup"""
    # Generates Text box for a new server creation
    new_server = Entry(new_table_prompt, width=25, font=("Arial", 15))
    new_server.insert(END, "(New Server Name)")
    new_server.place(x=0, y=60)
    # Edits submit button to load correct information and removes old buttons
    submit_button.config(command=lambda: create_new_table(
        new_table_prompt, floorplan, table_name, new_server, table_x, table_y, colour_default))
    add_server.place_forget()
    table_server.place_forget()


def create_new_table(popup_root, floorplan, table_name, table_server, table_x, table_y, colour_default):
    """Gets and saves user inputted information for new table being created"""
    # Gets user input for buttons
    server = table_server.get()
    colour = colour_default.get()
    new_table_info = {
        "x": table_x,
        "y": table_y,
        "server": server,
        "colour": COLOUR_CHOICES[colour]
    }
    # Writes new input to save file
    with open("tables.json", "r", encoding="utf-8") as table_object_read:
        tables_read = json.load(table_object_read)
        for floorplans in tables_read:
            if floorplans == floorplan:
                if not table_name.get() in tables_read[floorplan]:
                    tables_read[floorplan][table_name.get()] = {}
                else:
                    warning_popup("Table Already Exists")
                tables_read[floorplan][table_name.get()].update(
                    new_table_info)
        added_table = json.dumps(tables_read, indent=4)
    with open("tables.json", "w", encoding="utf-8") as tables_object_write:
        tables_object_write.write(added_table)
    popup_root.destroy()


def config_table_gui(floorplan, table_name, table_colour, table_server):
    """Allows user to config a table"""
    config_table_popup = Tk()
    config_table_popup.title(f"Configure {table_name}")
    config_table_popup.geometry("330x100")

    table_name_entry = Entry(
        config_table_popup, width=25, font=("Arial", 15))
    table_name_entry.insert(END, table_name)
    table_name_entry.place(x=0, y=0)

    colour_default = StringVar(config_table_popup)
    colour_default.set("")
    options2 = COLOUR_CHOICES
    table_colour = OptionMenu(
        config_table_popup, colour_default, * options2)
    table_colour.place(x=0, y=table_name_entry.winfo_reqheight())

    table_server_entry = Entry(
        config_table_popup, width=25, font=("Arial", 15))
    table_server_entry.insert(END, table_server)
    table_server_entry.place(x=0, y=(
        table_name_entry.winfo_reqheight()+table_colour.winfo_reqheight()))

    cancel_button = Button(config_table_popup, text="Cancel",
                           command=lambda: config_table_popup.destroy())
    cancel_button.place(x=table_name_entry.winfo_reqwidth(), y=0)

    submit_button = Button(config_table_popup, text="Submit", command=lambda: config_table(
        floorplan, table_name_entry, colour_default, table_server_entry, table_name, config_table_popup))
    submit_button.place(x=table_name_entry.winfo_reqwidth(),
                        y=cancel_button.winfo_reqheight())


def config_table(floorplan, table_name_entry, colour_default, table_server_entry, table_name, config_table_popup):
    """Saves configurements to json file"""
    existing_table_name = table_name
    # Sets user input to new var name.
    new_table_name = table_name_entry.get()
    new_table_colour = COLOUR_CHOICES[colour_default.get()]
    new_table_server = table_server_entry.get()
    with open("tables.json", "r", encoding="utf-8") as tables_config_obj:
        tables_config = json.load(tables_config_obj)
        for floorplans in tables_config:
            if floorplans == floorplan:
                for tables in tables_config[floorplans]:
                    if tables == existing_table_name:
                        # Finds table to configure and edits server name and colour.
                        tables_config[floorplans][tables]["server"] = new_table_server
                        tables_config[floorplans][tables]["colour"] = new_table_colour
                        # Replaces table name with new table name and deletes old one.
                        if not new_table_name == existing_table_name:
                            tables_config[floorplans][new_table_name] = tables_config[floorplans][tables]
                            del tables_config[floorplans][tables]
                        config_table_popup.destroy()
                        break
    # Saves table name and content to json file.
    with open("tables.json", "w", encoding="utf-8") as tables_config_write:
        to_write = json.dumps(tables_config, indent=4)
        tables_config_write.write(to_write)
    clear_page(table_identities, orders_widget,
               floorplan_button_identities, waitstaff_box)
    generate_tables(table_manager_root, floorplan, orders_widget,
                    waitstaff_box, table_identities, save_button)
    generate_floorplan_buttons(
        table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities)


def clear_page(table_identities, orders_widget, floorplan_button_identities, waitstaff_box):
    """Clears loaded page"""
    num_of_tables = len(table_identities)
    clear_floorplan_buttons(table_manager_root, orders_widget,
                            waitstaff_box, floorplan_button_identities)
    for tables in range(num_of_tables):
        print(num_of_tables)
        table_identities[tables].destroy()
        orders_widget.delete("1.0", END)
        waitstaff_box.delete("1.0", END)
    for i in range(num_of_tables):
        table_identities.remove(table_identities[i-1])

def save_tables(floorplan, table_identities):
    """Saves tables"""
    table_number = 0
    with open("tables.json", "r", encoding="utf-8") as tables_object:
        tables_list = json.load(tables_object)
        for floors in tables_list:
            if floors == floorplan:
                for tables in tables_list[floorplan]:
                    if table_identities[table_number]["text"] == tables:
                        current_table = table_identities[table_number]
                        current_table_name = table_identities[table_number]["text"]
                        tables_list[floorplan][current_table_name]["x"] = current_table.winfo_x(
                        )
                        tables_list[floorplan][current_table_name]["y"] = current_table.winfo_y(
                        )
                    table_number += 1
    updated_table = json.dumps(tables_list, indent=4)
    with open("tables.json", "w", encoding="utf-8") as tables_object_w:
        tables_object_w.write(updated_table)

# Waitstaff functions:
def get_servers_on_floor(floorplan, return_type, *server):
    """Loads and displays the servers on floorplan"""
    servers_list = []
    servers_colour = []
    server_info = []
    current_server = ""
    # Loads "tables.json" file
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        tables_object = json.load(tables_file)
        # Iterates through each floorplan in "tables.json"
        for floorplans in tables_object:
            if floorplans == floorplan:
                for tables in tables_object[floorplans]:
                    current_server = tables_object[floorplans][tables]["server"]
                    if not current_server in servers_list:
                        servers_list.append(current_server)
                        servers_colour.append(
                            tables_object[floorplans][tables]["colour"])
    if return_type == "servers_list":
        if not servers_list:
            servers_list.append("Please add a server to this floor")
            return servers_list
        else:
            return servers_list
    if return_type == "servers_key":
        for i in range(len(servers_list)):
            server_info.append(f"{servers_list[i]}: {list(COLOUR_CHOICES.keys())[list(COLOUR_CHOICES.values()).index(servers_colour[i])]}\n")
        return "".join(server_info)
    if return_type == "servers_color":
        return server_info[server]


# Floorplan functions:
def generate_floorplan_buttons(table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities,):
    """Generates buttons to load each saved floorplan"""
    iterating_x_pos = 0
    # Loads "table.json" file
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        tables_object = json.load(tables_file)
        # Iterates through floorplans in "table.json" file and creates button to load each floorplan
        for floorplan in tables_object:
            new_floorplan_button = Button(
                table_manager_root, text=floorplan, font=("Arial", 15))
            new_floorplan_button.config(command=partial(
                generate_tables, table_manager_root, floorplan, orders_widget, waitstaff_box, table_identities, save_button))
            # Places button and updates x position to make buttons evenly spaced apart
            new_floorplan_button.place(x=(825 + iterating_x_pos), y=15)
            iterating_x_pos += (new_floorplan_button.winfo_reqwidth() + 15)
            floorplan_button_identities.append(new_floorplan_button)


def clear_floorplan_buttons(table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities):
    """Function to delete and regenerate floorplan buttons when new floorplan is created"""
    for floorplans in range(len(floorplan_button_identities)):
        floorplan_button_identities[floorplans].destroy()
    floorplans = []
    generate_floorplan_buttons(
        table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities)


def create_floorplan_interface(table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities):
    """User interface for floorplan creation"""
    create_floorplan_popup = Tk()
    create_floorplan_popup.title("Create New Floorplan")
    create_floorplan_popup.geometry("350x100")

    floorplan_name = Entry(create_floorplan_popup,
                           width=25, font=("Arial", 15))
    floorplan_name.insert(END, "(New Floorplan Name)")

    submit_button = Button(create_floorplan_popup, text="Submit", bg="#AB92BF", fg="#F2EFE9",
                           command=lambda: create_floorplan(floorplan_name, create_floorplan_popup, table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities))
    floorplan_name.place(x=0, y=0)
    submit_button.place(x=275, y=0)


def create_floorplan(floorplan_name, popup_root, table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities):
    """Saves requested floorplan to json file"""
    with open("tables.json", "r", encoding="utf-8") as tables_object_read:
        tables = json.load(tables_object_read)
        if not floorplan_name.get() in tables:
            tables[floorplan_name.get()] = {}
        else:
            warning_popup("Floorplan Already Exists")
        new_floorplan = json.dumps(tables, indent=4)
    with open("tables.json", "w", encoding="utf-8") as tables_object_write:
        tables_object_write.write(new_floorplan)
    popup_root.destroy()
    clear_floorplan_buttons(table_manager_root, orders_widget,
                            waitstaff_box, floorplan_button_identities)


def get_floorplans():
    """Creates a list containing each floorplan in the tables.json file"""
    floorplan_list = []
    with open("tables.json", "r", encoding="utf-8") as tables_object:
        tables = json.load(tables_object)
        for floorplans in tables:
            floorplan_list.append(floorplans)
    return floorplan_list


def delete_floorplan_popup(table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities):
    """Generates a popup that allows the user to deleta/remove a created floorplan"""
    delete_floorplan_popup_root = Tk()
    delete_floorplan_popup_root.title("Remove a Floorplan")
    delete_floorplan_popup_root.geometry("350x100")

    floorplan_default = StringVar(delete_floorplan_popup_root)
    floorplan_default.set(get_floorplans()[0])
    options = get_floorplans()
    floorplan_to_delete = OptionMenu(
        delete_floorplan_popup_root, floorplan_default, options[0], * options)
    floorplan_to_delete.place(x=0, y=0)

    submit_button = Button(delete_floorplan_popup_root, text="Submit",
                           command=lambda: delete_floorplan(delete_floorplan_popup_root, floorplan_default.get(),
                                                            table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities))
    submit_button.place(x=(floorplan_to_delete.winfo_reqwidth()), y=0)


def delete_floorplan(delete_floorplan_popup_root, floorplan_to_delete, table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities):
    """Uses information from popup to remove the selected floorplan from the tables.json file"""
    with open("tables.json", "r", encoding="utf-8") as tables_object:
        tables = json.load(tables_object)
        for floorplans in tables:
            if floorplans == floorplan_to_delete:
                tables.pop(floorplan_to_delete)
                removed_floorplan = json.dumps(tables, indent=4)
                with open("tables.json", "w", encoding="utf-8") as tables_object_write:
                    tables_object_write.write(removed_floorplan)
                    delete_floorplan_popup_root.destroy()
                break
    clear_floorplan_buttons(table_manager_root, orders_widget,
                            waitstaff_box, floorplan_button_identities)

# Popup Functions:
def warning_popup(warning):
    """Function to create generic popups when needed"""
    warning_popup_root = Tk()
    warning_popup_root.geometry("250x250")
    warning_popup_root.title(f"{warning}")

    warning_text = Label(warning_popup_root, text=warning)
    cancel_button = Button(warning_popup_root, text="Cancel",
                           command=lambda: warning_popup_root.destroy())

    warning_text.place(x=0, y=0)
    cancel_button.place(x=0, y=warning_text.winfo_reqheight())

load_home_page()
