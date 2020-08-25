"""
File to hold the main loop of the logger
"""
# External imports
import os
import sys
import time

# Local imports
#import origin
from logger_setup import setup_root_logger

DATA = 15

def recorder():
    """
    Main loop for the lab logger. Should loop through all streams we're watching, prompt
    measurements and post the measured data to the origin server.
    """
    devices = []  # list of devices measuring our streams

    pass


if __name__ == "__main__":

    print("Setting up logger")
    root_log = setup_root_logger()
    root_log.critical("CRITICAL")
    root_log.error("ERROR")
    root_log.warning("WARN")
    root_log.info("INFO")
    root_log.debug("DEBUG")
    root_log.data("DATA")
    recorder()