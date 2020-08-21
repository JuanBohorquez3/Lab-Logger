"""
Holds steam class to organize connection to both origin server and data device
for a given data stream.
"""
# external imports
from typing import Dict, Tuple
import logging

# local imports


class Stream:
    """
    Attributes:
        stream_name : Name of data stream in origin server this channel will manage. Must be
            formatted:
            {NAMESPACE}_{descriptive string}
        data_type : string describing type of data being sent to the server. eg. float, or bool
        server : origin.server object. Interfaces with the origin server
        data_map : mapping of field names to physical channels on our measurement device
        device : Monitor object communicating with our physical measurement device
    """
    TIMEOUT = 60*1000  # server timeout time in ms
    NAMESPACE = "Hybrid"  # TODO : configure this with config file or GUI setting

    def __init__(self, stream_name: str, data_type: str, server: origin.server, data_map: Dict[str: str], device: Monitor):
        self.logger = logging.getLogger(self.__class__.__name__)  # TODO set up logger
        """
        TODO : imports for origin and Monitors
        """
        # TODO : ensure that name is formatted correctly:
        #   {Channel.NAMESPACE}_{descriptive name}
        self.__stream_name = stream_name
        # TODO : ensure data_type is string corresponding to c types:
        #   eg 'float' or 'bool'
        self.__data_type = data_type
        self.server = server
        self.data_map = data_map
        self.device = device

        self.data_names = self.data_map.keys()
        self.records = {}
        self.data = {}

        self.connection = self.connect()

    @property
    def stream_name(self):
        return self.__stream_name

    @property
    def data_type(self):
        return self.__data_type

    def connect(self):
        """
        Initiates connection with the server. Passes info on stream name and data types of the
        stream

        Returns:
            connection, object representing our connection to the server
        """
        self.logger.debug(f"Connecting stream {self.stream_name}\n records {self.records}")
        connection = self.server.registerStream(
            stream=self.stream_name,
            records=self.records,
            timeout=self.TIMEOUT
        )
        return connection

    def measure(self) -> Dict[str: float]:
        """
        Instructs our device to measure the data and returns said data
        Returns:
            measured data mapping field names to their measured values
        """
        self.data = self.device.measure(self.stream_name)
        return self.data

    def close(self) -> Tuple[int,int]:
        """
        Closes the connection to the server and to the device
        Returns:
            error codes provided by either the server and device, in that order
        """
        err_serv = self.connection.close()
        err_dev = self.device.close()
        return err_serv, err_dev
