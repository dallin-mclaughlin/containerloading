# containerloading

code for container loading 3D visualizing application

## About the Project

While I was working at the meatworks at Alliance Smithfield I developed this application to make the planning of packing freight containers faster. The time needed to plan decreased for complex container orders but not for simple orders. This was because easy orders that had only two different carton sizes could be calculated by hand in 5 minutes.

I used information from "Developing Graphics Frameworks with Python and OpenGL" by Lee Stemkoski and Michael Pascale published by CRC Press in 2021, to help me implement the graphics.

I would like to redo this project and add database CRUD methods to it. I solely focused on the 3D GUI and the algorithm to get the cartons packed. I would redo it using ImGUI a C++ starter GUI library. It has all the essentials I need. Many developers have used this library to create their own game engines for example, <p><a href="https://www.youtube.com/@thecherno">The Cherno</a></p>

## Different Project Menus

![Alt text](./images/homescreen.png 'Home Screen')

This is the Home screen. The user will decide whether they wish to add another carton item to the database or start setting up the container for planning.

![Alt text](./images/inputscreen.png 'Input Screen')

This is the Input screen. Here a user will input the carton types and how many of each type will need to be loaded into the container.

![Alt text](./images/viewallscreen.png 'View All Screen')

This is the View screen. You can view the container from any angle. Each stack of cartons can be selected so that the stack can be modified or deleted.

![Alt text](./images/viewstackscreen.png 'View Stack Screen')
This is the View screen. Each carton in a currently selected stack can be selected so that the carton can change its orientation or deleted.
