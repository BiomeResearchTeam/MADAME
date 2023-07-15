import os
import logging
import platform

# Utilities classes

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


    def append_new_line(self, file_name, text_to_append):
    # Open the file in append & read mode ('a+')
        with open(file_name, "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(text_to_append)


    def createDirectory(self, new_directory):
    # Creates directory only if it doesn't exist yet
        if os.path.exists(new_directory):
            pass
        else:
            os.makedirs(new_directory)


    def log(self, __name__, user_session):

        logger = logging.getLogger(__name__)

        # Create handlers
        c_handler = logging.StreamHandler()
        if "Downloads" not in user_session:
            f_handler = logging.FileHandler(os.path.join('Downloads', user_session, f'{user_session}_log.log'))
        else:
            f_handler = logging.FileHandler(os.path.join(user_session, f'{os.path.basename(user_session)}_log.log'))

        logger.setLevel(logging.DEBUG) 
        if not logger.handlers: #prevent logger.info printing twice the message
            c_handler.setLevel(logging.INFO) # logger.info for saving to log file and printing nicely (only the message)
            f_handler.setLevel(logging.DEBUG) # logger.debug for ONLY saving log to file - does not print on console

            # Create formatters and add it to handlers
            c_format = logging.Formatter('%(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)

        return logger


    def clear(self):
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('tput reset')

class Color:
    # Bright RGB colors
    RED = '\033[38;2;255;0;0m' 
    GREEN = '\033[38;2;0;255;0m' 
    YELLOW = '\033[38;2;255;255;0m' 
    BLUE = '\033[38;2;0;0;255m' 
    PURPLE = '\033[38;2;255;0;255m' 
    CYAN = '\033[38;2;0;255;255m' 

    # Text format
    BOLD = '\033[1m'
    ITALIC = '\33[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\33[5m'

    # Bright RGB background colors
    BLACKBG = '\033[48;2;0;0;0m'
    REDBG = '\033[48;2;255;0;0m' 
    GREENBG = '\033[48;2;0;255;0m'
    YELLOWBG = '\033[48;2;255;255;0m'
    BLUEBG = '\033[48;2;0;0;255m'
    PURPLEBG = '\033[48;2;255;0;255m'
    WHITEBG = '\033[48;2;255;255;255m'

    # End of format\colors
    END = '\033[0m'


Utilities = Utilities('Utilities')

   



