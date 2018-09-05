# 2048 1.1
Fix the bug that the game can't over correctly.
# 2048 
This is a 2048 game made by python. The version of python is 3.6.3. And it uses the "wxpython" extension package. For windows and python 3.6.3, wxPython-4.0.0b2-cp36-cp36m-win32.whl is required to install.
# some trivial ideas about the programme
I want to make a easy 2048 game by python to practice my proficiency in using python. At first, I find an example in www.shiyanlou.com. It is useful and I understand how the 2048 game is built and how the game runs.
## There are some points which I learned from it:
1.The concept of state machine.
2.Use dict() and zip() together to create initialize a complex dictionary. 
## But it still has some problems:
1.It use "curses" extension package. Because of some reason, it can't be running in the terminal of pycharm. But if you run it in the windows shell or cmd, it works. I guess it is beacuse the size of pycharm's  terminal is not big enough.
2.The UI is really ugly!!
## So I learn to use wxpython to write a more beautiful UI. Then it becomes what you see now.
