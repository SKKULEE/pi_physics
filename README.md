# pi_physics
Calculating pi by 1-dimensional elastic collision model simulation.  

### Introduction
This program is built to show that counting 1-dimensional elastic collisions can derive the value of pi.  

The hyperlinked video below is what I referred and there are all the details about what this program exactly do.  
[The most unexpected answer to a counting puzzle - 3Blue1Brown](https://youtu.be/HEfHFsfGXjs)

### How to Use
![experiment_state](https://user-images.githubusercontent.com/100181857/155082583-1ecbec4a-a420-42f9-a109-e4b64cd400eb.png)  
The initial state of the program is "experiment".  
"RS" button is used for entering "Setting" state.  
"RUN/PAUSE" button is used for pausing/resuming the current experiment.  
"Collisions" displays the number of collisions occurred in the current experiment.    

![setting_state](https://user-images.githubusercontent.com/100181857/155082600-76c61301-0f61-4af8-ad95-b1c1438970f4.png)  
If you enter "Setting" state by clicking "RS" button, all the experiment information are deleted, and you can set new experiment information.  
Size: Set the size of a collider (unit: meter)  
Mass: Set the Mass of the collider (unit: kilogram)  
Position: Set the initial position of the collider (unit: meter)  
Velocity: Set the initial velocity of the collider (unit: m/s)  
Color: Set the color of the collider (default: random)  
"ADD" button is used for adding new collider data by given information.  
"DONE" button is used for entering "experiment" state with the current experiment information.    

### Initial state
The program state is "experiment" state and two initial colliders' information are as follows:  
collider1 - size 1, mass 1, position 2, velocity 0, color RED  
collider2 - size 1, mass 1, position 5, velocity -1, color BLUE  

### Note
note1: All the information for colliders can be any integer/decimal, but using integers only is recommended.  
note2: RED, GREEN, BLUE, BLACK, WHITE, YELLOW, MAGENTA, CYAN are valid colors.  
note3: Entering some invalid data (ex: negative mass) is not prohibited, but it may cause unexpected malfunctions.  
note4: Changing window size is not fully supported.  
