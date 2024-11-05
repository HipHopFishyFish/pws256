import os

def setupchecks():
    path = os.path.dirname(__file__) + "/srcimport.py"
    with open(path, "w") as file:
        file.write("""\"THIS FILE IS PREGENERATED. ANY CHANGE YOU MAKE WILL BE OVERWRITTEN\"

from ..src import _Password, Password, PwsType, defaultpass""")
        
    path = os.path.dirname(__file__) + "/usersrcimport.py"
    with open(path, "w") as file:
        file.write("""\"THIS FILE IS PREGENERATED. ANY CHANGE YOU MAKE WILL BE OVERWRITTEN\"

from ..src.users import User""")
        

