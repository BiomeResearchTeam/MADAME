import os

# Utilities classes

class Directory:
    def __init__(self, name):
        self.name = name

    def setMADAMEdirectory(self, set_directory):
    # Sets working directory, creates MADAME main folder, then changes 
    # working directory into MADAME main folder
        os.chdir(set_directory)
        main_folder = "MADAME"
        directory = os.path.join(os.getcwd(), main_folder)
        self.createDirectory(directory) 
        os.chdir(directory)

    def createDirectory(self, new_directory):
    # Creates directory only if it doesn't exist yet
        if os.path.exists(new_directory):
            pass
        else:
            os.makedirs(new_directory)

   
class Utilities:
    def __init__(self, name):
        self.name = name

    def bytes_converter(self, bytes):
    # Converts bytes    
        units = ['KB', 'MB', 'GB', 'TB']
        mult = 1024
        for unit in units:
            bytes = bytes / mult           
            if bytes < mult:
                return '{0:.2f} {1}'.format(bytes, unit)



