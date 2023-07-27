
# **Aterio:**

- Designed to satisfy the criteria for NCEA L2 Assignment AS91886 for Digital Science.

- Aterio is a table management software that should be used by the host stand at a restaurant or cafe. 

- Aterio is designed to allow users to manage and keep track of most physical aspects of their restaurant/cafe.

# **Documentation:**

## **Main Page:**
Upon starting the program, you will be greeted with this page:

![Screenshot of program home page](documentation_ss\Home_Page.PNG)

At present, the "Reservation Manager" Functionality is not working however, "Table manager" Functionality is.

Once the "Table Manager" button is clicked and loaded for the first time the following page will appear:

## **Table Management:**
![Screenshot of Table Manager page with no floorplans or tables created](documentation_ss\Table_Manager_Page-Empty.PNG)

From this page you can add a floorplan by clicking the "+ Floor" button in the top right of the screen. 
You can also return to the home page at any time by pressing the "Back" Button in the bottom left of the page.

## **Creating Floor:**
Once you click the "+ Floor" Button a prompt will apear asking for the name of the floorplan to be entered. This prompt looks like the following: 

![Screenshot of Table Manager page with floorplan prompt](documentation_ss\Table_Manager_Page-New_Floor_Prompt.PNG)

In order to create a floorplan from this prompt you must replace the text in parenthesis "(New Floorplan Name)" with the unique name. We reccomend using a key feature of the dining area in your cafe/restaurant.

If the new floorplan name is the same as one that has already been created, you will receive an error "Floorplan already exists".

When you've created a floorplan, you will see the following image:
![Screenshot of Table Manager page with one floorplan](documentation_ss\Table_Manager_Page-With_Floorplan.PNG)

If you have already gone through this process, when opening the Table Manager program, this is the page you will be greeted with rather than the empty page from above.

## **Creating Tables:**
From here, you can click on a floorplan and begin creating tables.

![Screenshot of Table Manager page with floorplan loaded](documentation_ss\Table_Manager_Page-With_Floorplan_Open.PNG)

Upon clicking on a floorplan in the top bar, you will be met with the above image.

To add a table to this floorplan, you would click the "Add Table" Button in the bottom left of the orange square. this orange square is where any tables on the floorplan will be shown.

You can also save the floorplan by click the "Update Current Floorplan" button located in the bottom left of the screen.

If you choose to create a table from here, the following prompt will appear:
![Screenshot of Table Manager page with table creation prompt](documentation_ss\Table_Manager_Page-Add_Table_Prompt.PNG)

This prompt will ask you to enter the name of the new table, the colour of the table, and if no tables exist on the floorplan to add a server to the floor. 
Adding a server can be accomplished by clicking the "Add Server" button, this will then allow you to enter the name of the server you wish to add.

![Screenshot of Table Manager page with table creation and server creation prompt](documentation_ss\Table_Manager_Page-Add_Table-Prompt-New_Server.PNG)

The above image illustrates this server creation part of the prompt.

Once all fields are completed, you can then click the "Submit" button located in the prompt.

Upon submitting the table, the prompt will close, and you will have to reload the floorplan by clicking its named button in the top right bar.

## **Moving and editing tables:**
When the floorplan is reloaded, the following screen will appear:

![Floorplan with one table on](documentation_ss\Table_Manager_Page-With_Table.PNG)

This table will appear in the top right corner of the orange square, this table can then be dragged around the orange square by clicking on it and dragging around the screen.

If you wish to configure a table, you can simply click on the table and a "Configure Table" prompt will appear allowing you to edit the table's attributes, such as colour, name, and server.

## **Information widgets:**
On the far left of the page, you may manage and track orders for each table, this can be done by simply typing in this box. ***(Functionality to disable this feature may be added in the future)***

On the right of the Order management widget is a server management widget, this box will display the name and corresponding colour of the servers on the floorplan so you can tell which people are managing which tables in which areas of the restaurant.

## **Deleting Floors:**
If you decide you no longer want a floorplan that you have made, you can click the "- Floor" button on any screen.

Once clicked the following prompt will appear:

![Prompt to allow user to remove floorplan](documentation_ss\Table_Manager_Page-Remove_Floorplan_Prompt.PNG)

In order to delete a floorplan, simply click on the dropdown menu on the left of the prompt and select the floorplan you wish to remove.
From here, just click submit and the floorplan and all tables on the floorplan will be deleted permanently.