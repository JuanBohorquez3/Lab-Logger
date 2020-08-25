"""
Instrument abstact base class for the lab logger

Base class from which all instruments should inherit.
"""
# external imports
from abc import ABC, abstractmethod
from typing import Dict


class Instrument(ABC):
    """
    Instrument abstract base class
    """

    # Overwrite this class attribute with error codes from your device, or with a property that
    #   provides those error codes
    ERRORS = {0: "OK"}

    def __init__(self, streams: Dict[str: Dict[str: str]]):
        """
        Args:
            streams : Dict mapping stream names to data dictionaries mapping data fields to physical
                channels on the instrument
                i.e.
                {stream name:
                    {field name : instrument channel}
                }
        """
        self.streams: Dict[str: Dict[str: str]] = streams

        self.stream_names = self.streams.keys()
        self.fields = []
        self.channels = []
        for stream in self.streams:
            self.fields.append([stream.keys()])
            self.channels.append([stream.values()])

    @abstractmethod
    def start(self) -> int:
        """
        Overwrite this function. It should initialize the device and start our measurement loop
        Returns: An error code provided by the device API
        """
        raise NotImplementedError(
            f"start function not implemented in instrument {self.__class__.__name__}"
        )

    @abstractmethod
    def measure(self, stream: str = None) -> Dict[str: float]:
        """
        Overwrite this function. It should query the device to measure stream (or all streams).
        Args:
            stream : name of stream to be queried. If not specified all streams being considered by
                this device are queried
        Returns:
            data : dictionary of data. If stream is specified data looks like:
                {field name : field data}
                otherwise it looks like
                {stream_name: {field name : field data}}
        """
        if stream is not None and stream not in self.streams.keys():
            raise ValueError(f"Stream name {stream} not a stream managed by this Instrument")

    @abstractmethod
    def close(self) -> int:
        """
        Overwrite this function to safely end the measurement and close the connection to the device
        Returns:
            Error code indicating the success or failure of the closing operation
        """
        return 0
