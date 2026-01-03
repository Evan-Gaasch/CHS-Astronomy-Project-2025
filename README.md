# CHS-Astronomy-Project-2025

Install instructions (Windows, DM me for other OS):
1) Download requirements.txt file (on GitHub)
2) In the windows search bar (press windows icon), search "cmd" and click on the "command prompt" app
3) Open command prompt
4) use dir to see directories and cd *directory-name* to move into a directory (for example, cd Documents would move from C:/Users/Evan to C:/Users/Evan/Documents for my PC)
5) Once you have navigated to a directory you want to put your virtual environment in (I recommend creating a folder named astronomy in your documents folder and navigating into it), proceed to the next step.

6) Now, we need to install python. If you don't have an existing version of python, run the command `python`, which will open a windows store window. Click the install button for python 3.13.9
Note: If you have python already on your computer, update to 3.13.9 or run the command `python`. If you wish to install from the Python website, make sure you add python to path (just DM me)

Once Python is installed:
8) Run the command `pip -m venv astro-project` (where astro-project is the name of your virtual environment on your computer, feel free to change this name)
9) Run the command `./astro-project/Source/activate.bat` to activate the virtual environment
10) Move the python file [when we make it] (downloaded from GitHub) and the requirements.txt file to your "astronomy" folder using file manager
11) In command prompt, run the command `pip install -r requirements.txt` to install all dependencies without conflict
12) To run the script, run the command `python [whatever we decide to call our file].py`

Note: if you ever want to work in a different virtual environment or exit the virtual environment, run the command `deactivate` in command prompt, or `exit` to close the terminal completely
