import logging
import colorlog

DATA = 15


def setup_root_logger(level: int = logging.INFO, fmt: str = None) -> logging.Logger:
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
        and
        | logging.info("Hello World")
        will output to the stdout identically
    Args:
        level - logging level to establish for the root logger. A logger set to a given level
            will print messages at that level and above, ignoring other options. Options are:
            logging.DEBUG = 10
            logging.INFO = 20
            logging.WARNING = 30
            logging.ERROR = 40
            logging.CRITICAL = 50
        fmt - formatting string. For instructions on use see the documentation on logging
            formatters. Uses the % style.
            If None is passed in a default style is used.
    Returns:
        the root logger
    """
    try:
        level = int(level)
    except ValueError as e:
        raise TypeError("level arg must be an int, or castable to an int") from e

    def data(self, message, *args, **kwargs):
        """Custom logging function used to log data being measured, posted, and read"""
        if self.isEnabledFor(DATA):
            self._log(DATA, message, args, **kwargs)

    # Add functionality for a custom logging level
    # To be used when logging data that is being recorded by our instruments
    logging.addLevelName(DATA, "DATA")
    logging.DATA = DATA
    logging.Logger.data = data

    # Explicitly set up the base logger from which all loggers will inherit
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Establish the handler we want the root logger to use
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # As well as the formatting we're interested in using for our logs
    root_formatter = colorlog.ColoredFormatter(
        fmt=("%(log_color)s%(levelname)s - %(name)s - %(asctime)s : "
             "%(white)s%(bg_black)s\n%(message)s\n"),
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


def setup_child_logger(name: str,
                       level: int = logging.INFO,
                       formatter: logging.Formatter = None,
                       propagate: bool = False) -> logging.Logger:
    """
    Sets up a logger other than the root logger to be used in this module.

    Args:
        name : name to be used to reference the logger
        level : logging level to use. Typical options are:
            logging.DEBUG
            logging.INFO
            logging.WARNING
            logging.ERROR
            logging.CRITICAL
        formatter : formatter to be used by this logger. If none is passed the root formatter is
            used
        propagate : Sets the propagate attribute on the new logger. If this is true, all events
            logged to this logger will be passed to the ancestor loggers' handlers.
            If this is set to true and a message is sent to the same handler that output stream may
            log the event twice.
    Returns:
        logger that was created
    """
    if not isinstance(name, str):
        name = str(name)
        logging.warning(f"name should be a string. Attempted to cast it as {name}")

    logger = logging.getLogger(name)
    logger.propagate = propagate
    # Build a handler
    handler = colorlog.StreamHandler()
    handler.setLevel(level)
    # Use the same formatter used by our root handler
    root_logger = logging.getLogger()
    formatter = root_logger.handlers[0].formatter
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger