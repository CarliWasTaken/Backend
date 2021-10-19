import logging
import sys

class Log:
    __logger = None

    @staticmethod
    def get_instance():
        '''Gets the instance of the class Log
        
        Returns the static variable of the class Log or creates the instance
        of this class.

        Returns
        -------
        Log
            the class Log
        '''
        if Log.__logger is None:
            Log.__logger = Log()
        return Log.__logger

    def __init__(self):
        # generate the logger
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.INFO)
        
        # format for the output
        self.__formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')

        # console logging
        self.__stdout_handler = logging.StreamHandler(sys.stdout)
        self.__stdout_handler.setFormatter(self.__formatter)
        self.__stdout_handler.setLevel(logging.DEBUG)

        # file logging
        self.__file_handler = logging.FileHandler('logs.log')
        self.__file_handler.setFormatter(self.__formatter)
        self.__file_handler.setLevel(logging.DEBUG)

        # add console and file handler to logging
        self.__logger.addHandler(self.__stdout_handler)
        self.__logger.addHandler(self.__file_handler)
        pass

    # sets the current logging value
    def set_console_log_level(self, level):
        '''Sets the logging level for the console

        This method is provided with a level by the logging library
        or an integer (10, 20, 30, 40, 50) in order to update the level
        of logging on console level.

        Parameters
        ----------
        level : int
            The level on which the console should log
        '''
        self.__stdout_handler.setLevel(level)
        pass

    def set_file_log_level(self, level):
        '''Sets the logging level for the file

        This method is provided with a level by the logging library
        or an integer (10, 20, 30, 40, 50) in order to update the level
        of logging on file level.
        
        Parameters
        ----------
        level : int
            The level on which the file should log
        '''
        self.__file_handler.setLevel(level)
        pass

    def debug(self, message):
        '''Creates a debug log

        Logs the message on the console or a file if the log level is
        set correctly.
        
        Parameters
        ----------
        message : str
            message that should be present in the log
        '''
        self.__logger.debug(message)
        self.__logger.deb
        pass

    def info(self, message):
        '''Creates an info log

        Logs the message on the console or a file if the log level is
        set correctly.
        
        Parameters
        ----------
        message : str
            message that should be present in the log
        '''
        self.__logger.info(message)
        pass

    def warning(self, message):
        '''Creates a warning log

        Logs the message on the console or a file if the log level is
        set correctly.
        
        Parameters
        ----------
        message : str
            message that should be present in the log
        '''
        self.__logger.warning(message)
        pass

    def error(self, error):
        '''Creates an error log

        Logs the corresponding excpetion to the console or a file if
        the log level is set correctly.
        
        Parameters
        ----------
        message : str
            message that should be present in the log
        '''
        self.__logger.error(error)
        pass

    def critical(self, message):
        '''Creates a critical log

        Logs the message on the console or a file if the log level is
        set correctly.
        
        Parameters
        ----------
        message : str
            message that should be present in the log
        '''
        self.__logger.critical(message)

    def move(self, x, y):
        '''Creates an movement info log

        Logs the currenct speed and angel of the car to the
        console or a file if the log level is set correctly.
        
        Parameters
        ----------
        x : int
            speed value of the car
        y : int
            steering value of the car
        '''
        self.info(f'Speed: {x}, Angel: {y}')
