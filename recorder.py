"""
File to hold the main loop of the logger
"""
# External imports
import os
import sys
import time

# TODO : Figure out a half decent way of doing this import
origin_path = r"C:\Users\Hybrid\Repos\Origin"
sys.path.append(os.path.join(origin_path, "lib"))
# Local imports
from origin.client import server
from logger_setup import setup_root_logger
from stream import Stream, Field
from instruments import Instrument

DATA = 15

def make_streams():
    MOT_I2V_fields = {}
    units = "mW"
    conversion_desc = "V to mW"
    MOT_I2V_fields["Y1"] = Field(
        "Y1",
        "ai0",
        lambda v: 0.902*v+0.022,
        units,
        conversion_desc
    )
    MOT_I2V_fields["Y2"] = Field(
        "Y2",
        "ai1",
        lambda v: 0.849*v+0.028,
        units,
        conversion_desc
    )
    MOT_I2V_fields["X1"] = Field(
        "X1",
        "ai4",
        lambda v: 0.740*v+0.026,
        units,
        conversion_desc
    )

    MOT_stream = Stream("MOT I2Vs, ")


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