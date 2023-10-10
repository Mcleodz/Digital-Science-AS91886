"""Software for table management in restaurants"""
from tkinter import Button, Label, Tk, Text, Entry, OptionMenu, StringVar, END
import json
from functools import partial

# pylint: disable= C0200, C0301, W0212, W0601, W0108

# The following are the functions that allow drag and drop to work.
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
            boundry_object.winfo_x() + boundry_object.winfo_width()) - widget.winfo_width() and (
            y_pos < boundry_object.winfo_y() + boundry_object.winfo_height()):
        widget.place(x=x_pos, y=y_pos)


# GUI Generation Functions:

def load_home_page():
    """Home page creation code"""

    # Declaring Screen size constants for auto sizing the GUI.
    global DEVICE_HEIGHT, DEVICE_WIDTH, CHARACTER_WIDTH_CONSTANT, home_page_root

    # Creates home page for Aterio
    home_page_root = Tk()
    home_page_root.title("Aterio")
    home_page_root.config(bg="#F2EFE9")
    home_page_root.attributes("-fullscreen", True)

    DEVICE_HEIGHT = home_page_root.winfo_screenheight()
    DEVICE_WIDTH = home_page_root.winfo_screenwidth()
    CHARACTER_WIDTH_CONSTANT = round(DEVICE_WIDTH/8)

    # Makes program name text
    aterio_text = Label(home_page_root, text="Aterio",
                        bg="#F06233", fg="#F2EFE9", font=("Arial", 35))
    aterio_text.pack(fill="both", expand=True)

    # Makes button to load table manager software
    table_manager_button = Button(home_page_root,
                                  text="Table Manager", command=lambda: load_table_managment(
                                      home_page_root), bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))
    table_manager_button.pack(fill="both", expand=True)

    # Makes button to load reservation manager software
    reservation_manager_button = Button(home_page_root,
                                        text="Reservation manager", command=lambda: warning_popup(
                                            "Reservation manager is not currently available"),
                                        bg="#655A7C", fg="#F2EFE9", font=("Arial", 30))

    reservation_manager_button.pack(fill="both", expand=True)

    # Makes button to quit program
    quit_button = Button(home_page_root, text="Quit", command=lambda: quit(
    ), bg="#690500", fg="#F2EFE9", font=("Arial", 30))
    quit_button.pack(fill="both", expand=True)

    home_page_root.mainloop()


def close_page(page_to_close):
    """Closes currently opened tab"""
    # Closes selected paged and opens the home page
    page_to_close.destroy()
    load_home_page()


def load_table_managment(root_to_destroy):
    """Loads the table manager page"""
    # Declares Global Variables
    global table_manager_root, orders_widget, waitstaff_box, table_identities, save_button
    global floorplan_buttons_bg, boundry_object, floorplan_button_identities, COLOUR_CHOICES

    # Creates Table Management page
    table_manager_root = Tk()
    table_manager_root.title("Aterio - Table Management")
    table_manager_root.attributes("-fullscreen", True)
    root_to_destroy.destroy()

    # Sets table and floorplan button trackers to []
    table_identities = []
    floorplan_button_identities = []

    # Declares Colour options for tables
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
    orders_widget = Text(table_manager_root, height=DEVICE_HEIGHT,
                         width=int(round(CHARACTER_WIDTH_CONSTANT/10)), bg="#655A7C",
                         fg="#F2EFE9", font=("Arial", 20), insertbackground="#F2EFE9")
    orders_widget.place(x=0, y=0)

    # Creates widget to display waitstaff
    waitstaff_box = Text(table_manager_root, height=DEVICE_HEIGHT,
                         width=int(round(CHARACTER_WIDTH_CONSTANT/10)), bg="#655A7C",
                         fg="#F2EFE9", font=("Arial", 20), insertbackground="#F2EFE9")
    waitstaff_box.place(x=(0+orders_widget.winfo_reqwidth()), y=0)

    # Creates the background bar behind floorplan buttons
    floorplan_buttons_bg = Text(table_manager_root, blockcursor=True, state="disabled", bg="#655A7C",
                                height=5, width=round((orders_widget.winfo_reqwidth() +
                                                       waitstaff_box.winfo_reqwidth()) - CHARACTER_WIDTH_CONSTANT))
    floorplan_buttons_bg.place(
        x=(orders_widget.winfo_reqwidth()+waitstaff_box.winfo_reqwidth()), y=0)

    # Creates button to allow user to add a floorplan
    create_new_floorplan_button = Button(table_manager_root,
                                         text="+ Floor", command=lambda: create_floorplan_interface(
                                             table_manager_root, orders_widget, waitstaff_box,
                                             floorplan_button_identities),
                                         bg="#AB92BF", fg="#F2EFE9", font=("Arial", 15))
    create_new_floorplan_button.place(x=DEVICE_WIDTH-create_new_floorplan_button.winfo_reqwidth() -
                                      create_new_floorplan_button.winfo_reqwidth()-30, y=15)

    # Creates button to allow user to delete a floorplan
    delete_floorplan_button = Button(table_manager_root,
                                     text="- Floor", command=lambda: delete_floorplan_popup(
                                        orders_widget, waitstaff_box, floorplan_button_identities),
                                     bg="#690500", fg="#F2EFE9", font=("Arial", 15))
    delete_floorplan_button.place(
        x=(DEVICE_WIDTH-create_new_floorplan_button.winfo_reqwidth())-15, y=15)

    # Creates Boundry object for table drag and drop
    boundry_object = Text(table_manager_root, blockcursor=True,
                          state="disabled", bg="#F06233", height=DEVICE_HEIGHT-5, width=DEVICE_WIDTH)
    boundry_object.place(
        x=(orders_widget.winfo_reqwidth()+waitstaff_box.winfo_reqwidth()), y=75)

    # Creates save button
    save_button = Button(table_manager_root, text="Save", command=lambda: print(
        "test"), bg="#AB92BF", fg="#F2EFE9")
    save_button.place(x=DEVICE_WIDTH-(save_button.winfo_reqwidth()+15),
                      y=DEVICE_HEIGHT-(save_button.winfo_reqheight()+15))

    # Creates buttons to load any exisiting floorplan
    generate_floorplan_buttons(table_manager_root, orders_widget,
                               waitstaff_box, floorplan_button_identities)

    # Creates back button
    back_button = Button(table_manager_root, text="Back", command=lambda: close_page(
        page_to_close=table_manager_root), bg="#690500", fg="#F2EFE9")
    back_button.place(x=15, y=DEVICE_HEIGHT-(save_button.winfo_reqheight()+15))


# Tables functions:
def generate_tables(root, floorplan, orders,
                    waitstaff, identities, save):
    """Generates each table from selected floorplan"""

    # Clears page
    clear_page(identities, orders,
               floorplan_button_identities, waitstaff)

    # Loads "table.json" file
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        tables_object = json.load(tables_file)

        # Places all relevant info into waitstaff box
        waitstaff.config(state="normal")
        waitstaff.delete(1.0, END)
        waitstaff.insert(
            END, get_servers_on_floor(floorplan, "servers_key"))
        waitstaff.config(state="disabled")

        # Creates "new table" button
        create_new_table_button = Button(root, text="Add Table",
                                         command=lambda: create_new_table_popup(
                                             floorplan), bg="#655A7C", fg="#F2EFE9")
        create_new_table_button.place(x=waitstaff.winfo_reqwidth() +
                                      orders.winfo_reqwidth() + 15,
                                      y=DEVICE_HEIGHT -
                                      create_new_table_button.winfo_reqheight() - 15)

        # Iterates through floorplans in tables.json to find selected floorplan
        for floorplans in tables_object:
            if floorplans == floorplan:
                # Iterates through tables in chosen floorplan
                for tables in tables_object[floorplans]:
                    # Displays current table in orders box
                    orders.insert(END, f"{tables}:\n\n\n")
                    # Creates button for current table at saved coordinates.
                    new_table = Button(root, text=tables, fg="white",
                                       bg=tables_object[floorplans][tables]["colour"],
                                       command=partial(edit_or_move, floorplan, tables,
                                                       tables_object[floorplans][tables]["colour"],
                                                       tables_object[floorplans][tables]["server"]))
                    # Places the new table at its assigned coordinates
                    new_table.place(x=tables_object[floorplans][tables]["x"],
                                    y=tables_object[floorplans][tables]["y"])
                    # Gives table drag and drop properties
                    make_draggable(new_table)
                    # Adds table to table tracker list
                    table_identities.append(new_table)
    # Updates the save button so that the floorplan can be saved
    save.config(command=lambda: save_tables(
        floorplan, identities))
    # Updates window name to show the floorplan
    root.title(f"Aterio - Table Management - {floorplan}")


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
        new_table_prompt, server_default, * options)
    table_server.place(x=0, y=59)

    # Creates drop down menu for colours on floor
    colour_default = StringVar(new_table_prompt)
    colour_default.set("Blue")
    options2 = COLOUR_CHOICES
    table_colour = OptionMenu(
        new_table_prompt, colour_default, * options2)
    table_colour.place(x=0, y=30)

    # Creates submit button
    submit_button = Button(new_table_prompt, text="Submit", bg="#AB92BF", fg="#F2EFE9",
                            command=lambda: create_new_table(new_table_prompt, floorplan,
                            table_name, server_default, table_x, table_y, colour_default))
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
    table_x = int(waitstaff_box.winfo_reqwidth() +
                  orders_widget.winfo_reqwidth()+15)
    table_y = int("100")


def create_server_for_floor(new_table_prompt, floorplan, table_name, table_x, table_y,
                            submit_button, add_server, colour_default, table_server):
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


def create_new_table(popup_root, floorplan, table_name,
                     table_server, table_x, table_y, colour_default):
    """Gets and saves user inputted information for new table being created"""

    # Checks if there is a name for the new table
    if table_name.get() == "" or table_name.get() == "(New Table Name)":
        warning_popup("Please give the table a name")

    # Checks if the tables server is a valid name
    elif not table_server.get().isalpha():
        warning_popup("Please enter a valid server name")

    elif table_server.get() == "":
        warning_popup("Please assign a server to the table")

    elif colour_default.get() == "":
        warning_popup("Please assign the table a colour")

    else:
        # Gets user input from text/dropdown boxes
        server = table_server.get()
        colour = colour_default.get()


        # Sets new table data to inputted data
        new_table_info = {
            "x": table_x,
            "y": table_y,
            "server": server,
            "colour": COLOUR_CHOICES[colour]
        }

        # Opens json file to check if new table exists already
        with open("tables.json", "r", encoding="utf-8") as table_object_read:
            tables_read = json.load(table_object_read)
            for floorplans in tables_read:
                if floorplans == floorplan:
                    # Checks if the new table exists on the floor
                    if not table_name.get() in tables_read[floorplan]:
                        # If the table does not exist on the floor then the table is saved in file
                        tables_read[floorplan][table_name.get()] = {}
                    else:
                        # If the table does exist on the floor user gets warning notification
                        warning_popup("Table Already Exists")

                    # Appends table data to the new table dictionary in json file
                    tables_read[floorplan][table_name.get()].update(
                        new_table_info)
        # Writes new table data to json file
            added_table = json.dumps(tables_read, indent=4)
        with open("tables.json", "w", encoding="utf-8") as tables_object_write:
            tables_object_write.write(added_table)

        generate_tables(table_manager_root, floorplan, orders_widget, waitstaff_box,
                        table_identities, save_button)

        # Closes popup
        popup_root.destroy()


def edit_or_move(floorplan, table_name, table_colour, table_server):
    """Displays popup allowing the user to choose whether they wish to edit a table or move it"""

    # Creates popup
    edit_or_move_popup = Tk()
    edit_or_move_popup.title(f"Edit or Move {table_name}")
    edit_or_move_popup.geometry("330x100")

    # Creates confirmation text
    text = Label(edit_or_move_popup,
                 text="Are you attempting to edit or move this table?")
    text.pack()

    # Creates buttons to confirm whether table should be moved or edit popup generated
    edit_button = Button(edit_or_move_popup, text="Edit", command=lambda: config_table_gui(
        floorplan, table_name, table_colour, table_server))
    edit_button.pack()

    move_button = Button(edit_or_move_popup, text="Move",
                         command=lambda: edit_or_move_popup.destroy())
    move_button.pack()


def config_table_gui(floorplan, table_name, table_colour, table_server):
    """Allows user to config a table"""

    # Creates Popup
    config_table_popup = Tk()
    config_table_popup.title(f"Configure {table_name}")
    config_table_popup.geometry("330x100")

    # Creates Table name box and puts in current table name
    table_name_entry = Entry(
        config_table_popup, width=25, font=("Arial", 15))
    table_name_entry.insert(END, table_name)
    table_name_entry.place(x=0, y=0)

    # Creates colour dropdown and sets default colour
    colour_default = StringVar(config_table_popup)
    colour_default.set("Blue")
    options2 = COLOUR_CHOICES
    table_colour = OptionMenu(
        config_table_popup, colour_default, * options2)
    table_colour.place(x=0, y=table_name_entry.winfo_reqheight())

    # Creates Server entry box
    table_server_entry = Entry(
        config_table_popup, width=25, font=("Arial", 15))
    table_server_entry.insert(END, table_server)
    table_server_entry.place(x=0, y=(
        table_name_entry.winfo_reqheight()+table_colour.winfo_reqheight()))

    # Creates cancel and submit buttons
    cancel_button = Button(config_table_popup, text="Cancel",
                           command=lambda: config_table_popup.destroy())
    cancel_button.place(x=table_name_entry.winfo_reqwidth(), y=0)

    submit_button = Button(config_table_popup, text="Submit", command=lambda: config_table(floorplan,
                        table_name_entry, colour_default, table_server_entry,
                        table_name, config_table_popup))
    submit_button.place(x=table_name_entry.winfo_reqwidth(),
                        y=cancel_button.winfo_reqheight())


def config_table(floorplan, table_name_entry, colour_default,
                 table_server_entry, table_name, config_table_popup):
    """Saves configurements to json file"""

    # Declares existing table name
    existing_table_name = table_name

    # Sets user input to new var name.
    new_table_name = table_name_entry.get()
    new_table_colour = COLOUR_CHOICES[colour_default.get()]
    new_table_server = table_server_entry.get()

    # Checking validity of new table colour:
    if new_table_colour == "":
        warning_popup("Please select a colour for the table")

    # Checking validity of new table server:
    elif new_table_server == "":
        warning_popup("Please select a server for the table")

    # Checking validity of new table name:
    elif new_table_name == "":
        warning_popup("Please name the table")
        # Finds table in json file

    else:
        with open("tables.json", "r", encoding="utf-8") as tables_config_obj:
            tables_config = json.load(tables_config_obj)
            for floorplans in tables_config:
                if floorplans == floorplan:
                    for tables in tables_config[floorplans]:
                        if new_table_name in tables:
                            warning_popup("Please give the table a unique name")

                        elif tables == existing_table_name:
                            # Finds table to configure and edits server name and colour.
                            tables_config[floorplans][tables]["server"] = new_table_server
                            tables_config[floorplans][tables]["colour"] = new_table_colour

                            # If the user changes the table name, the old table name is replaced
                            if not new_table_name == existing_table_name:
                                tables_config[floorplans][new_table_name] = (
                                    tables_config[floorplans][tables])
                                del tables_config[floorplans][tables]

                            # popup is closed and process is finished
                            config_table_popup.destroy()
                            break
        # Saves table name and content to json file.
        with open("tables.json", "w", encoding="utf-8") as tables_config_write:
            to_write = json.dumps(tables_config, indent=4)
            tables_config_write.write(to_write)

        # Clears the page and re-places everything
        clear_page(table_identities, orders_widget,
                   floorplan_button_identities, waitstaff_box)
        generate_tables(table_manager_root, floorplan, orders_widget,
                        waitstaff_box, table_identities, save_button)
        generate_floorplan_buttons(
            table_manager_root, orders_widget, waitstaff_box, floorplan_button_identities)


def clear_page(identities, orders, floorplan_identities, waitstaff):
    """Clears loaded page"""
    # Declares the number of tables that exist
    num_of_tables = len(identities)

    # Clears floorplan buttons
    clear_floorplan_buttons(table_manager_root, orders,
                            waitstaff, floorplan_identities)

    # Deletes each table on the screen and clears widgets, also clears table_identities
    for tables in range(num_of_tables):
        identities[0].destroy()
        orders.delete("1.0", END)
        waitstaff.delete("1.0", END)
        identities.remove(identities[0])
        tables += 1


def save_tables(floorplan, identities):
    """Saves tables"""
    # Sets current table number
    table_number = 0

    # Iterates through json file to check if table exists
    with open("tables.json", "r", encoding="utf-8") as tables_object:
        tables_list = json.load(tables_object)
        for floors in tables_list:
            if floors == floorplan:
                for tables in tables_list[floorplan]:
                    # If the table being saved is the selected table, its coordinates are updated
                    if identities[table_number]["text"] == tables:
                        current_table = identities[table_number]
                        current_table_name = identities[table_number]["text"]
                        tables_list[floorplan][current_table_name]["x"] = current_table.winfo_x()
                        tables_list[floorplan][current_table_name]["y"] = current_table.winfo_y()
                    # Moves to the next table on the screen
                    table_number += 1
    # Writes the updated table positions to the json file
    updated_table = json.dumps(tables_list, indent=4)
    with open("tables.json", "w", encoding="utf-8") as tables_object_w:
        tables_object_w.write(updated_table)

# Waitstaff functions:
def get_servers_on_floor(floorplan, return_type):
    """Loads and displays the servers on floorplan"""
    # Declares variables to be used
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
                    # Sets the Current server to the server on the current table
                    current_server = tables_object[floorplans][tables]["server"]
                    # Checks if the current server has already been found
                    # If current server is not on list they are added
                    if not current_server in servers_list:
                        servers_list.append(current_server)
                        servers_colour.append(
                            tables_object[floorplans][tables]["colour"])
    # Returns list of servers in requested format
    if return_type == "servers_list":
        if not servers_list:
            servers_list.append("Please add a server to this floor")
            return servers_list
        else:
            return servers_list
    if return_type == "servers_key":
        for i in range(len(servers_list)):
            # Iterates through the list to find each server's hex code colour
            # Once found, the the servers name, and the name of the designated colour
            # is added to a list of each respective server and their colours
            server_info.append(
                f"{servers_list[i]} : "
                f"{list(COLOUR_CHOICES.keys())[list(COLOUR_CHOICES.values()).index(servers_colour[i])]}"
                "\n")
        return "".join(server_info)


# Floorplan functions:
def generate_floorplan_buttons(root, orders, waitstaff, button_identities):
    """Generates buttons to load each saved floorplan"""
    iterating_x_pos = 0
    # Loads "table.json" file
    with open("tables.json", "r", encoding="utf-8") as tables_file:
        tables_object = json.load(tables_file)
        # Iterates through floorplans in "table.json" file and creates button to load each floorplan
        for floorplan in tables_object:
            new_floorplan_button = Button(
                root, text=floorplan, font=("Arial", 15))
            # Edits floorplan button to have load correct floorplan when clicjed
            new_floorplan_button.config(command=partial(
                generate_tables, root, floorplan, orders, waitstaff,
                table_identities, save_button))

            # Places button and updates x position to make buttons evenly spaced apart
            new_floorplan_button.place(x=((waitstaff.winfo_reqwidth(
            ) + orders.winfo_reqwidth()+15) + iterating_x_pos), y=15)

            # Adds floorplan button to screen
            iterating_x_pos += (new_floorplan_button.winfo_reqwidth() + 15)
            button_identities.append(new_floorplan_button)


def clear_floorplan_buttons(root, orders, waitstaff, floorplan_identities):
    """Function to delete and regenerate floorplan buttons when new floorplan is created"""
    # Iterates through floorplan buttons and deletes them from screen
    for floorplans in range(len(floorplan_identities)):
        floorplan_identities[floorplans].destroy()
    floorplans = []
    # Once cleared the buttons are re-generated
    generate_floorplan_buttons(root, orders,
                               waitstaff, floorplan_identities)


def create_floorplan_interface(root, orders, waitstaff, floorplan_identities):
    """User interface for floorplan creation"""
    # Creates Popup
    create_floorplan_popup = Tk()
    create_floorplan_popup.title("Create New Floorplan")
    create_floorplan_popup.geometry("350x100")

    # Creates entry box so user can name floorplan
    floorplan_name = Entry(create_floorplan_popup,
                           width=25, font=("Arial", 15))
    floorplan_name.insert(END, "(New Floorplan Name)")
    floorplan_name.place(x=0, y=0)

    # Creates submit button
    submit_button = Button(create_floorplan_popup, text="Submit", bg="#AB92BF", fg="#F2EFE9",
                           command=lambda: create_floorplan(floorplan_name,
                                                            create_floorplan_popup, root, orders, waitstaff, floorplan_identities))
    submit_button.place(x=275, y=0)


def create_floorplan(floorplan_name, popup_root, root, orders, waitstaff, floorplan_identities):
    """Saves requested floorplan to json file"""

    # Checks if floorplan name is empty or placeholder text
    if floorplan_name.get() == "" or floorplan_name.get() == "(New Floorplan Name)":
        warning_popup("Please enter a name for the floorplan")

    # Checks if floorplan name contains numbers
    elif not floorplan_name.get().isalpha():
        warning_popup("Floorplan names can only contain letters")

    # If new floorplan name is valid, it is added to json file
    else:
        with open("tables.json", "r", encoding="utf-8") as tables_object_read:
            tables = json.load(tables_object_read)

            # Checks if floorplan already exists
            if not floorplan_name.get() in tables:
                tables[floorplan_name.get()] = {}
            else:
                warning_popup("Floorplan Already Exists")

        # If floorplan is valid, it is written to json file
            new_floorplan = json.dumps(tables, indent=4)
        with open("tables.json", "w", encoding="utf-8") as tables_object_write:
            tables_object_write.write(new_floorplan)
        popup_root.destroy()

        # Floorplan buttons are cleared and updated
        clear_floorplan_buttons(root, orders,
                                waitstaff, floorplan_identities)


def get_floorplans():
    """Creates a list containing each floorplan in the tables.json file"""

    # Makes a list to put floorplan names in
    floorplan_list = []

    # Iterates through floorplans and adds them to list
    with open("tables.json", "r", encoding="utf-8") as tables_object:
        tables = json.load(tables_object)
        for floorplans in tables:
            floorplan_list.append(floorplans)

    # Returns list of floorplans
    return floorplan_list


def delete_floorplan_popup(orders, waitstaff, floorplan_identities):
    """Generates a popup that allows the user to deleta/remove a created floorplan"""

    # Gives user warning that the floorplan they choose to delete will be permanently removed
    warning_popup(
        "If you continue, the selected floorplan will "
        "be deleted and the current page will be cleared")

    # Creates Popup
    delete_floorplan_popup_root = Tk()
    delete_floorplan_popup_root.title("Remove a Floorplan")
    delete_floorplan_popup_root.geometry("350x100")

    # Creates floorplan selection dropdown
    floorplan_default = StringVar(delete_floorplan_popup_root)
    floorplan_default.set(get_floorplans()[0])
    options = get_floorplans()
    floorplan_to_delete = OptionMenu(
        delete_floorplan_popup_root, floorplan_default, options[0], * options)

    floorplan_to_delete.place(x=0, y=0)

    # Creates Submit button
    submit_button = Button(delete_floorplan_popup_root, text="Submit",
                           command=lambda: delete_floorplan(delete_floorplan_popup_root,
                            floorplan_default.get(), orders, waitstaff, floorplan_identities))

    submit_button.place(x=(floorplan_to_delete.winfo_reqwidth()), y=0)


def delete_floorplan(delete_floorplan_popup_root, floorplan_to_delete,
                    orders, waitstaff, floorplan_identities):
    """Uses information from popup to remove the selected floorplan from the tables.json file"""
    # Opens json
    with open("tables.json", "r", encoding="utf-8") as tables_object:
        tables = json.load(tables_object)
        for floorplans in tables:
            # Finds selected floorplan in file
            if floorplans == floorplan_to_delete:
                # Removes floorplan and all of its contents
                tables.pop(floorplan_to_delete)

                # Writes the updated data to file
                removed_floorplan = json.dumps(tables, indent=4)
                with open("tables.json", "w", encoding="utf-8") as tables_object_write:
                    tables_object_write.write(removed_floorplan)
                    # closes popup and ends deletetion process
                    delete_floorplan_popup_root.destroy()
                break

    # Clears page in case floorplan is selected so no tables that should are on deleted floorplan remain
    clear_page(table_identities, orders, floorplan_identities, waitstaff)


# Popup Functions:
def warning_popup(warning):
    """Function to create generic popups when needed"""
    # Creates popup
    warning_popup_root = Tk()
    warning_popup_root.title(f"{warning}")

    # Adds text given in "warning" param
    warning_text = Label(warning_popup_root, text=warning)
    cancel_button = Button(warning_popup_root, text="Cancel",
                           command=lambda: warning_popup_root.destroy())
    warning_text.place(x=0, y=0)
    cancel_button.place(x=0, y=warning_text.winfo_reqheight())

    # Sets size of popup to auto fit texzt
    warning_popup_root.geometry(
        f"{warning_text.winfo_reqwidth()}x{warning_text.winfo_reqheight()+cancel_button.winfo_reqheight()}")


load_home_page()
