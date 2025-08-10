from autogen_core import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME
import logging

# Configure the trace logger
trace_file_handler = logging.FileHandler("autogen_trace.log")
trace_file_handler.setLevel(logging.DEBUG)
trace_logger = logging.getLogger(TRACE_LOGGER_NAME)
trace_logger.addHandler(trace_file_handler)
trace_logger.setLevel(logging.DEBUG)

# log file
file_handler = logging.FileHandler("autogen_event.log")
file_handler.setLevel(logging.INFO)
event_logger = logging.getLogger(EVENT_LOGGER_NAME)
event_logger.addHandler(file_handler)
event_logger.setLevel(logging.INFO)