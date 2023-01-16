import os
listOfProjectIDs_abs_path = "home/casa/prova/oo/aaa"

listOfProjectIDs_path = os.sep.join(os.path.normpath(listOfProjectIDs_abs_path).split(os.sep)[-2:])

print(listOfProjectIDs_path)