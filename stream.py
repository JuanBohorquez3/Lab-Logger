"""
Holds steam class to organize connection to both origin server and data device
for a given data stream.
"""
# external imports
from typing import Dict, Tuple, Callable, Union
import logging
import colorlog
from inspect import signature

# local imports
from logger_setup import setup_child_logger
from instruments import Instrument


class Field:
    """
    Class to contain a data field that exists within a data stream and all it's attributes

    Attributes
    """
    def __init__(self, name: str, address: str, conversion: Callable = None, unit: str = ""):
        self.__name = str(name)
        self.__address = str(address)
        self.__unit = str(unit)

        self.logger = setup_child_logger(self.name)

        # Buncha warnings and typing errors
        if not isinstance(name, str):
            self.logger.warning(f"Name provided was not a string, name cast as {self.name}")
        if not isinstance(address, str):
            self.logger.warning(
                f"Address provided was not a string, address cast as {self.address}")
        if not isinstance(unit, str):
            self.logger.warning(f"units provided was not a string. units cast as {self.unit}")

        # make sure our conversion function is a function of a single variable.
        conversion = conversion if conversion is not None else (lambda x: x)
        if not callable(conversion):
            raise TypeError(
                f"{conversion} is not callable. Provide a function of a single argument"
            )
        if len(signature(conversion).parameters) != 1:
            raise TypeError(
                f"{conversion} takes the incorrect number of arguments. Provide a function of a "
                f"single argument"
            )

        self.__conversion = conversion

    @property
    def name(self) -> str:
        """Name of the field"""
        return self.__name

    @property
    def address(self):
        """Device address corresponding to the field"""
        return self.__address

    @property
    def conversion(self) -> Callable:
        """
        Function of a single variable that provides conversion between device measured value
        and value of data in desired units, to be logged in origin server
        """
        return self.__conversion

    @property
    def unit(self) -> str:
        """
        Unit of data to be logged, e.g "mW" or "electron Volts"
        """
        return self.__unit

    @property
    def conversion_doc(self) -> Union[str,None]:
        """
        Docstring attached to conversion function, if any is provided.

        Suggested docstring indicates conversion formula being used, device measured units, units of
            converted data
        """
        return self.__conversion.__doc__

    def __str__(self):
        return f"{self.__class__.__name__} : {self.name}"


class Stream:
    """
    Attributes:
        stream_name : Name of data stream in origin server this channel will manage. Must be
            formatted as {NAMESPACE}_{descriptive string}
        fields : dictionary of field names to Field objects
        data_type : type of data being sent to the server. eg. float, or bool
        server : origin.server object. Interfaces with the origin server
        instrument : Instrument object communicating with our physical measurement device
    """
    TIMEOUT = 60*1000  # server timeout time in ms
    NAMESPACE = "Hybrid"  # TODO : configure this with config file or GUI setting

    def __init__(
            self,
            stream_name: str,
            fields: Dict[str: Field],
            data_type: type,
            server: origin.server,
            instrument: Instrument):
        # use root logger temporarily
        self.logger = logging.getLogger(self.__class__.__name__)
        """
        TODO : imports for origin and Monitors
        """
        # TODO : ensure that name is formatted correctly:
        #   {Channel.NAMESPACE}_{descriptive name}
        self.__stream_name = stream_name
        setup_child_logger(str(self))

        self.__fields = fields

        if data_type not in [int, float, bool, str]:
            raise ValueError("data_type must be int, float, bool or str")
        self.__data_type = data_type

        self.__instrument = instrument

        self.server = server

        self.field_names = self.fields.keys()
        self.records = {}
        self.data = {}

        self.connection = self.connect()

    @property
    def stream_name(self):
        """
        Returns: name of the stream
        """
        return self.__stream_name

    @property
    def data_type(self) -> type:
        """
        Returns: Data type being measured
        """
        return self.__data_type

    @property
    def serv_data_type(self) -> str:
        """
        Returns: string origin library can parse to indicate data type being logged
        """
        if self.data_type in [int, float, bool]:
            return self.data_type.__name__
        elif self.data_type == str:
            return "string"

    # some Read Only attributes
    # TODO : Do they need to be exposed?
    @property
    def fields(self) -> Dict[str: Field]:
        return self.__fields

    @property
    def instrument(self) -> Instrument:
        return self.__instrument

    @property

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
        self.data = self.__instrument.measure(self.stream_name)
        return self.data

    def close(self) -> Tuple[int,int]:
        """
        Closes the connection to the server and to the device
        Returns:
            error codes provided by either the server and device, in that order
        """
        err_serv = self.connection.close()
        err_dev = self.__instrument.close()
        return err_serv, err_dev

    def __str__(self):
        return f"{self.__class__.__name__} : {self.stream_name}"
