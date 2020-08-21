"""
File to hold the main loop of the logger
"""
# External imports
import os
import sys
import time
import logging
import colorlog

# Local imports
#import origin

DATA = 15


def setup_loggers() -> logging.Logger:
    """
    Sets up logging in the module

    Sets up the root logger in detail, creating a new logging level for our monitored data,
    establishing a color-coded logging scheme for different logging levels, and setting the stdout
    as our handler for our root logger.

    The custom level is the DATA level, to be used when logging data that is being posted to the
    server, in order to readily distinguish it from diagnostic messages.

    Returns: logger object with name "root", aka the root logger. Calls to this logger's logging
        functions will work just as they would if they were calls to logging. i.e
        | root_logger.info("Hello World")
        will output to the stdout identically to
        | logging.info("Hello World")
    """
    def data(self, message, *args, **kwargs):
        """Custom logging function we're going to pass to our logger"""
        if self.isEnabledFor(DATA):
            self._log(DATA, message, args, **kwargs)

    # Add functionality for a custom logging level
    # To be used when logging data that is being recorded by our instruments
    logging.addLevelName(DATA, "DATA")
    logging.DATA = DATA
    logging.Logger.data = data

    # Explicitly set up the base logger from which all loggers will inherit
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Establish the handler we want the root logger to use
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # As well as the formatting we're interested in using for our logs
    root_formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(levelname)s - %(name)s - %(asctime)s : %(white)s%(bg_black)s\n%(message)s\n",
        log_colors={
            'DEBUG': 'cyan',
            'DATA': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'black,bg_white'
        }
    )

    # set the formatter for our handler
    console_handler.setFormatter(root_formatter)
    # set our handler for the logger
    root_logger.addHandler(console_handler)

    return root_logger


def recorder():
    """
    Main loop for the lab logger. Should loop through all streams we're watching, prompt
    measurements and post the measured data to the origin server.
    """
    devices = []  # list of devices measuring our streams

    pass


if __name__ == "__main__":

    print("Setting up logger")
    root_log = setup_loggers()
    root_log.critical("CRITICAL")
    root_log.error("ERROR")
    root_log.warning("WARN")
    root_log.info("INFO")
    root_log.debug("DEBUG")
    root_log.data("DATA")
    recorder()