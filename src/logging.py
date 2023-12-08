import logging

name = __name__
logger_ = logging.getLogger(name)
logger_.setLevel(logging.DEBUG)
log_handler = logging.FileHandler(filename=f'{name}.log',
                                  encoding='utf-8',
                                  mode="a")
log_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log_handler.setFormatter(log_formatter)
logger_.addHandler(log_handler)
