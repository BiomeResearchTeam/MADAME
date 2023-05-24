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

# DA SOSTITUIRE CON LE FUNZIONALITA' DI RICH:
class Color:
    # Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

    # Text format
    BOLD = '\033[1m'
    ITALIC = '\33[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\33[5m'

    # Background colors
    BLACKBG = '\33[40m'
    REDBG = '\33[41m'
    GREENBG = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG = '\33[46m'
    WHITEBG = '\33[47m'

    # End of format\colors
    END = '\033[0m'


Utilities = Utilities('Utilities')

   



